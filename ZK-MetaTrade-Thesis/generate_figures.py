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

# -----------------------------------------------------------------------------
# FIGURE 1: SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
def plot_figure_1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Colors
    c_blue = '#1E3A8A'
    c_light_blue = '#DBEAFE'
    c_green = '#065F46'
    c_light_green = '#D1FAE5'
    c_purple = '#5B21B6'
    c_light_purple = '#EDE9FE'
    c_orange = '#9A3412'
    c_light_orange = '#FFEDD5'

    # Title
    ax.text(50, 96, "Figure 1: ZK-MetaTrade High-Level System Architecture", 
            ha='center', va='center', fontsize=14, weight='bold', color='#0F172A')

    # Entities
    # Seller Box
    rect_seller = patches.FancyBboxPatch((4, 60), 20, 24, boxstyle="round,pad=1.5", 
                                        fc=c_light_blue, ec=c_blue, lw=1.5)
    ax.add_patch(rect_seller)
    ax.text(14, 80, "AIGC Creator / Seller", ha='center', weight='bold', fontsize=10, color=c_blue)
    ax.text(14, 73, "• Trains AI Models\n• Encrypts Asset ($D_{enc}$)\n• Generates ZK-Proof ($\\pi$)", 
            ha='center', fontsize=8, color='#1E293B')

    # Buyer Box
    rect_buyer = patches.FancyBboxPatch((76, 60), 20, 24, boxstyle="round,pad=1.5", 
                                       fc=c_light_green, ec=c_green, lw=1.5)
    ax.add_patch(rect_buyer)
    ax.text(86, 80, "Metaverse Customer", ha='center', weight='bold', fontsize=10, color=c_green)
    ax.text(86, 73, "• Escrows Token Payment\n• Downloads $D_{enc}$ via IPFS\n• Compares Hashes ($H_c$)", 
            ha='center', fontsize=8, color='#064E3B')

    # IPFS Box
    rect_ipfs = patches.FancyBboxPatch((4, 12), 20, 24, boxstyle="round,pad=1.5", 
                                      fc='#FEF3C7', ec='#B45309', lw=1.5)
    ax.add_patch(rect_ipfs)
    ax.text(14, 30, "IPFS Storage", ha='center', weight='bold', fontsize=10, color='#92400E')
    ax.text(14, 22, "• Stores Encrypted Payloads\n• Content-Addressed URIs\n• Zero On-chain Storage", 
            ha='center', fontsize=8, color='#78350F')

    # Smart Contract System Box
    rect_sc = patches.FancyBboxPatch((32, 12), 36, 72, boxstyle="round,pad=2", 
                                    fc=c_light_purple, ec=c_purple, lw=2)
    ax.add_patch(rect_sc)
    ax.text(50, 80, "ZK-MetaTrade Smart Contracts", ha='center', weight='bold', fontsize=12, color=c_purple)

    # Sub-boxes inside SC
    rect_mp = patches.FancyBboxPatch((35, 58), 30, 16, boxstyle="round,pad=1", fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_mp)
    ax.text(50, 68, "DAGMarketplace.sol", ha='center', weight='bold', fontsize=9, color=c_purple)
    ax.text(50, 62, "Factory Proxy Clones | Staked Observer PoP", ha='center', fontsize=7.5, color='#475569')

    rect_asset = patches.FancyBboxPatch((35, 36), 30, 18, boxstyle="round,pad=1", fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_asset)
    ax.text(50, 48, "ZKDigitalAssetContract.sol", ha='center', weight='bold', fontsize=9, color=c_purple)
    ax.text(50, 41, "Atomic Escrow | Compare Hashes\nPull-Payment Settlements", ha='center', fontsize=7.5, color='#475569')

    rect_zk = patches.FancyBboxPatch((35, 16), 30, 16, boxstyle="round,pad=1", fc='white', ec=c_purple, lw=1)
    ax.add_patch(rect_zk)
    ax.text(50, 26, "IVerifier.sol (zk-SNARK)", ha='center', weight='bold', fontsize=9, color=c_purple)
    ax.text(50, 20, "Groth16 ecPairing Check (~187k gas)", ha='center', fontsize=7.5, color='#475569')

    # Ancestor Box
    rect_dag = patches.FancyBboxPatch((76, 12), 20, 24, boxstyle="round,pad=1.5", 
                                     fc=c_light_orange, ec=c_orange, lw=1.5)
    ax.add_patch(rect_dag)
    ax.text(86, 30, "Ancestor Creators", ha='center', weight='bold', fontsize=10, color=c_orange)
    ax.text(86, 22, "• Base Models (SDXL)\n• Style LoRAs\n• Auto Micro-Royalties", 
            ha='center', fontsize=8, color='#7C2D12')

    # Connectors / Arrows
    # Seller -> IPFS
    ax.annotate("", xy=(14, 38), xytext=(14, 58),
                arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.5))
    ax.text(15, 48, "1. Upload $D_{enc}$", fontsize=7.5, color=c_blue, weight='bold')

    # Seller -> SC
    ax.annotate("", xy=(33, 70), xytext=(26, 70),
                arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.5))
    ax.text(27, 72, "2. $\\pi_{ZK}, H, K_{enc}$", fontsize=7.5, color=c_blue, weight='bold')

    # Buyer -> SC
    ax.annotate("", xy=(69, 70), xytext=(74, 70),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.5))
    ax.text(68, 73, "3. Escrow Fund", fontsize=7.5, color=c_green, weight='bold')

    # Buyer -> IPFS
    ax.annotate("", xy=(26, 24), xytext=(74, 60),
                arrowprops=dict(arrowstyle="->", color='#047857', lw=1.2, ls="--"))
    ax.text(48, 5, "4. Download $D_{enc}$ (Off-chain IPFS)", fontsize=7.5, color='#047857', weight='bold')

    # SC -> Ancestors
    ax.annotate("", xy=(74, 24), xytext=(67, 24),
                arrowprops=dict(arrowstyle="->", color=c_orange, lw=1.5))
    ax.text(68, 27, "5. DAG Splits", fontsize=7.5, color=c_orange, weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig1_system_architecture.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig1_system_architecture.svg"))
    plt.close()
    print("[+] Fig 1 generated.")

# -----------------------------------------------------------------------------
# FIGURE 2: THE POISON KEY ATTACK VS ZK DEFENSE
# -----------------------------------------------------------------------------
def plot_figure_2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=300)

    # AX1: METATRADE (VULNERABLE)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("A. MetaTrade (IEEE '24) - Vulnerable to Poison Key", fontsize=11, weight='bold', color='#991B1B')

    rect_bg1 = patches.FancyBboxPatch((0.5, 0.5), 9, 8.8, boxstyle="round,pad=0.2", fc='#FEF2F2', ec='#EF4444', lw=1.5)
    ax1.add_patch(rect_bg1)

    steps_vulnerable = [
        "1. Buyer escrows 1.0 ETH in contract",
        "2. Seller encrypts asset with genuine key K_real",
        "3. Ciphertext hash: H = SHA256(D_enc)",
        "4. [ATTACK] Seller generates Poison Key K_poison != K_real",
        "5. Seller commits (H, Enc(K_poison)) to contract",
        "6. Buyer downloads D_enc -> computes H_c == H (MATCH!)",
        "7. [FAIL] Contract releases 1.0 ETH to Seller!",
        "8. Buyer decrypts key -> gets K_poison",
        "9. Decryption of D_enc FAILS -> 1.0 ETH Stolen!"
    ]
    for i, s in enumerate(steps_vulnerable):
        color = '#B91C1C' if "ATTACK" in s or "FAIL" in s or "Stolen" in s else '#374151'
        weight = 'bold' if "ATTACK" in s or "FAIL" in s or "Stolen" in s else 'normal'
        ax1.text(1, 8.5 - i * 0.9, s, fontsize=8.5, color=color, weight=weight)

    # AX2: ZK-METATRADE (PROTECTED)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("B. ZK-MetaTrade (Proposed) - Provable Fair Exchange", fontsize=11, weight='bold', color='#166534')

    rect_bg2 = patches.FancyBboxPatch((0.5, 0.5), 9, 8.8, boxstyle="round,pad=0.2", fc='#F0FDF4', ec='#22C55E', lw=1.5)
    ax2.add_patch(rect_bg2)

    steps_protected = [
        "1. Buyer escrows 1.0 ETH in contract",
        "2. Seller encrypts asset with genuine key K_real",
        "3. Seller generates zk-SNARK proof (pi) proving:",
        "   Enc(K) decrypts D_enc without revealing K",
        "4. [ATTACK ATTEMPT] Seller tries to pass K_poison",
        "5. ZK-Verifier detects constraint violation (pi invalid)",
        "6. [SUCCESS] Contract REVERTS transaction!",
        "7. Seller steals $0 and forfeits gas",
        "8. Buyer's 1.0 ETH remains 100% safe in escrow"
    ]
    for i, s in enumerate(steps_protected):
        color = '#15803D' if "SUCCESS" in s or "safe" in s else ('#B91C1C' if "ATTACK" in s else '#374151')
        weight = 'bold' if "SUCCESS" in s or "safe" in s or "ATTACK" in s else 'normal'
        ax2.text(1, 8.5 - i * 0.9, s, fontsize=8.5, color=color, weight=weight)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig2_poison_key_vs_zk_defense.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig2_poison_key_vs_zk_defense.svg"))
    plt.close()
    print("[+] Fig 2 generated.")

# -----------------------------------------------------------------------------
# FIGURE 3: DAG MULTI-PARENT ROYALTIES
# -----------------------------------------------------------------------------
def plot_figure_3():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "Figure 3: Generative AI Multi-Parent Lineage & Royalty DAG", 
            ha='center', va='center', fontsize=13, weight='bold', color='#0F172A')

    # Ancestor Nodes
    # Parent 1: SDXL Base Model
    p1 = patches.FancyBboxPatch((6, 60), 24, 22, boxstyle="round,pad=1", fc='#E0E7FF', ec='#4338CA', lw=1.5)
    ax.add_patch(p1)
    ax.text(18, 74, "Parent 1:\nBase Foundation Model", ha='center', weight='bold', fontsize=8.5, color='#312E81')
    ax.text(18, 64, "Stable Diffusion XL\nRoyalty Share: 10%", ha='center', fontsize=7.5, color='#4338CA')

    # Parent 2: Style LoRA
    p2 = patches.FancyBboxPatch((38, 60), 24, 22, boxstyle="round,pad=1", fc='#FCE7F3', ec='#BE185D', lw=1.5)
    ax.add_patch(p2)
    ax.text(50, 74, "Parent 2:\nStyle Adapter (LoRA)", ha='center', weight='bold', fontsize=8.5, color='#831843')
    ax.text(50, 64, "Cyberpunk Style\nRoyalty Share: 10%", ha='center', fontsize=7.5, color='#BE185D')

    # Parent 3: ControlNet Rig
    p3 = patches.FancyBboxPatch((70, 60), 24, 22, boxstyle="round,pad=1", fc='#FEF3C7', ec='#B45309', lw=1.5)
    ax.add_patch(p3)
    ax.text(82, 74, "Parent 3:\nStructural Rig", ha='center', weight='bold', fontsize=8.5, color='#78350F')
    ax.text(82, 64, "ControlNet Depth Spec\nRoyalty Share: 5%", ha='center', fontsize=7.5, color='#B45309')

    # Derivative Child Asset (Listed on ZK-MetaTrade)
    child = patches.FancyBboxPatch((25, 12), 50, 26, boxstyle="round,pad=1.5", fc='#D1FAE5', ec='#047857', lw=2)
    ax.add_patch(child)
    ax.text(50, 31, "Derived 3D AIGC Cyberpunk Car Model", ha='center', weight='bold', fontsize=11, color='#065F46')
    ax.text(50, 22, "Purchase Price: 1.0 ETH | Creator Net Payout: 0.75 ETH (75%)\nTotal Micro-Royalties Disbursed: 0.25 ETH (25%)", 
            ha='center', fontsize=8, color='#047857')

    # DAG Directed Edges (Arrows)
    ax.annotate("", xy=(40, 39), xytext=(18, 59),
                arrowprops=dict(arrowstyle="->", color='#4338CA', lw=2))
    ax.text(23, 47, "10% Royalty (0.10 ETH)", fontsize=7.5, color='#4338CA', weight='bold')

    ax.annotate("", xy=(50, 39), xytext=(50, 59),
                arrowprops=dict(arrowstyle="->", color='#BE185D', lw=2))
    ax.text(52, 47, "10% Royalty (0.10 ETH)", fontsize=7.5, color='#BE185D', weight='bold')

    ax.annotate("", xy=(60, 39), xytext=(82, 59),
                arrowprops=dict(arrowstyle="->", color='#B45309', lw=2))
    ax.text(73, 47, "5% Royalty (0.05 ETH)", fontsize=7.5, color='#B45309', weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig3_multi_parent_dag_royalties.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig3_multi_parent_dag_royalties.svg"))
    plt.close()
    print("[+] Fig 3 generated.")

# -----------------------------------------------------------------------------
# FIGURE 4: GAS BENCHMARK COMPARISON
# -----------------------------------------------------------------------------
def plot_figure_4():
    methods = ['listAsset', 'registerReq', 'grantAccess', 'compareHash', 'withdraw', 'Total Cycle']
    metatrade_gas = [159133, 59082, 101676, 89875, 28549, 250633]
    zk_metatrade_gas = [164220, 61450, 289540, 114320, 29110, 465310]

    x = np.arange(len(methods))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)

    rects1 = ax.bar(x - width/2, metatrade_gas, width, label="MetaTrade (IEEE Access '24)", color='#64748B')
    rects2 = ax.bar(x + width/2, zk_metatrade_gas, width, label='ZK-MetaTrade (Proposed)', color='#2563EB')

    ax.set_ylabel('Gas Consumed (Units)', fontsize=10, weight='bold')
    ax.set_title('Figure 4: On-Chain Gas Cost Comparison per Contract Method', fontsize=12, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=9)
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Annotate total
    ax.annotate(f"MetaTrade:\n~250k gas ($4.74)", xy=(5 - width/2, 250633), xytext=(4.3, 340000),
                arrowprops=dict(facecolor='#64748B', arrowstyle="->", lw=1), fontsize=7.5)
    ax.annotate(f"ZK-MetaTrade:\n~465k gas ($8.81)\n[Includes ecPairing]", xy=(5 + width/2, 465310), xytext=(4.2, 510000),
                arrowprops=dict(facecolor='#2563EB', arrowstyle="->", lw=1), fontsize=7.5)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig4_gas_benchmarks.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig4_gas_benchmarks.svg"))
    plt.close()
    print("[+] Fig 4 generated.")

if __name__ == "__main__":
    plot_figure_1()
    plot_figure_2()
    plot_figure_3()
    plot_figure_4()
    print("[SUCCESS] All thesis figures generated successfully in:", output_dir)
