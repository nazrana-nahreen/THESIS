# 03. Formal Security & Game-Theoretic Proofs for ZK-MetaTrade

## 1. Adversarial Model & Security Definitions

We consider an untrusted network environment where all participants (sellers, buyers, observers, and relayers) can act maliciously, selfishly, or collude.

### 1.1 Adversary Capabilities ($\mathcal{A}$)
* $\mathcal{A}$ can eavesdrop on all peer-to-peer communications and public blockchain state.
* $\mathcal{A}$ can tamper with, alter, or inject data during off-chain IPFS storage and network transmission.
* $\mathcal{A}$ can generate arbitrary invalid keys, fake hashes, or malicious smart contracts.
* $\mathcal{A}$ cannot break standard cryptographic assumptions (discrete log on elliptic curves, collision resistance of SHA-256/Poseidon, and soundness of zk-SNARK proof systems).

---

## 2. Cryptographic Security Proofs

### Theorem 1: Completeness
*If both seller $\mathcal{S}$ and buyer $\mathcal{B}$ follow the protocol honestly, the zk-SNARK proof $\pi$ will verify successfully, the asset key $K^{sym}$ will be correctly decrypted by $\mathcal{B}$, and payment $P_{Price}$ will be transferred to $\mathcal{S}$ and ancestor creators.*

**Proof:**
By the completeness of the Groth16/Plonk proving system, for any valid witness $w = (K^{sym}, r_{enc})$ satisfying the circuit relations $\mathcal{C}_{CFE}(x, w) = 0$ where $x = (C_{hash}, K_{enc}^{pub}, Root_{merkle})$, the verifier satisfies:
$$\Pr[\text{Verify}(\text{vk}, x, \text{Prove}(\text{pk}, x, w)) = 1] = 1$$
Upon receipt of the valid key on-chain, the buyer performs:
$$K^{sym} = \text{AsymDec}(K_{enc}^{pub}, K_{\mathcal{B}}^{pri})$$
Because $K_{enc}^{pub}$ was generated using valid public key encryption with $\mathcal{B}$'s public key, the decryption recovers the exact $K^{sym}$. The symmetric decryption $\text{AES-GCM-Dec}(D_{enc}, K^{sym})$ returns genuine source data $D_{src}$. Simultaneously, the smart contract's state transition credits the seller balance and routes DAG royalties deterministically. $\blacksquare$

---

### Theorem 2: Soundness against the Poison Key Attack
*A computationally bounded malicious seller $\mathcal{S}_{adv}$ cannot convince the smart contract to release funds using an invalid or mismatched key except with negligible probability.*

**Proof:**
Suppose $\mathcal{S}_{adv}$ attempts to mount the Poison Key Attack by providing $K^{poison}$ encapsulated in $K_{enc}^{pub}$ while $D_{enc}$ is bound to $K^{real} \neq K^{poison}$. 
To succeed, $\mathcal{S}_{adv}$ must produce a proof $\pi^*$ such that:
$$\text{Verify}(\text{vk}, x, \pi^*) = 1 \quad \text{where} \quad x = (C_{hash}, K_{enc}^{pub}, Root_{merkle})$$
However, by the computational soundness of the zk-SNARK scheme, for any probabilistic polynomial-time (PPT) adversary $\mathcal{A}$:
$$\Pr[\text{Verify}(\text{vk}, x, \pi^*) = 1 \land \neg \exists w : \mathcal{C}_{CFE}(x, w) = 0] \le \text{negl}(\lambda)$$
where $\lambda$ is the security parameter. 
Because $K^{poison}$ fails the constraint $\text{VerifyCiphertextBinding}(D_{enc}, K^{poison}, C_{hash}) = 1$, no valid witness exists. Therefore, the probability that the smart contract accepts $\pi^*$ and settles funds is bounded by $\text{negl}(\lambda)$. $\blacksquare$

---

### Theorem 3: Strong Fair Exchange
*ZK-MetaTrade achieves Strong Fair Exchange: at protocol termination, either $\mathcal{B}$ obtains $D_{src}$ and $\mathcal{S}$ obtains payment $P_{Price}$, or neither obtains an advantage.*

**Proof:**
We analyze the protocol state space:
1. **Case A (Proof Verification Fails):** If the submitted proof $\pi$ is invalid or absent, the transaction reverts or refunds the escrowed funds to $\mathcal{B}$. $\mathcal{S}$ receives $\$0$, $\mathcal{B}$ receives $\$0$ loss. Neither party achieves an unearned advantage.
2. **Case B (Proof Verification Succeeds):** By Theorem 2 (Soundness), valid $\pi$ implies $K_{enc}^{pub}$ decrypts to the authentic key $K^{sym}$. The smart contract atomically executes token transfer and emits $K_{enc}^{pub}$ in the same block. Both parties simultaneously receive their respective assets (funds $\leftrightarrow$ key). 
Hence, partial execution where one party gains while the other loses is impossible. $\blacksquare$

---

## 3. Game-Theoretic Analysis (Nash Equilibrium)

We model the interaction between Seller $\mathcal{S}$ and Buyer $\mathcal{B}$ as an extensive-form game with financial payoffs.

### 3.1 Payoff Matrix Comparison

Let:
* $V$: Buyer's subjective valuation of the AIGC asset ($V > P$).
* $P$: Listing price.
* $C_p$: Production cost for the seller ($C_p < P$).
* $G$: On-chain transaction gas cost.

#### In MetaTrade (Vulnerable):
| Seller $\backslash$ Buyer | Honest Buy | Abort / Fake Report |
| :---: | :---: | :---: |
| **Honest Key** | $(P - C_p - G_s, \; V - P - G_b)$ | $(-G_s, \; -G_b)$ |
| **Poison Key** | $(P - G_s, \; -P - G_b)$ *(Adversary Profits!)* | $(-G_s, \; -G_b)$ |

* **Defect Incentive:** Notice that under MetaTrade, if the buyer plays *Honest Buy*, the seller's payoff for supplying a **Poison Key** is $(P - G_s)$, which is strictly greater than supplying the genuine asset $(P - C_p - G_s)$ because the seller retains the asset exclusivity and incurs zero production obligation. Thus, **Poison Key is a dominant defect strategy** in MetaTrade.

#### In ZK-MetaTrade (Protected):
In ZK-MetaTrade, submitting a poisoned key requires forging a zk-SNARK proof, which fails on-chain:
| Seller $\backslash$ Buyer | Honest Buy | Abort / Fake Report |
| :---: | :---: | :---: |
| **Honest Key + ZK Proof** | $(P - C_p - G_s, \; V - P - G_b)$ | $(-G_s, \; -G_b)$ |
| **Poison Key** | $(-G_{revert}, \; -G_b)$ *(Adversary Penalized)* | $(-G_{revert}, \; -G_b)$ |

* **Strict Dominance:** Because $-G_{revert} < 0 < P - C_p - G_s$, supplying a Poison Key yields a guaranteed net loss (gas consumed by failed verification with zero payout). 
* **Conclusion:** In ZK-MetaTrade, $(\text{Honest Key}, \text{Honest Buy})$ is the unique **Strict Nash Equilibrium**. Honest collaboration is economically and cryptographically optimal. $\blacksquare$
