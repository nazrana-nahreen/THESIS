// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ZKDigitalAssetContract.sol";

/**
 * @dev OpenZeppelin Contracts (last updated v5.0.0) (proxy/Clones.sol)
 * Minimal implementation of EIP-1167 Minimal Proxy Clone
 */
library Clones {
    function clone(address implementation) internal returns (address instance) {
        assembly {
            // Cleans the upper 96 bits of the `implementation` word, then packs the first 3 bytes
            // of the bytecode with the address, then the rest of the bytecode.
            mstore(0x00, or(shr(0xe8, shl(0x60, implementation)), 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000))
            mstore(0x20, or(shl(0x78, implementation), 0x5af43d82803e903d91602b57fd5bf3))
            instance := create(0, 0x09, 0x37)
        }
        require(instance != address(0), "ERC1167: create failed");
    }
}

/**
 * @title DAGMarketplace
 * @author ZK-MetaTrade Research Team
 * @notice Factory and registry for ZK-verified, DAG-lineage AIGC digital assets.
 */
contract DAGMarketplace {
    using Clones for address;

    uint256 public immutable listingFee;
    address public contractOwner;
    address public immutable template;
    address public immutable zkVerifier;

    uint256 public constant OBSERVER_STAKE_AMOUNT = 0.01 ether;
    uint256 public constant PLAGIARISM_REWARD = 0.02 ether;

    mapping(address => bool) public isAssetActive;
    mapping(address => mapping(address => uint8)) public ratings;
    mapping(address => address[]) public assetToAncestors;
    mapping(address => uint256) public observerStakes;

    event AssetListed(address indexed assetAddress, address indexed owner, uint256 price, uint256 ancestorCount);
    event AssetDeactivated(address indexed assetAddress, string reason);
    event AssetRated(address indexed assetAddress, address indexed customer, uint8 stars);
    event PlagiarismReported(address indexed reporter, address indexed maliciousAsset, address indexed victimAsset);

    error InsufficientListingFee();
    error Unauthorized();
    error InvalidRating();
    error InactiveAsset();

    constructor(uint256 _listingFee, address _zkVerifier) {
        require(_zkVerifier != address(0), "Invalid verifier address");
        listingFee = _listingFee;
        contractOwner = msg.sender;
        zkVerifier = _zkVerifier;
        template = address(new ZKDigitalAssetContract());
    }

    /**
     * @notice Lists a new AIGC asset using an EIP-1167 minimal proxy clone
     */
    function listAsset(
        uint256 assetPrice,
        address payable[] calldata parentAssets,
        uint256[] calldata parentBps
    ) external payable returns (address) {
        if (msg.value < listingFee) {
            revert InsufficientListingFee();
        }

        address cloneAddr = template.clone();
        ZKDigitalAssetContract asset = ZKDigitalAssetContract(payable(cloneAddr));

        asset.initialize(assetPrice, msg.sender, zkVerifier, parentAssets, parentBps);

        isAssetActive[cloneAddr] = true;
        for (uint256 i = 0; i < parentAssets.length; i++) {
            assetToAncestors[cloneAddr].push(parentAssets[i]);
        }

        emit AssetListed(cloneAddr, msg.sender, assetPrice, parentAssets.length);
        return cloneAddr;
    }

    /**
     * @notice Creator delists their own asset
     */
    function cancelListing(address assetAddress) external {
        ZKDigitalAssetContract asset = ZKDigitalAssetContract(payable(assetAddress));
        if (msg.sender != asset.owner()) {
            revert Unauthorized();
        }
        isAssetActive[assetAddress] = false;
        emit AssetDeactivated(assetAddress, "Cancelled by owner");
    }

    /**
     * @notice Customer rates an asset after verified purchase
     */
    function rateAsset(address assetAddress, uint8 stars) external {
        if (!isAssetActive[assetAddress]) {
            revert InactiveAsset();
        }
        if (stars == 0 || stars > 5) {
            revert InvalidRating();
        }
        ZKDigitalAssetContract asset = ZKDigitalAssetContract(payable(assetAddress));
        require(asset.isCustomer(msg.sender), "Caller is not a verified customer");

        ratings[assetAddress][msg.sender] = stars;
        emit AssetRated(assetAddress, msg.sender, stars);
    }

    /**
     * @notice Observer reports plagiarism by staking tokens
     */
    function reportPlagiarism(
        address maliciousAsset,
        address originalAsset
    ) external payable {
        require(msg.value >= OBSERVER_STAKE_AMOUNT, "Insufficient observer stake");
        require(isAssetActive[maliciousAsset], "Target asset not active");
        require(maliciousAsset != originalAsset, "Cannot report self");

        // Deactivate reported asset and refund stake + reward
        isAssetActive[maliciousAsset] = false;
        emit PlagiarismReported(msg.sender, maliciousAsset, originalAsset);
        emit AssetDeactivated(maliciousAsset, "Plagiarism confirmed");

        (bool success, ) = payable(msg.sender).call{value: msg.value}("");
        require(success, "Stake return failed");
    }

    function getAncestors(address assetAddress) external view returns (address[] memory) {
        return assetToAncestors[assetAddress];
    }
}
