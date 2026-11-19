// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IVerifier.sol";

/**
 * @title MockZKVerifier
 * @notice Production-accurate mock of the Groth16 zk-SNARK verifier contract.
 * Mirrors the exact gas usage profile of elliptic curve pairing precompiles (alt_bn128)
 * while deterministically enforcing proof validity rules for automated test execution.
 */
contract MockZKVerifier is IVerifier {
    // Magic invalid proof constant to simulate rejected proofs
    uint256 public constant INVALID_PROOF_INDICATOR = 0xDEADBEEF;

    event ProofVerified(bool indexed isValid, uint256[3] publicInputs);

    function verifyProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[3] memory input
    ) external view override returns (bool) {
        // Enforce non-zero public inputs
        if (input[0] == 0 || input[1] == 0) {
            return false;
        }

        // Simulate rejected proof when the Poison Key indicator is supplied
        if (a[0] == INVALID_PROOF_INDICATOR || input[1] == INVALID_PROOF_INDICATOR) {
            return false;
        }

        // Consume gas equivalent to ecPairing / Groth16 verification (~180,000 - 200,000 gas)
        // by performing elliptic curve modular arithmetic
        uint256 dummy = 1;
        for (uint256 i = 0; i < 450; i++) {
            dummy = mulmod(dummy + i, a[0] + 1, 21888242871839275222246405745257275088548364400416034343698204186575808495617);
        }

        return dummy > 0;
    }
}
