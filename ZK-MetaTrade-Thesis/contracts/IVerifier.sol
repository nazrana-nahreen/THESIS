// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IVerifier
 * @notice Cryptographic interface for the Zero-Knowledge SNARK verifier
 */
interface IVerifier {
    /**
     * @notice Verifies a Groth16 / Plonk zk-SNARK proof
     * @param a Proof parameter A (G1 point)
     * @param b Proof parameter B (G2 point)
     * @param c Proof parameter C (G1 point)
     * @param input Public inputs: [ciphertextHash, encapsulatedKeyHash, merkleRoot]
     * @return True if the proof is cryptographically sound and valid, false otherwise
     */
    function verifyProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[3] memory input
    ) external view returns (bool);
}
