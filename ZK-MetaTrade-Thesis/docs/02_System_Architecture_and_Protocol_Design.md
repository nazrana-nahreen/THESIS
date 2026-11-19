# 02. ZK-MetaTrade System Architecture & Protocol Specification

## 1. Architectural Overview

**ZK-MetaTrade** is designed to provide provable, trust-free, and asynchronous trading of AI-Generated Content (AIGC) in metaverse environments. It achieves:
1. **Mathematical Fair Exchange:** Powered by a Zero-Knowledge circuit ($\text{zk-SNARK}$) that guarantees the validity of decryption keys before funds settle.
2. **Asynchronous 24/7 Autonomous Settlement:** Utilizing Proxy Re-Encryption (PRE) so sellers upload once, enabling continuous automated delivery without seller interactivity.
3. **Multi-Parent Royalty DAG:** A generalized lineage graph distributing proportional compensation across multi-tier AI models, LoRAs, and control pipelines.

```
+-----------------------------------------------------------------------------------+
|                              ZK-MetaTrade Ecosystem                               |
+-----------------------------------------------------------------------------------+
       |                                                                      |
       v                                                                      v
 [ AIGC Seller ]                                                        [ Customer ]
       |                                                                      |
       | 1. One-time upload (D_enc)                                           | 3. Purchase & Verify
       v                                                                      v
[ Decentralized Storage (IPFS) ]                                    [ ZK-MetaTrade Contracts ]
       ^                                                                      |
       | 2. Re-Encryption / Key Resolution                                    | 4. Atomic Settlement
       +------------------- [ Re-Encryption Network ] <-----------------------+
```

---

## 2. Cryptographic Protocol Specifications

### 2.1 Zero-Knowledge Contingent Fair Exchange (zk-CFE)
To eliminate the Poison Key attack, the seller or re-encryption relayer must submit a zk-SNARK proof $\pi$ along with the encrypted key.

#### Public Inputs:
* $C_{hash}$: Hash commitment of the encrypted asset ($H(D_{enc})$).
* $K_{enc}^{pub}$: The encryption of symmetric key $K^{sym}$ under the buyer's public key $K_{cus}^{pub}$.
* $Root_{merkle}$: Merkle root or fingerprint of the source asset $D_{src}$.

#### Private Inputs (Witness):
* $K^{sym}$: The actual 256-bit symmetric encryption key.
* $r_{enc}$: Randomness/ephemeral key used during public key encryption.

#### Circuit Constraints ($\mathcal{C}_{CFE}$):
1. **Key Derivation & Decryption Consistency:**
   $$\text{VerifyCiphertextBinding}(D_{enc}, K^{sym}, C_{hash}) = 1$$
   The circuit proves that the secret key $K^{sym}$ in the witness correctly generates the commitment $C_{hash}$ when combined with the ciphertext chunk sample.
2. **Asymmetric Key Encapsulation:**
   $$K_{enc}^{pub} \equiv \text{AsymEnc}(K^{sym}, K_{cus}^{pub}, r_{enc})$$
   The circuit proves that the exact same key $K^{sym}$ is encapsulated in $K_{enc}^{pub}$ designated for the buyer.

#### On-Chain Verification:
The smart contract executes:
$$\text{verifyProof}(\pi, [C_{hash}, K_{enc}^{pub}, Root_{merkle}]) \to \{\text{True, False}\}$$
* **Invariant:** If the function returns `True`, it is mathematically impossible for the seller to have provided a mismatched or poisoned key (Soundness property).

---

### 2.2 Asynchronous Trade Flow via Proxy Re-Encryption (PRE)

Instead of requiring the seller to be online for every trade:

1. **One-Time Publishing:**
   * Seller generates master key pair $(pk_S, sk_S)$.
   * Seller encrypts source asset $D_{src}$ under $pk_S \to D_{enc}^{S}$.
   * Seller uploads $D_{enc}^{S}$ to IPFS and registers asset on `DAGMarketplace`.
2. **Buyer Request:**
   * Buyer $\mathcal{B}$ with key pair $(pk_B, sk_B)$ deposits funds into `ZKDigitalAssetContract`.
   * A re-encryption license event is emitted on-chain.
3. **Decentralized Re-encryption:**
   * Using Umbral threshold re-encryption or a secure decentralized key relayer, re-encryption keys $rk_{S \to B}$ transform $D_{enc}^{S} \to D_{enc}^{B}$ without ever revealing plaintext $D_{src}$.
4. **Immediate Download:**
   * Buyer retrieves $D_{enc}^{B}$ and decrypts using $sk_B$.
   * Settlement occurs in a single transaction block.

---

### 2.3 Directed Acyclic Graph (DAG) Multi-Parent Royalty Distribution

Let an AIGC asset $\mathcal{A}$ depend on a set of ancestor assets $\mathcal{P} = \{P_1, P_2, \dots, P_k\}$ with associated royalty shares $\mathbf{w} = [w_1, w_2, \dots, w_k]$ such that:
$$\sum_{i=1}^k w_i \le W_{max} < 100\%$$

When a buyer pays $P_{Price}$ for asset $\mathcal{A}$:
1. **Ancestor Royalties:**
   $$\forall i \in \{1, \dots, k\}, \quad \text{Royalty}(P_i) = \frac{w_i \cdot P_{Price}}{10^4}$$
2. **Direct Seller Proceeds:**
   $$\text{Payout}(\text{Seller}_{\mathcal{A}}) = P_{Price} - \sum_{i=1}^k \text{Royalty}(P_i)$$
3. **Recursive/Multi-Tier Routing:**
   * Each $P_i$ contract receives funds and triggers internal royalty splits to its own ancestor nodes up to depth limit $D_{max}$ (to bound EVM gas execution).

```
                      Purchase Payment ($100)
                                 |
         +-----------------------+-----------------------+
         |                                               |
   Seller Net ($70)                              Royalties Pool ($30)
                                                         |
                                 +-----------------------+-----------------------+
                                 |                                               |
                        Parent 1: SDXL ($15)                            Parent 2: LoRA ($15)
                                 |                                               |
                         Foundation Treasury                             LoRA Model Creator
```

---

## 3. Detailed Algorithmic Workflows

### Algorithm 1: Publishing Asset with Multi-Parent DAG Declaration
```text
Input: price, parentAddresses[], commissionShares[], contentHash, zkParams
Output: Deployed Asset Address A_addr

1: Assert length(parentAddresses) == length(commissionShares)
2: Assert sum(commissionShares) <= MAX_TOTAL_ROYALTY
3: Clone ZKDigitalAsset template via EIP-1167
4: Initialize contract with (price, parentAddresses, commissionShares, contentHash)
5: Register A_addr in DAGMarketplace registry
6: Return A_addr
```

### Algorithm 2: Atomic ZK-Verified Purchase & Settlement
```text
Input: Asset contract A, Proof pi, PublicInputs, msg.value
Output: Success / Abort

1: Assert msg.value >= A.price
2: Verify zk-SNARK proof:
      valid = ZKVerifier.verify(pi, PublicInputs)
3: If valid == False:
      Revert("Invalid ZK Proof: Key and Ciphertext mismatch")
4: Distribute Royalties across all parent contracts in A.parentAddresses[]
5: Credit remaining balance to A.seller
6: Release encrypted key K_enc to buyer
7: Emit AccessSettled(buyer, K_enc)
```
