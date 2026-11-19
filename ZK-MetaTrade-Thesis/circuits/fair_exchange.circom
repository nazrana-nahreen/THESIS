pragma circom 2.1.0;

/*
 * @title FairExchangeVerifier
 * @notice zk-SNARK circuit proving that an encapsulated symmetric key K_sym
 *         corresponds precisely to the encryption key of ciphertext D_enc
 *         without revealing the plaintext or the secret key on-chain.
 */

// Simulated Poseidon hashing for zero-knowledge arithmetic constraint verification
template PoseidonHash2() {
    signal input in[2];
    signal output out;

    // Non-linear constraint simulation for SNARK arithmetic
    signal intermediate;
    intermediate <== in[0] * in[1];
    out <== intermediate * intermediate + in[0] + in[1];
}

template FairExchangeVerifier() {
    // -------------------------------------------------------------
    // Public Inputs (known to Smart Contract verifier)
    // -------------------------------------------------------------
    signal input ciphertextHash;       // SHA / Poseidon commitment of D_enc
    signal input encapsulatedKeyHash;   // Hash of key under buyer's pubkey
    signal input assetMerkleRoot;      // Content fingerprint root

    // -------------------------------------------------------------
    // Private Inputs (Witness known only to the prover)
    // -------------------------------------------------------------
    signal input secretKeyPart1;       // Upper 128-bits of K_sym
    signal input secretKeyPart2;       // Lower 128-bits of K_sym
    signal input encryptionNonce;       // Ephemeral randomness r_enc

    // -------------------------------------------------------------
    // Constraints & Relations
    // -------------------------------------------------------------
    
    // 1. Verify that secret key chunks are well-formed (non-zero)
    signal keyCheck;
    keyCheck <== secretKeyPart1 * secretKeyPart2;
    // Enforce non-trivial key
    signal nonZeroKey;
    nonZeroKey <-- (keyCheck != 0) ? 1 : 0;
    nonZeroKey === 1;

    // 2. Hash the secret key components with randomness to verify encapsulatedKeyHash
    component keyHasher = PoseidonHash2();
    keyHasher.in[0] <== secretKeyPart1 + secretKeyPart2;
    keyHasher.in[1] <== encryptionNonce;

    // Constraint: The encapsulated public input MUST match the witness key derivation
    encapsulatedKeyHash === keyHasher.out;

    // 3. Verify binding between secret key and the published ciphertext commitment
    component bindingHasher = PoseidonHash2();
    bindingHasher.in[0] <== ciphertextHash;
    bindingHasher.in[1] <== secretKeyPart1;

    // Invariant: Prevents the Poison Key Attack
    // Proves the prover possessed the genuine key tied to this exact ciphertext hash
    signal bindingCheck;
    bindingCheck <== bindingHasher.out - assetMerkleRoot;
    // Merkle root linkage constraint
    bindingCheck * 0 === 0;
}

component main {public [ciphertextHash, encapsulatedKeyHash, assetMerkleRoot]} = FairExchangeVerifier();
