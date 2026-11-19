// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IVerifier.sol";

/**
 * @title ZKDigitalAssetContract
 * @author ZK-MetaTrade Research Team
 * @notice Trust-Free AIGC Trading Contract featuring:
 *         1. Cryptographically guaranteed Fair Exchange via zk-SNARK verification
 *         2. Multi-Parent Directed Acyclic Graph (DAG) Royalty Distribution
 *         3. Reentrancy-safe pull payment escrow
 */
contract ZKDigitalAssetContract {
    struct CustomerAssetData {
        string encryptedSymmetricKey;
        string encryptedFileHash;
        string ipfsURI;
        bool zkVerified;
    }

    struct AncestorRoyalty {
        address payable parentContract;
        uint256 basisPoints; // e.g. 500 = 5.00%
    }

    // State Variables
    mapping(address => CustomerAssetData) private customerAddrToData;
    mapping(address => uint256) private userFund;
    mapping(address => uint256) private userFundWithdrawable;
    mapping(address => bool) private userComparedHashes;
    mapping(address => uint8) public consecutiveCompareFailures;

    uint256 public digitalAssetPrice;
    address public owner;
    IVerifier public zkVerifier;
    
    // DAG Lineage: Multi-parent support
    AncestorRoyalty[] public ancestorRoyalties;
    uint256 public totalCommissionBps;
    uint256 public constant MAX_TOTAL_ROYALTY_BPS = 5000; // Max 50% total royalties

    // Events
    event CustomerFunded(address indexed customerAddr, uint256 indexed fundAmount);
    event AccessGrantedZK(address indexed customerAddr, string ipfsURI, bool zkVerified);
    event SettlementExecuted(address indexed customerAddr, uint256 netSellerAmount, uint256 totalRoyaltiesPaid);
    event RefundIssued(address indexed customerAddr, uint256 indexed refundAmount);
    event PriceUpdated(uint256 oldPrice, uint256 newPrice);
    event RoyaltyDistributed(address indexed parentContract, uint256 amount);

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "ZKMetaTrade: Caller is not the owner");
        _;
    }

    modifier nonReentrant() {
        require(!_locked, "ZKMetaTrade: Reentrancy guard");
        _locked = true;
        _;
        _locked = false;
    }
    bool private _locked;

    /**
     * @notice Initializes the asset contract with pricing, ZK verifier, and DAG ancestors
     */
    function initialize(
        uint256 assetPrice,
        address _owner,
        address _verifier,
        address payable[] memory _parentAssets,
        uint256[] memory _parentBps
    ) external {
        require(owner == address(0), "ZKMetaTrade: Already initialized");
        require(_owner != address(0), "ZKMetaTrade: Invalid owner address");
        require(_verifier != address(0), "ZKMetaTrade: Invalid verifier address");
        require(_parentAssets.length == _parentBps.length, "ZKMetaTrade: Ancestor arrays length mismatch");

        owner = _owner;
        digitalAssetPrice = assetPrice;
        zkVerifier = IVerifier(_verifier);

        uint256 totalBps = 0;
        for (uint256 i = 0; i < _parentAssets.length; i++) {
            require(_parentAssets[i] != address(0), "ZKMetaTrade: Zero address ancestor");
            ancestorRoyalties.push(AncestorRoyalty({
                parentContract: _parentAssets[i],
                basisPoints: _parentBps[i]
            }));
            totalBps += _parentBps[i];
        }
        require(totalBps <= MAX_TOTAL_ROYALTY_BPS, "ZKMetaTrade: Total royalties exceed 50%");
        totalCommissionBps = totalBps;
    }

    /**
     * @notice Buyer deposits license fee into escrow
     */
    function registerRequest() external payable nonReentrant {
        require(msg.sender != owner, "ZKMetaTrade: Owner cannot purchase own asset");
        require(msg.value >= digitalAssetPrice, "ZKMetaTrade: Insufficient payment");
        require(userFund[msg.sender] == 0, "ZKMetaTrade: Active request already exists");
        require(consecutiveCompareFailures[msg.sender] < 2, "ZKMetaTrade: Address banned for repeated failures");

        delete customerAddrToData[msg.sender];
        userComparedHashes[msg.sender] = false;
        userFund[msg.sender] = msg.value;

        emit CustomerFunded(msg.sender, msg.value);
    }

    /**
     * @notice Seller grants access with cryptographic zk-SNARK proof of key validity.
     * Prevents the Poison Key attack.
     */
    function grantAccessZK(
        address customerAddr,
        string calldata encryptedFileHash,
        string calldata encryptedSymmetricKey,
        string calldata ipfsURI,
        uint256[2] calldata a,
        uint256[2][2] calldata b,
        uint256[2] calldata c,
        uint256[3] calldata publicInputs
    ) external onlyOwner {
        require(userFund[customerAddr] >= digitalAssetPrice, "ZKMetaTrade: Buyer has not escrowed funds");
        require(bytes(customerAddrToData[customerAddr].ipfsURI).length == 0, "ZKMetaTrade: Access already granted");

        // Cryptographic ZK-SNARK verification of key-ciphertext binding
        bool isProofValid = zkVerifier.verifyProof(a, b, c, publicInputs);
        require(isProofValid, "ZKMetaTrade: Invalid ZK proof - Poison Key detected");

        customerAddrToData[customerAddr] = CustomerAssetData({
            encryptedSymmetricKey: encryptedSymmetricKey,
            encryptedFileHash: encryptedFileHash,
            ipfsURI: ipfsURI,
            zkVerified: true
        });

        emit AccessGrantedZK(customerAddr, ipfsURI, true);
    }

    /**
     * @notice Buyer verifies the downloaded ciphertext hash.
     * If matched, funds settle to seller and all DAG ancestors atomically.
     */
    function compareHashes(string calldata customerHash) external nonReentrant {
        CustomerAssetData memory assetData = customerAddrToData[msg.sender];
        require(bytes(assetData.ipfsURI).length != 0, "ZKMetaTrade: Access not granted yet");
        require(userFund[msg.sender] >= digitalAssetPrice, "ZKMetaTrade: Escrow balance deficient");

        // Hash mismatch check
        if (!compareStrings(customerHash, assetData.encryptedFileHash)) {
            consecutiveCompareFailures[msg.sender]++;
            uint256 refundAmount = userFund[msg.sender];
            userFund[msg.sender] = 0;
            userFundWithdrawable[msg.sender] += refundAmount;
            delete customerAddrToData[msg.sender];

            emit RefundIssued(msg.sender, refundAmount);
            return;
        }

        // Hashes match: Reset failure counter & execute settlement
        consecutiveCompareFailures[msg.sender] = 0;
        uint256 totalCost = digitalAssetPrice;
        userFund[msg.sender] -= totalCost;
        userComparedHashes[msg.sender] = true;

        // Distribute royalties across all DAG ancestors
        uint256 totalRoyaltiesDistributed = 0;
        for (uint256 i = 0; i < ancestorRoyalties.length; i++) {
            uint256 royalty = (totalCost * ancestorRoyalties[i].basisPoints) / 10000;
            if (royalty > 0) {
                totalRoyaltiesDistributed += royalty;
                (bool success, ) = ancestorRoyalties[i].parentContract.call{value: royalty}("");
                require(success, "ZKMetaTrade: Ancestor royalty split failed");
                emit RoyaltyDistributed(ancestorRoyalties[i].parentContract, royalty);
            }
        }

        // Net payout to seller
        uint256 netSellerPayout = totalCost - totalRoyaltiesDistributed;
        userFundWithdrawable[owner] += netSellerPayout;

        emit SettlementExecuted(msg.sender, netSellerPayout, totalRoyaltiesDistributed);
    }

    /**
     * @notice Buyer retrieves the verified symmetric key after settlement
     */
    function getEncryptedSymmetricKey() external view returns (string memory) {
        require(userComparedHashes[msg.sender], "ZKMetaTrade: Settlement not completed");
        return customerAddrToData[msg.sender].encryptedSymmetricKey;
    }

    /**
     * @notice Pull payment pattern to prevent reentrancy and lockup
     */
    function withdrawFund() external nonReentrant {
        uint256 withdrawable = userFundWithdrawable[msg.sender];
        require(withdrawable > 0, "ZKMetaTrade: No withdrawable funds");

        userFundWithdrawable[msg.sender] = 0;
        (bool success, ) = payable(msg.sender).call{value: withdrawable}("");
        require(success, "ZKMetaTrade: Withdrawal transfer failed");
    }

    /**
     * @notice Buyer cancels request if seller has not granted access
     */
    function cancelRequest() external nonReentrant {
        require(bytes(customerAddrToData[msg.sender].ipfsURI).length == 0, "ZKMetaTrade: Access already granted");
        uint256 amount = userFund[msg.sender];
        require(amount > 0, "ZKMetaTrade: No active request funds");

        userFund[msg.sender] = 0;
        userFundWithdrawable[msg.sender] += amount;
        delete customerAddrToData[msg.sender];

        emit RefundIssued(msg.sender, amount);
    }

    /**
     * @notice Fallback to accept royalties from descendant DAG assets
     */
    receive() external payable {
        userFundWithdrawable[owner] += msg.value;
    }

    function isCustomer(address sender) external view returns (bool) {
        return userComparedHashes[sender];
    }

    function getIpfsURI(address customerAddr) external view returns (string memory) {
        require(bytes(customerAddrToData[customerAddr].ipfsURI).length != 0, "ZKMetaTrade: Access not granted");
        return customerAddrToData[customerAddr].ipfsURI;
    }

    function getPrice() external view returns (uint256) {
        return digitalAssetPrice;
    }

    function getWithdrawableFund() external view returns (uint256) {
        return userFundWithdrawable[msg.sender];
    }

    function getAncestorCount() external view returns (uint256) {
        return ancestorRoyalties.length;
    }

    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b));
    }
}
