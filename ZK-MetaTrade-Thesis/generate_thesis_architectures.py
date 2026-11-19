import os
import matplotlib
import tempfile

# Set writable cache directory for Matplotlib on Windows sandbox
temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Publication quality style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = r"g:\gdownloads\ll\ZK-MetaTrade-Thesis\figures"
os.makedirs(output_dir, exist_ok=True)

# =============================================================================
# FIGURE 1: ZK-METATRADE HIGH-LEVEL SYSTEM ARCHITECTURE
# =============================================================================
def plot_figure_1():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette (IEEE Modern Crisp)
    c_blue = '#1E40AF'
    c_blue_bg = '#EFF6FF'
    c_emerald = '#065F46'
    c_emerald_bg = '#ECFDF5'
    c_purple = '#5B21B6'
    c_purple_bg = '#F5F3FF'
    c_amber = '#92400E'
    c_amber_bg = '#FFFBEB'
    c_slate = '#334155'

    # Title & Subtitle
    ax.text(50, 97, "FIGURE 1. High-Level System Architecture and Entity Interaction of ZK-MetaTrade",
            ha='center', va='center', fontsize=12, weight='bold', color='#0F172A')

    # --- ENTITY: Staked Plagiarism Observers (Top) ---
    rect_obs = patches.FancyBboxPatch((32, 82), 36, 11, boxstyle="round,pad=0.8", fc='#FEF2F2', ec='#DC2626', lw=1.5)
    ax.add_patch(rect_obs)
    ax.text(50, 89, "Decentralized Plagiarism Observers (Staked PoP)", ha='center', weight='bold', fontsize=9.5, color='#B91C1C')
    ax.text(50, 84.5, "• Multi-Observer Staking • Perceptual Hash Verification • Bribing-Resistant Voting", ha='center', fontsize=7.5, color='#7F1D1D')

    # Arrow: Observers -> Marketplace
    ax.annotate("", xy=(50, 68), xytext=(50, 82),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.5))
    ax.text(51, 74, "Report Plagiarism\n(Stake-Weighted Quorum)", fontsize=7.5, color='#B91C1C', weight='bold')

    # --- MAIN BOX: ZK-MetaTrade Marketplace DApp & Smart Contracts ---
    rect_dapp = patches.FancyBboxPatch((24, 18), 52, 50, boxstyle="round,pad=1.5", fc='white', ec=c_slate, lw=1.5, ls='--')
    ax.add_patch(rect_dapp)
    ax.text(26, 65, "ZK-MetaTrade Protocol Suite & DApp", fontsize=10, weight='bold', color='#1E293B')

    # Sub-component 1: DAG Marketplace Smart Contract
    rect_sc = patches.FancyBboxPatch((27, 46), 46, 15, boxstyle="round,pad=0.8", fc=c_purple_bg, ec=c_purple, lw=1.5)
    ax.add_patch(rect_sc)
    ax.text(50, 56, "DAG Marketplace & Registry Contract", ha='center', weight='bold', fontsize=9.5, color=c_purple)
    ax.text(50, 50, "• EIP-1167 Factory Clones • Staking Pool • Plagiarism Governance\n• Recursive DAG Multi-Parent Micro-Royalty Router", ha='center', fontsize=7.2, color='#4C1D95')

    # Sub-component 2: Product Clones & Verifier
    rect_prod1 = patches.FancyBboxPatch((27, 22), 14, 18, boxstyle="round,pad=0.5", fc=c_blue_bg, ec=c_blue, lw=1)
    ax.add_patch(rect_prod1)
    ax.text(34, 33, "AIGC Contract:\nProduct 1", ha='center', weight='bold', fontsize=8, color=c_blue)
    ax.text(34, 25, "ZK-Escrow\nSettlement", ha='center', fontsize=7, color='#1E3A8A')

    rect_prod2 = patches.FancyBboxPatch((43, 22), 14, 18, boxstyle="round,pad=0.5", fc=c_blue_bg, ec=c_blue, lw=1)
    ax.add_patch(rect_prod2)
    ax.text(50, 33, "AIGC Contract:\nProduct 2", ha='center', weight='bold', fontsize=8, color=c_blue)
    ax.text(50, 25, "DAG Royalties\n(k-Parents)", ha='center', fontsize=7, color='#1E3A8A')

    rect_verif = patches.FancyBboxPatch((59, 22), 14, 18, boxstyle="round,pad=0.5", fc='#FAF5FF', ec='#7E22CE', lw=1.5)
    ax.add_patch(rect_verif)
    ax.text(66, 33, "zk-CFE Verifier\n(IVerifier)", ha='center', weight='bold', fontsize=8, color='#6B21A8')
    ax.text(66, 25, "Groth16 Pairing\n(alt_bn128)", ha='center', fontsize=7, color='#581C87')

    # Arrows inside DApp: Registry -> Products
    ax.annotate("", xy=(34, 40), xytext=(34, 46), arrowprops=dict(arrowstyle="->", color=c_purple, lw=1.2))
    ax.annotate("", xy=(50, 40), xytext=(50, 46), arrowprops=dict(arrowstyle="->", color=c_purple, lw=1.2))
    ax.annotate("", xy=(66, 40), xytext=(66, 46), arrowprops=dict(arrowstyle="->", color=c_purple, lw=1.2))

    # --- ENTITY: Customer (Left) ---
    rect_cust = patches.FancyBboxPatch((2, 36), 18, 25, boxstyle="round,pad=1", fc=c_emerald_bg, ec=c_emerald, lw=1.5)
    ax.add_patch(rect_cust)
    ax.text(11, 55, "Metaverse\nCustomer", ha='center', weight='bold', fontsize=9.5, color=c_emerald)
    ax.text(11, 44, "• Escrows Funds\n• Submits $pk_B$\n• Verifies Ciphertext\n• Rates Asset", ha='center', fontsize=7.2, color='#064E3B')

    # --- ENTITY: AIGC Seller (Right) ---
    rect_seller = patches.FancyBboxPatch((80, 36), 18, 25, boxstyle="round,pad=1", fc=c_blue_bg, ec=c_blue, lw=1.5)
    ax.add_patch(rect_seller)
    ax.text(89, 55, "AIGC Creator\n/ Seller", ha='center', weight='bold', fontsize=9.5, color=c_blue)
    ax.text(89, 44, "• Synthesizes Content\n• Encrypts Asset ($D_{enc}$)\n• Generates Proof $\\pi$\n• Autonomous PRE", ha='center', fontsize=7.2, color='#1E3A8A')

    # --- ENTITY: Ancestor Model Contributors (Bottom Right) ---
    rect_anc = patches.FancyBboxPatch((80, 5), 18, 22, boxstyle="round,pad=1", fc=c_amber_bg, ec=c_amber, lw=1.5)
    ax.add_patch(rect_anc)
    ax.text(89, 21, "Ancestor Model\nContributors", ha='center', weight='bold', fontsize=9, color=c_amber)
    ax.text(89, 11, "• SDXL Base Foundation\n• Style LoRAs\n• ControlNet Depth Rigs", ha='center', fontsize=7.2, color='#78350F')

    # --- ENTITY: IPFS Storage (Bottom Left) ---
    rect_ipfs = patches.FancyBboxPatch((2, 5), 18, 22, boxstyle="round,pad=1", fc='#FEF9C3', ec='#CA8A04', lw=1.5)
    ax.add_patch(rect_ipfs)
    ax.text(11, 21, "IPFS / Arweave\nDecentralized Store", ha='center', weight='bold', fontsize=9, color='#854D0E')
    ax.text(11, 11, "• Content Addressed\n• Encrypted $D_{enc}$\n• Zero Gas Storage", ha='center', fontsize=7.2, color='#713F12')

    # Connectors & Numbered Protocol Flows
    # 1. Seller initializes product
    ax.annotate("", xy=(76, 32), xytext=(80, 38), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2))
    ax.text(76, 39, "① Initialize AIGC\n& DAG Lineage", fontsize=7.5, color=c_blue, weight='bold')

    # 2. List on marketplace
    ax.annotate("", xy=(73, 53), xytext=(80, 53), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2))
    ax.text(74, 55, "② List on\nMarketplace", fontsize=7.5, color=c_blue, weight='bold')

    # 3. Customer purchase & escrow
    ax.annotate("", xy=(27, 30), xytext=(15, 36), arrowprops=dict(arrowstyle="->", color=c_emerald, lw=1.2))
    ax.text(17, 31, "③ Purchase Asset\n& Escrow Payment", fontsize=7.5, color=c_emerald, weight='bold')

    # 4. Customer rating
    ax.annotate("", xy=(27, 53), xytext=(20, 53), arrowprops=dict(arrowstyle="->", color=c_emerald, lw=1.2))
    ax.text(20, 55, "④ Submit Rating", fontsize=7.5, color=c_emerald, weight='bold')

    # 5. DAG Micro-Royalty Routing (SC -> Ancestors)
    ax.annotate("", xy=(80, 16), xytext=(57, 22), arrowprops=dict(arrowstyle="->", color=c_amber, lw=1.5, ls='--'))
    ax.text(62, 14, "⑤ Automated DAG Micro-Royalties", fontsize=7.5, color=c_amber, weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig1_system_architecture.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig1_system_architecture.svg"))
    plt.close()
    print("[+] Fig 1 generated successfully.")

# =============================================================================
# FIGURE 2: DETAILED TRADING PROCESS & zk-CFE PROTOCOL (CORRESPONDING TO FIG 2)
# =============================================================================
def plot_figure_2():
    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Palette
    c_blue = '#1E3A8A'
    c_blue_bg = '#EFF6FF'
    c_green = '#065F46'
    c_green_bg = '#ECFDF5'
    c_purple = '#5B21B6'
    c_purple_bg = '#F5F3FF'

    # Title
    ax.text(50, 97.5, "FIGURE 2. The Provably Fair AIGC Trading Process with zk-CFE and DAG Settlements",
            ha='center', va='center', fontsize=12, weight='bold', color='#0F172A')

    # Top: IPFS Storage
    rect_ipfs = patches.FancyBboxPatch((40, 84), 22, 9, boxstyle="round,pad=0.8", fc='#FEF9C3', ec='#CA8A04', lw=1.5)
    ax.add_patch(rect_ipfs)
    ax.text(51, 89.5, "IPFS Decentralized Storage", ha='center', weight='bold', fontsize=9, color='#854D0E')
    ax.text(51, 86, "Content-Addressed Encrypted Asset Payload ($D_{enc}$)", ha='center', fontsize=7, color='#713F12')

    # Left: Customer Box
    rect_cust = patches.FancyBboxPatch((2, 14), 25, 68, boxstyle="round,pad=1", fc=c_green_bg, ec=c_green, lw=1.5)
    ax.add_patch(rect_cust)
    ax.text(14.5, 78, "Metaverse Customer (Buyer $\\mathcal{B}$)", ha='center', weight='bold', fontsize=9.5, color=c_green)

    # Customer Sub-boxes
    rect_c1 = patches.Rectangle((4, 60), 21, 14, fc='white', ec=c_green, lw=1)
    ax.add_patch(rect_c1)
    ax.text(14.5, 70, "Encrypted Data ($D_{enc}$)", ha='center', fontsize=7.5, color='#1E293B')
    ax.text(14.5, 63, "Compute $H_c = \\text{SHA-256}(D_{enc})$", ha='center', weight='bold', fontsize=7.5, color=c_green)

    rect_c2 = patches.Rectangle((4, 38), 21, 18, fc='white', ec=c_green, lw=1)
    ax.add_patch(rect_c2)
    ax.text(14.5, 51.5, "Recover Encrypted Key ($K_{enc}^{pub}$)", ha='center', fontsize=7.5, color='#1E293B')
    ax.text(14.5, 46, "Decrypt with Secret Key:\n$K^{sym} = \\text{Dec}_{sk_B}(K_{enc}^{pub})$", ha='center', fontsize=7.5, color='#4338CA')
    ax.text(14.5, 40.5, "Authentic Key Decryption Guaranteed", ha='center', weight='bold', fontsize=7, color='#047857')

    rect_c3 = patches.Rectangle((4, 18), 21, 16, fc='white', ec=c_green, lw=1)
    ax.add_patch(rect_c3)
    ax.text(14.5, 29, "Decrypt Plaintext Content:", ha='center', fontsize=7.5, color='#1E293B')
    ax.text(14.5, 22.5, "$D_{src} = \\text{AES-GCM}(D_{enc}, K^{sym})$\n(Content Integrity: Verified)", ha='center', weight='bold', fontsize=7.5, color='#065F46')

    # Middle: ZK Smart Contract Box
    rect_sc = patches.FancyBboxPatch((35, 14), 31, 68, boxstyle="round,pad=1", fc=c_purple_bg, ec=c_purple, lw=1.5)
    ax.add_patch(rect_sc)
    ax.text(50.5, 78, "ZKDigitalAssetContract.sol", ha='center', weight='bold', fontsize=10, color=c_purple)

    # Smart contract internal logic boxes
    rect_s1 = patches.Rectangle((37, 54), 27, 20, fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_s1)
    ax.text(50.5, 69.5, "zk-CFE Verifier Engine", ha='center', weight='bold', fontsize=8.5, color=c_purple)
    ax.text(50.5, 63, "Checks Groth16 Proof $\\pi = (A,B,C)$:\n$e(A,B) == e(\\alpha,\\beta) \\cdot e(x,\\gamma) \\cdot e(C,\\delta)$", ha='center', fontsize=7.2, color='#4C1D95')
    ax.text(50.5, 56.5, "[Neutralizes Poison Key Attacks]", ha='center', weight='bold', fontsize=7.2, color='#BE185D')

    rect_s2 = patches.Rectangle((37, 34), 27, 16, fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_s2)
    ax.text(50.5, 45, "Ciphertext Hash Comparison", ha='center', weight='bold', fontsize=8.5, color=c_purple)
    ax.text(50.5, 38, "Verifies: $H_c == H$\n(Ensures identical payload download)", ha='center', fontsize=7.2, color='#475569')

    rect_s3 = patches.Rectangle((37, 18), 27, 12, fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_s3)
    ax.text(50.5, 25, "Multi-Party Settlement Engine", ha='center', weight='bold', fontsize=8.5, color=c_purple)
    ax.text(50.5, 20.5, "• Atomic DAG Royalties ($P_1..P_k$)\n• Net Seller Payout ($P_{net}$)", ha='center', fontsize=7, color='#047857')

    # Right: AIGC Seller Box
    rect_seller = patches.FancyBboxPatch((74, 38), 24, 44, boxstyle="round,pad=1", fc=c_blue_bg, ec=c_blue, lw=1.5)
    ax.add_patch(rect_seller)
    ax.text(86, 78, "AIGC Seller / PRE KMS", ha='center', weight='bold', fontsize=9.5, color=c_blue)

    rect_sel1 = patches.Rectangle((76, 62), 20, 12, fc='white', ec=c_blue, lw=1)
    ax.add_patch(rect_sel1)
    ax.text(86, 70, "1. Extract Buyer $pk_B$", ha='center', fontsize=7.5, color='#1E293B')
    ax.text(86, 64.5, "From Escrow Transaction", ha='center', fontsize=7, color='#64748B')

    rect_sel2 = patches.Rectangle((76, 42), 20, 16, fc='white', ec=c_blue, lw=1)
    ax.add_patch(rect_sel2)
    ax.text(86, 53, "2. Generate ZK-Proof $\\pi$", ha='center', weight='bold', fontsize=7.5, color=c_blue)
    ax.text(86, 45.5, "Proof of Key Binding &\nCorrect Encapsulation\nvia Circom Circuit", ha='center', fontsize=7, color='#475569')

    # Bottom Right: ZK Encryption & Proof Unit Box
    rect_unit = patches.FancyBboxPatch((74, 5), 24, 28, boxstyle="round,pad=1", fc='#F8FAFC', ec='#475569', lw=1.2)
    ax.add_patch(rect_unit)
    ax.text(86, 29, "zk-CFE Cryptographic Unit", ha='center', weight='bold', fontsize=8.5, color='#0F172A')
    ax.text(86, 22, "• Plaintext Sample $D_{sample}$\n• Symmetric Key $K^{sym}$\n• AES-256-GCM + Poseidon\n• Circom Proof Witness $(K, r)$", ha='center', fontsize=7, color='#334155')
    ax.text(86, 9.5, "Outputs: $\\pi, K_{enc}^{pub}, C_{hash}$", ha='center', weight='bold', fontsize=7.5, color='#4338CA')

    # Step-by-Step Flow Arrows with Labels
    # 1.1 Customer submits buying request + escrow fund
    ax.annotate("", xy=(35, 68), xytext=(27, 68), arrowprops=dict(arrowstyle="->", color=c_green, lw=1.2))
    ax.text(28, 70, "1. Submit Escrow & $pk_B$", fontsize=7, color=c_green, weight='bold')

    # 2. Seller uploads to IPFS
    ax.annotate("", xy=(62, 88), xytext=(86, 82), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2))
    ax.text(76, 86, "2. Upload $D_{enc}$", fontsize=7, color=c_blue, weight='bold')

    # 3. Seller gets IPFS URI
    ax.annotate("", xy=(86, 82), xytext=(62, 85), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2, ls=':'))

    # 4. Seller calls grantAccess with Proof + Encrypted Key
    ax.annotate("", xy=(66, 62), xytext=(74, 62), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2))
    ax.text(67, 64, "4. Post Proof $\\pi$, $K_{enc}^{pub}$, $H$", fontsize=7, color=c_blue, weight='bold')

    # 5. Customer downloads IPFS data
    ax.annotate("", xy=(14.5, 74), xytext=(40, 86), arrowprops=dict(arrowstyle="->", color='#CA8A04', lw=1.2))
    ax.text(20, 83, "5. Download $D_{enc}$", fontsize=7, color='#A16207', weight='bold')

    # 6. Customer calls compareHashes
    ax.annotate("", xy=(35, 42), xytext=(27, 42), arrowprops=dict(arrowstyle="->", color=c_green, lw=1.2))
    ax.text(28, 44, "6. compareHashes($H_c$)", fontsize=7, color=c_green, weight='bold')

    # 7. Settlement & Key release
    ax.annotate("", xy=(27, 49), xytext=(35, 49), arrowprops=dict(arrowstyle="->", color=c_purple, lw=1.2))
    ax.text(28, 51, "7. Grant Verified $K_{enc}^{pub}$", fontsize=7, color=c_purple, weight='bold')

    # 8. Payout to Seller
    ax.annotate("", xy=(74, 40), xytext=(66, 26), arrowprops=dict(arrowstyle="->", color=c_purple, lw=1.2))
    ax.text(68, 32, "8. Net Payout $P_{net}$", fontsize=7, color=c_purple, weight='bold')

    # 9. Internal recovery arrow in Customer
    ax.annotate("", xy=(14.5, 34), xytext=(14.5, 38), arrowprops=dict(arrowstyle="->", color=c_green, lw=1))
    ax.annotate("", xy=(14.5, 14), xytext=(14.5, 18), arrowprops=dict(arrowstyle="->", color=c_green, lw=1))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig2_trading_protocol_process.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig2_trading_protocol_process.svg"))
    plt.close()
    print("[+] Fig 2 generated successfully.")

# =============================================================================
# FIGURE 3: INHERITABLE MULTI-PARENT DAG ARCHITECTURE (CORRESPONDING TO FIG 3)
# =============================================================================
def plot_figure_3():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Palette
    c_blue = '#1E3A8A'
    c_blue_bg = '#EFF6FF'
    c_purple = '#5B21B6'
    c_purple_bg = '#F5F3FF'
    c_emerald = '#065F46'
    c_emerald_bg = '#ECFDF5'
    c_amber = '#92400E'
    c_amber_bg = '#FFFBEB'

    # Title
    ax.text(50, 97.5, "FIGURE 3. Inheritable Content Development Architecture with Multi-Parent DAG Lineage",
            ha='center', va='center', fontsize=12, weight='bold', color='#0F172A')

    # Top: DAG Marketplace Registry Contract
    rect_top = patches.FancyBboxPatch((30, 85), 40, 10, boxstyle="round,pad=0.8", fc=c_purple_bg, ec=c_purple, lw=1.5)
    ax.add_patch(rect_top)
    ax.text(50, 91.5, "DAG Marketplace Smart Contract", ha='center', weight='bold', fontsize=9.5, color=c_purple)
    ax.text(50, 87, "Contract Address: 0x5FbDB2315678... | Listed Clones: [0x4758, 0x9c78, 0x8753, 0x7469]", ha='center', fontsize=7, color='#4C1D95')

    # Line from Marketplace to Root Nodes
    ax.plot([50, 50], [85, 78], color=c_purple, lw=1.5)
    ax.plot([25, 75], [78, 78], color=c_purple, lw=1.5)
    ax.plot([25, 25], [78, 74], color=c_purple, lw=1.5)
    ax.plot([75, 75], [78, 74], color=c_purple, lw=1.5)

    # --- LEVEL 1: FOUNDATION / ROOT MODELS (PARENTS = NONE) ---
    # Node 1: SDXL 1.0 Foundation Model
    rect_r1 = patches.FancyBboxPatch((12, 57), 26, 17, boxstyle="round,pad=0.6", fc='#F1F5F9', ec='#475569', lw=1.2)
    ax.add_patch(rect_r1)
    ax.text(25, 70, "Root AIGC Contract: SDXL 1.0", ha='center', weight='bold', fontsize=8.5, color='#0F172A')
    ax.text(25, 64.5, "Base Foundation Diffusion Model\nParents: None | Commission: 10%\nContract Address: 0x47582A...", ha='center', fontsize=7, color='#334155')

    # Node 2: Midjourney / ControlNet Base Rig
    rect_r2 = patches.FancyBboxPatch((62, 57), 26, 17, boxstyle="round,pad=0.6", fc='#F1F5F9', ec='#475569', lw=1.2)
    ax.add_patch(rect_r2)
    ax.text(75, 70, "Root AIGC Contract: ControlNet", ha='center', weight='bold', fontsize=8.5, color='#0F172A')
    ax.text(75, 64.5, "Structural Edge/Depth Rig Model\nParents: None | Commission: 5%\nContract Address: 0x9c78D1...", ha='center', fontsize=7, color='#334155')

    # --- LEVEL 2: DERIVED ADAPTERS & FINE-TUNED MODELS (MULTI-PARENT LINKAGES) ---
    # Node 3: Cyberpunk Style LoRA (Child of SDXL)
    rect_c1 = patches.FancyBboxPatch((3, 31), 28, 17, boxstyle="round,pad=0.6", fc=c_blue_bg, ec=c_blue, lw=1.2)
    ax.add_patch(rect_c1)
    ax.text(17, 44, "LoRA Adapter: Cyberpunk Style", ha='center', weight='bold', fontsize=8, color=c_blue)
    ax.text(17, 38.5, "Styled Weights | Commission: 10%\nAncestors: [0x47582A (SDXL)]\nContract Address: 0x12235B...", ha='center', fontsize=6.8, color='#1E3A8A')

    # Node 4: Futuristic Car Rig (Child of ControlNet)
    rect_c2 = patches.FancyBboxPatch((36, 31), 28, 17, boxstyle="round,pad=0.6", fc=c_emerald_bg, ec=c_emerald, lw=1.2)
    ax.add_patch(rect_c2)
    ax.text(50, 44, "Chassis Rig: Neo-Aerocar", ha='center', weight='bold', fontsize=8, color=c_emerald)
    ax.text(50, 38.5, "3D Mesh Geometry | Commission: 8%\nAncestors: [0x9c78D1 (ControlNet)]\nContract Address: 0x87535C...", ha='center', fontsize=6.8, color='#064E3B')

    # Node 5: Textual Prompt Workflow (Child of SDXL)
    rect_c3 = patches.FancyBboxPatch((69, 31), 28, 17, boxstyle="round,pad=0.6", fc=c_amber_bg, ec=c_amber, lw=1.2)
    ax.add_patch(rect_c3)
    ax.text(83, 44, "Prompt Rig: Octane Render Spec", ha='center', weight='bold', fontsize=8, color=c_amber)
    ax.text(83, 38.5, "Prompt Pipeline | Commission: 4%\nAncestors: [0x47582A (SDXL)]\nContract Address: 0x68453D...", ha='center', fontsize=6.8, color='#78350F')

    # Connectors from Level 1 to Level 2
    ax.annotate("", xy=(17, 48), xytext=(22, 57), arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.2))
    ax.annotate("", xy=(50, 48), xytext=(70, 57), arrowprops=dict(arrowstyle="->", color=c_emerald, lw=1.2))
    ax.annotate("", xy=(83, 48), xytext=(32, 57), arrowprops=dict(arrowstyle="->", color=c_amber, lw=1.2, ls='--'))

    # --- LEVEL 3: MULTI-PARENT COMPOSITE PRODUCT (THE DAG CONVERGENCE) ---
    # Node 6: The Final Metaverse 3D Asset (Aerocar Royal)
    rect_final = patches.FancyBboxPatch((24, 4), 52, 19, boxstyle="round,pad=0.8", fc='#FAF5FF', ec='#7C3AED', lw=1.8)
    ax.add_patch(rect_final)
    ax.text(50, 19, "Final 3D Asset Contract: SKT Cyberpunk Aerocar Royal", ha='center', weight='bold', fontsize=9.5, color='#6D28D9')
    ax.text(50, 13.5, "Multi-Parent DAG Lineage: [0x4758 (SDXL 10%), 0x1223 (LoRA 10%), 0x8753 (Mesh 8%)]\nContract Address: 0x74698E... | Price: 1.0 ETH (or 100 Tokens)", ha='center', fontsize=7.2, color='#4C1D95')
    ax.text(50, 7.5, "Atomic Distribution: 28% Total Ancestor Micro-Royalties | 72% Net Creator Payout", ha='center', weight='bold', fontsize=7.5, color='#047857')

    # Multi-Parent Arrows converging into Final Asset
    ax.annotate("", xy=(36, 23), xytext=(20, 31), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))
    ax.text(23, 27, "10% Royalty", fontsize=6.8, color='#1D4ED8', weight='bold')

    ax.annotate("", xy=(50, 23), xytext=(50, 31), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5))
    ax.text(51, 27, "8% Royalty", fontsize=6.8, color='#047857', weight='bold')

    ax.annotate("", xy=(64, 23), xytext=(80, 31), arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.5))
    ax.text(73, 27, "4% Royalty", fontsize=6.8, color='#B45309', weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig3_multi_parent_dag_royalties.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig3_multi_parent_dag_royalties.svg"))
    plt.close()
    print("[+] Fig 3 generated successfully.")

if __name__ == "__main__":
    plot_figure_1()
    plot_figure_2()
    plot_figure_3()
    print("[SUCCESS] All 3 publication-grade thesis architectures generated in:", output_dir)
