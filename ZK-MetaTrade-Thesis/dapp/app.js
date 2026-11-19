// =============================================================================
// ZK-MetaTrade Interactive DApp & Protocol Simulator
// =============================================================================

// Initial State
const state = {
  activeTab: 'marketplace',
  network: 'ethereum', // 'ethereum' or 'fabric'
  connectedAccount: 'buyer',
  accounts: {
    buyer: { name: 'Buyer (Bob)', address: '0x70997970C51812dc3A010C7d01b50e0d17dc79C8', balanceEth: 10.0, balanceTokens: 1000 },
    seller: { name: 'Seller (Alice)', address: '0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC', balanceEth: 0.0, balanceTokens: 0 },
    parent1: { name: 'SDXL Foundation (Stability)', address: '0x90F79bf6EB2c4f870365E785982E1f101E93b906', balanceEth: 0.0, balanceTokens: 0 },
    parent2: { name: 'Cyberpunk LoRA (Community)', address: '0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65', balanceEth: 0.0, balanceTokens: 0 },
    parent3: { name: 'ControlNet Depth (Stanford)', address: '0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc', balanceEth: 0.0, balanceTokens: 0 },
    escrow: { name: 'Smart Contract Escrow', address: '0x5FbDB2315678afecb367f032d93F642f64180aa3', balanceEth: 0.0, balanceTokens: 0 }
  },
  assets: [
    {
      id: 'cyber_car_3d',
      title: 'Cyberpunk Aerocar 3D Asset',
      category: 'Metaverse Vehicle / GLTF',
      priceEth: 1.0,
      priceTokens: 100,
      image: 'https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=800&auto=format&fit=crop&q=60',
      description: 'Fully rigged 3D flying vehicle asset generated with SDXL fine-tuned on Cyberpunk LoRA and constrained via ControlNet Depth.',
      ancestors: [
        { name: 'SDXL 1.0 Foundation', rate: 10, payoutEth: 0.1, payoutTokens: 10, role: 'Base Diffusion Model' },
        { name: 'Cyberpunk Style LoRA', rate: 10, payoutEth: 0.1, payoutTokens: 10, role: 'Fine-tuned Style Weights' },
        { name: 'ControlNet Depth Map', rate: 5, payoutEth: 0.05, payoutTokens: 5, role: 'Structural Guidance Rig' }
      ],
      sellerShare: 75,
      sellerPayoutEth: 0.75,
      sellerPayoutTokens: 75
    },
    {
      id: 'neural_avatar_v2',
      title: 'Neural Metaverse Avatar V2',
      category: 'Interactive NPC / VRM',
      priceEth: 0.5,
      priceTokens: 50,
      image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=60',
      description: 'Dynamic humanoid avatar with procedural facial blendshapes and neural voice pipeline.',
      ancestors: [
        { name: 'SDXL 1.0 Foundation', rate: 10, payoutEth: 0.05, payoutTokens: 5, role: 'Base Diffusion Model' },
        { name: 'Avatar Blendshape LoRA', rate: 15, payoutEth: 0.075, payoutTokens: 7.5, role: 'Rigging Weights' }
      ],
      sellerShare: 75,
      sellerPayoutEth: 0.375,
      sellerPayoutTokens: 37.5
    },
    {
      id: 'holo_katana',
      title: 'Quantum Holo-Katana',
      category: 'Metaverse Weapon (Root Asset)',
      priceEth: 0.8,
      priceTokens: 50,
      image: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=800&auto=format&fit=crop&q=60',
      description: 'Original hand-modeled and standalone synthesized weapon asset (Zero parent dependencies).',
      ancestors: [],
      sellerShare: 100,
      sellerPayoutEth: 0.8,
      sellerPayoutTokens: 50
    }
  ],
  logs: []
};

// Logger function
function addLog(type, message, details = null) {
  const time = new Date().toLocaleTimeString();
  state.logs.unshift({ time, type, message, details });
  if (state.logs.length > 50) state.logs.pop();
  renderLogs();
}

// Render balances
function updateBalancesUI() {
  document.getElementById('buyerBalEth').textContent = state.accounts.buyer.balanceEth.toFixed(2) + ' ETH';
  document.getElementById('buyerBalTokens').textContent = state.accounts.buyer.balanceTokens.toFixed(0) + ' TKN';
  
  document.getElementById('sellerBalEth').textContent = state.accounts.seller.balanceEth.toFixed(2) + ' ETH';
  document.getElementById('sellerBalTokens').textContent = state.accounts.seller.balanceTokens.toFixed(0) + ' TKN';
  
  document.getElementById('parent1BalEth').textContent = state.accounts.parent1.balanceEth.toFixed(2) + ' ETH';
  document.getElementById('parent2BalEth').textContent = state.accounts.parent2.balanceEth.toFixed(2) + ' ETH';
  document.getElementById('parent3BalEth').textContent = state.accounts.parent3.balanceEth.toFixed(2) + ' ETH';
  
  document.getElementById('escrowBalEth').textContent = state.accounts.escrow.balanceEth.toFixed(2) + ' ETH';
  document.getElementById('escrowBalTokens').textContent = state.accounts.escrow.balanceTokens.toFixed(0) + ' TKN';
}

// Render Logs
function renderLogs() {
  const container = document.getElementById('logStream');
  if (!container) return;
  container.innerHTML = state.logs.map(log => {
    let badgeClass = 'bg-blue-900/50 text-blue-300 border-blue-500/30';
    if (log.type === 'error') badgeClass = 'bg-rose-900/50 text-rose-300 border-rose-500/30';
    if (log.type === 'success') badgeClass = 'bg-emerald-900/50 text-emerald-300 border-emerald-500/30';
    if (log.type === 'warn') badgeClass = 'bg-amber-900/50 text-amber-300 border-amber-500/30';
    if (log.type === 'zk') badgeClass = 'bg-purple-900/50 text-purple-300 border-purple-500/30';

    return `
      <div class="p-2.5 rounded-lg border bg-black/40 text-xs font-mono mb-2 transition-all">
        <div class="flex items-center justify-between mb-1">
          <span class="px-2 py-0.5 rounded text-[10px] uppercase font-bold border ${badgeClass}">
            ${log.type}
          </span>
          <span class="text-gray-500 text-[10px]">${log.time}</span>
        </div>
        <div class="text-gray-200">${log.message}</div>
        ${log.details ? `<pre class="mt-1.5 p-1.5 rounded bg-gray-950 text-gray-400 text-[10px] overflow-x-auto border border-gray-800">${log.details}</pre>` : ''}
      </div>
    `;
  }).join('');
}

// Reset Balances
function resetSimulationState() {
  state.accounts.buyer.balanceEth = 10.0;
  state.accounts.buyer.balanceTokens = 1000;
  state.accounts.seller.balanceEth = 0.0;
  state.accounts.seller.balanceTokens = 0;
  state.accounts.parent1.balanceEth = 0.0;
  state.accounts.parent1.balanceTokens = 0;
  state.accounts.parent2.balanceEth = 0.0;
  state.accounts.parent2.balanceTokens = 0;
  state.accounts.parent3.balanceEth = 0.0;
  state.accounts.parent3.balanceTokens = 0;
  state.accounts.escrow.balanceEth = 0.0;
  state.accounts.escrow.balanceTokens = 0;
  updateBalancesUI();
  addLog('info', 'Simulation state reinitialized to original genesis balances.');
}

// =============================================================================
// Attack & Defense Interactive Simulator
// =============================================================================

// 1. Poison Key Attack against MetaTrade (Broken Protocol)
async function simulatePoisonKeyMetaTrade() {
  const btn = document.getElementById('btnRunPoisonAttack');
  if (btn) btn.disabled = true;
  
  addLog('warn', '>>> INITIATING POISON KEY ATTACK ON METATRADE (IEEE ACCESS 2024)...');
  
  // Step 1: Buyer deposits
  state.accounts.buyer.balanceEth -= 1.0;
  state.accounts.escrow.balanceEth += 1.0;
  updateBalancesUI();
  addLog('info', '[Step 1] Buyer Bob deposits 1.0 ETH into MetaTrade escrow via registerRequest().');
  await new Promise(r => setTimeout(r, 800));

  // Step 2: Malicious seller crafts bogus key
  const kReal = '7d4a8a2fed276e24e354b7287f240b5093d86de446d5786afd71eb9042883794';
  const kPoison = '1c8d12c8a8813c2bf964df08cac5ffb464db1e82891fddddf416a169334f51e3';
  const cipherHash = 'a4f4a92c0c8f43cca7429acc69556586b7dbb8e02b8a4cbe216afe0f463d84be';
  
  addLog('warn', '[Step 2] Malicious Seller Alice crafts POISON KEY:', `K_real:   ${kReal}\nK_poison: ${kPoison}\nCiphertext SHA-256 (H): ${cipherHash}`);
  await new Promise(r => setTimeout(r, 900));

  // Step 3: grantAccess with genuine hash but poisoned key
  addLog('info', '[Step 3] Seller Alice calls grantAccess(bob, H, Enc(K_poison), ipfs://QmAttack)');
  await new Promise(r => setTimeout(r, 800));

  // Step 4: Buyer downloads and verifies hash
  addLog('info', '[Step 4] Buyer Bob downloads D_enc from IPFS, computes H_c = SHA256(D_enc).');
  addLog('info', '[Step 4] Verification: H_c == H -> TRUE! Buyer calls compareHashes(H_c).');
  await new Promise(r => setTimeout(r, 900));

  // Step 5: MetaTrade releases payment
  state.accounts.escrow.balanceEth -= 1.0;
  state.accounts.seller.balanceEth += 1.0;
  updateBalancesUI();
  addLog('warn', '[Step 5] MetaTrade Smart Contract transfers 1.0 ETH to Seller Alice! (Escrow = 0)');
  await new Promise(r => setTimeout(r, 900));

  // Step 6: Decryption Fails Irrevocably!
  addLog('error', '[CRITICAL FAILURE] Buyer Bob retrieves key, attempts AES-256-GCM decryption:');
  addLog('error', 'EXCEPTION: [ERR_CRYPTO_OPERATION_FAILED]: Ciphertext authentication failed / corrupted plaintext.');
  addLog('error', '>>> RESULT: Alice extracted 1.0 ETH with 0 asset delivered! MetaTrade Strong Fair Exchange VIOLATED!');

  // Show visual alert modal/banner
  document.getElementById('attackResultBanner').classList.remove('hidden');
  document.getElementById('attackResultBanner').innerHTML = `
    <div class="p-4 rounded-xl bg-rose-950/80 border border-rose-500/50 text-rose-200">
      <div class="flex items-center gap-3 mb-2 font-bold text-sm">
        <i class="fa-solid fa-triangle-exclamation text-rose-400 text-lg"></i>
        <span>VULNERABILITY CONFIRMED: Poison Key Attack Succeeded</span>
      </div>
      <p class="text-xs text-rose-300/90 leading-relaxed mb-2">
        In MetaTrade's <code>DigitalAssetContract.sol</code>, the contract only checks <code>H_c == H</code>. Because it cannot verify if the key actually decrypts the ciphertext, seller extracted 1.0 ETH using a bogus key. <strong>Buyer's 1.0 ETH is permanently lost with zero recourse.</strong>
      </p>
      <div class="text-[11px] font-mono text-rose-400 bg-black/50 p-2 rounded border border-rose-900/50">
        Seller Profit: +1.0 ETH | Buyer Loss: -1.0 ETH | Plaintext Recovered: FALSE
      </div>
    </div>
  `;

  if (btn) btn.disabled = false;
}

// 2. ZK-MetaTrade Defense (zk-CFE)
async function simulateZKDefense() {
  const btn = document.getElementById('btnRunZKDefense');
  if (btn) btn.disabled = true;

  addLog('zk', '>>> TESTING ZK-METATRADE ZERO-KNOWLEDGE CONTINGENT FAIR EXCHANGE (zk-CFE)...');

  // Step 1: Buyer deposits
  state.accounts.buyer.balanceEth -= 1.0;
  state.accounts.escrow.balanceEth += 1.0;
  updateBalancesUI();
  addLog('info', '[Step 1] Buyer Bob deposits 1.0 ETH into ZKDigitalAssetContract escrow.');
  await new Promise(r => setTimeout(r, 800));

  // Step 2: Malicious seller submits poison key with forged proof
  addLog('warn', '[Step 2] Malicious Seller Alice attempts to submit Poison Key K_poison...');
  addLog('zk', '[Step 2] Synthesizing Circom CFE Proof constraints: (Key Well-formedness, Encapsulation, Binding)');
  await new Promise(r => setTimeout(r, 1000));

  // Step 3: On-Chain Pairing Verifier
  addLog('zk', '[Step 3] Smart contract executes IVerifier(verifier).verifyProof(A, B, C, publicSignals)...');
  await new Promise(r => setTimeout(r, 1000));

  // Step 4: Verification FAILS! Transaction Reverts!
  addLog('error', '[TRANSACTION REVERTED] On-Chain Verifier (ecPairing) returned false!');
  addLog('success', '[DEFENSE SUCCESS] Smart Contract Reverted: "ZKMetaTrade: Invalid ZK proof - Poison Key detected!"');
  
  // Refund to Buyer
  state.accounts.escrow.balanceEth -= 1.0;
  state.accounts.buyer.balanceEth += 1.0;
  updateBalancesUI();
  addLog('success', '>>> RESULT: Buyer funds remain 100% SAFE in escrow/refunded! Seller penalized with revert gas!');

  // Show visual alert
  document.getElementById('defenseResultBanner').classList.remove('hidden');
  document.getElementById('defenseResultBanner').innerHTML = `
    <div class="p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/50 text-emerald-200">
      <div class="flex items-center gap-3 mb-2 font-bold text-sm">
        <i class="fa-solid fa-shield-halved text-emerald-400 text-lg"></i>
        <span>CRYPTOGRAPHIC DEFENSE VERIFIED: Poison Key Attack Blocked</span>
      </div>
      <p class="text-xs text-emerald-300/90 leading-relaxed mb-2">
        ZK-MetaTrade requires a zk-SNARK proof $\\pi$ proving that $K^{sym}$ decrypts $D_{enc}$ and encapsulates under buyer's public key. By the <strong>Knowledge Soundness of Groth16</strong>, the malicious seller cannot forge a valid proof. The transaction reverts atomically.
      </p>
      <div class="text-[11px] font-mono text-emerald-400 bg-black/50 p-2 rounded border border-emerald-900/50">
        Attack Blocked: TRUE | Buyer Fund Stolen: 0 ETH | Strict Nash Equilibrium: ENFORCED
      </div>
    </div>
  `;

  if (btn) btn.disabled = false;
}

// 3. Honest Trade & DAG Multi-Parent Royalty Settlement
async function simulateHonestDAGTrade(assetId) {
  const asset = state.assets.find(a => a.id === assetId);
  if (!asset) return;

  const btn = document.getElementById(`btnBuy_${assetId}`);
  if (btn) btn.disabled = true;

  addLog('info', `>>> EXECUTING HONEST ATOMIC TRADE: "${asset.title}"`);
  
  // Step 1: Buyer Escrow
  state.accounts.buyer.balanceEth -= asset.priceEth;
  state.accounts.escrow.balanceEth += asset.priceEth;
  updateBalancesUI();
  addLog('info', `[Step 1] Buyer Bob escrows ${asset.priceEth} ETH for asset "${asset.title}".`);
  await new Promise(r => setTimeout(r, 700));

  // Step 2: Honest Seller generates valid ZK-SNARK Proof
  addLog('zk', '[Step 2] Seller Alice generates genuine Groth16 zk-SNARK proof of key-ciphertext binding.');
  await new Promise(r => setTimeout(r, 800));

  // Step 3: Verification on-chain
  addLog('zk', '[Step 3] Smart contract validates pairing: e(A, B) == e(α, β) · e(x, γ) · e(C, δ) -> TRUE.');
  await new Promise(r => setTimeout(r, 800));

  // Step 4: DAG Multi-Parent Royalty Distribution
  addLog('info', '[Step 4] DAG Marketplace executes atomic multi-parent revenue routing:');
  state.accounts.escrow.balanceEth -= asset.priceEth;

  if (asset.ancestors.length > 0) {
    asset.ancestors.forEach((anc, idx) => {
      const parentAcc = state.accounts[`parent${idx + 1}`];
      if (parentAcc) {
        parentAcc.balanceEth += anc.payoutEth;
        addLog('success', `  ↳ [DAG Royalty] Sent ${anc.payoutEth} ETH (${anc.rate}%) to Ancestor ${parentAcc.name}`);
      }
    });
  }

  // Seller net payout
  state.accounts.seller.balanceEth += asset.sellerPayoutEth;
  addLog('success', `  ↳ [Seller Payout] Sent net ${asset.sellerPayoutEth} ETH (${asset.sellerShare}%) to Creator Alice.`);
  updateBalancesUI();

  // Decryption success
  addLog('success', `[SUCCESS] Buyer Bob decrypts AIGC payload: "${asset.id.toUpperCase()}_AUTHENTIC_DATA"`);
  addLog('success', `>>> Strong Fair Exchange Satisfied! Token balance conserved exactly.`);

  // Confetti celebration
  if (typeof confetti === 'function') {
    confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
  }

  // Show modal success
  showSuccessModal(asset);

  if (btn) btn.disabled = false;
}

function showSuccessModal(asset) {
  const modal = document.getElementById('tradeSuccessModal');
  const details = document.getElementById('modalTradeDetails');
  if (!modal || !details) return;

  details.innerHTML = `
    <div class="space-y-3 text-xs">
      <div class="flex justify-between border-b border-gray-800 pb-2">
        <span class="text-gray-400">Purchased Asset:</span>
        <span class="font-bold text-cyan-400">${asset.title}</span>
      </div>
      <div class="flex justify-between border-b border-gray-800 pb-2">
        <span class="text-gray-400">Total Settlement:</span>
        <span class="font-bold text-white">${asset.priceEth} ETH</span>
      </div>
      <div class="space-y-1.5 pt-1">
        <div class="text-[11px] font-bold text-purple-400">DAG Ancestor Payouts:</div>
        ${asset.ancestors.map(a => `
          <div class="flex justify-between text-[11px] text-gray-300 pl-2">
            <span>• ${a.name} (${a.rate}%):</span>
            <span class="text-emerald-400 font-mono">+${a.payoutEth} ETH</span>
          </div>
        `).join('')}
        <div class="flex justify-between text-[11px] text-gray-300 pl-2 pt-1 font-bold">
          <span>• Creator / Seller Alice (${asset.sellerShare}%):</span>
          <span class="text-emerald-400 font-mono">+${asset.sellerPayoutEth} ETH</span>
        </div>
      </div>
    </div>
  `;
  modal.classList.remove('hidden');
}

function closeModal() {
  const modal = document.getElementById('tradeSuccessModal');
  if (modal) modal.classList.add('hidden');
}

// Switch navigation tabs
function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.tab-btn').forEach(el => {
    el.classList.remove('border-cyan-500', 'text-cyan-400', 'bg-cyan-950/30');
    el.classList.add('border-transparent', 'text-gray-400');
  });

  const targetTab = document.getElementById(`tab_${tabId}`);
  const targetBtn = document.getElementById(`btnTab_${tabId}`);
  if (targetTab) targetTab.classList.remove('hidden');
  if (targetBtn) {
    targetBtn.classList.remove('border-transparent', 'text-gray-400');
    targetBtn.classList.add('border-cyan-500', 'text-cyan-400', 'bg-cyan-950/30');
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  updateBalancesUI();
  addLog('info', 'ZK-MetaTrade DApp Initialized. Connected to Web3 & Hyperledger Fabric simulation.');
});
