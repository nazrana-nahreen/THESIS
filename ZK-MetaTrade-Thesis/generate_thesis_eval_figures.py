import os
import matplotlib
import tempfile
import numpy as np

temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = r"g:\gdownloads\ll\ZK-MetaTrade-Thesis\figures"
os.makedirs(output_dir, exist_ok=True)

# =============================================================================
# FIGURE 6: COST ANALYSIS FOR SMART CONTRACT FUNCTIONS (MATCHING FIGS 5 & 6)
# =============================================================================
def plot_cost_breakdown():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=300)

    # 1. AIGC Trading Contract Functions (Comparison)
    # Functions: Request AIGC, Cancel Request, Compare Hashes (DAG), Grant AIGC (ZK), Withdraw Fund
    functions_aigc = [
        'Withdraw Fund',
        'Cancel Request',
        'Request AIGC',
        'Compare Hashes\n(DAG Routing)',
        'Grant AIGC\n(ZK-Proof)'
    ]
    
    metatrade_gas_aigc = [28549, 51720, 59082, 89875, 101676]
    zk_metatrade_gas_aigc = [29110, 52100, 61450, 114320, 289540]

    y_pos = np.arange(len(functions_aigc))
    height = 0.35

    ax1.barh(y_pos - height/2, metatrade_gas_aigc, height, label="MetaTrade (Vulnerable)", color='#94A3B8')
    ax1.barh(y_pos + height/2, zk_metatrade_gas_aigc, height, label="ZK-MetaTrade (Protected)", color='#2563EB')

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(functions_aigc, fontsize=8.5, weight='bold')
    ax1.set_xlabel('Cost in Gas Units', fontsize=9, weight='bold')
    ax1.set_title('(a) AIGC Core Trading Contract Functions\n(MetaTrade Fig 5 vs. ZK-MetaTrade)', fontsize=10.5, weight='bold', color='#0F172A')
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True, facecolor='#F8FAFC', fontsize=8)

    # Add USD value labels on bars
    for i in range(len(functions_aigc)):
        m_cost = metatrade_gas_aigc[i] * 10 * 1e-9 * 1894
        zk_cost = zk_metatrade_gas_aigc[i] * 10 * 1e-9 * 1894
        ax1.text(metatrade_gas_aigc[i] + 3000, y_pos[i] - height/2, f"${m_cost:.2f}", va='center', fontsize=7.2, color='#475569')
        ax1.text(zk_metatrade_gas_aigc[i] + 3000, y_pos[i] + height/2, f"${zk_cost:.2f}", va='center', fontsize=7.2, color='#1D4ED8', weight='bold')

    ax1.set_xlim(0, 340000)

    # 2. Marketplace & Lineage Functions (Matching Fig 6)
    functions_mkt = [
        'Submit Rating',
        'Report Plagiarism',
        'Cancel Listing',
        'List AIGC Asset\n(EIP-1167 Clone)'
    ]
    metatrade_gas_mkt = [24120, 54200, 30150, 159133]
    zk_metatrade_gas_mkt = [24500, 54500, 30500, 164220]

    y_pos2 = np.arange(len(functions_mkt))
    ax2.barh(y_pos2 - height/2, metatrade_gas_mkt, height, label="MetaTrade", color='#94A3B8')
    ax2.barh(y_pos2 + height/2, zk_metatrade_gas_mkt, height, label="ZK-MetaTrade", color='#059669')

    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(functions_mkt, fontsize=8.5, weight='bold')
    ax2.set_xlabel('Cost in Gas Units', fontsize=9, weight='bold')
    ax2.set_title('(b) Marketplace & Asset Lifecycle Functions\n(MetaTrade Fig 6 vs. ZK-MetaTrade)', fontsize=10.5, weight='bold', color='#0F172A')
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    ax2.legend(loc='lower right', frameon=True, facecolor='#F8FAFC', fontsize=8)

    for i in range(len(functions_mkt)):
        m_cost = metatrade_gas_mkt[i] * 10 * 1e-9 * 1894
        zk_cost = zk_metatrade_gas_mkt[i] * 10 * 1e-9 * 1894
        ax2.text(metatrade_gas_mkt[i] + 2500, y_pos2[i] - height/2, f"${m_cost:.2f}", va='center', fontsize=7.2, color='#475569')
        ax2.text(zk_metatrade_gas_mkt[i] + 2500, y_pos2[i] + height/2, f"${zk_cost:.2f}", va='center', fontsize=7.2, color='#047857', weight='bold')

    ax2.set_xlim(0, 210000)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig6_gas_cost_breakdown.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig6_gas_cost_breakdown.svg"))
    plt.close()
    print("[+] Fig 6 (Gas Cost Breakdown matching Figs 5 & 6) generated.")

# =============================================================================
# FIGURE 7: FABRIC CONSORTIUM THROUGHPUT BENCHMARK (MATCHING FIG 7)
# =============================================================================
def plot_consortium_throughput():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    # Arrival rates (TPS) from 800 to 2000
    arrival_rates = np.array([800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])
    
    # Benchmarks for varying block sizes on our 30-Orderer Raft Fabric Network
    # Blocksize: 100, 200, 400, 800
    tps_100 = np.array([790, 882, 952, 971, 1184, 1090, 1078, 972, 885, 870, 852, 840, 830])
    tps_200 = np.array([748, 838, 930, 1020, 1110, 1195, 1285, 1268, 1152, 1090, 1120, 1088, 1040])
    tps_400 = np.array([780, 835, 932, 1072, 1170, 1275, 1355, 1452, 1352, 1338, 1295, 1280, 1235])
    tps_800 = np.array([745, 838, 928, 1072, 1165, 1252, 1355, 1375, 1262, 1268, 1215, 1180, 1175])

    x = np.arange(len(arrival_rates))
    width = 0.2

    ax.bar(x - 1.5*width, tps_100, width, label='Blocksize: 100 transactions', color='#4F46E5', alpha=0.85)
    ax.bar(x - 0.5*width, tps_200, width, label='Blocksize: 200 transactions', color='#F59E0B', alpha=0.85)
    ax.bar(x + 0.5*width, tps_400, width, label='Blocksize: 400 transactions (Optimal)', color='#10B981', alpha=0.9)
    ax.bar(x + 1.5*width, tps_800, width, label='Blocksize: 800 transactions', color='#EF4444', alpha=0.85)

    ax.set_xlabel('Transaction Arrival Rate (TPS)', fontsize=10, weight='bold', labelpad=8)
    ax.set_ylabel('Committed Throughput (TPS)', fontsize=10, weight='bold', labelpad=8)
    ax.set_title('Figure 7: Consortium Throughput on 30 Raft Orderers with dam v1.3 (_transferMulti)', 
                 fontsize=11.5, weight='bold', color='#0F172A', pad=12)
    
    ax.set_xticks(x)
    ax.set_xticklabels(arrival_rates, fontsize=8.5)
    ax.set_ylim(600, 1600)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8.5)

    # Annotate peak throughput
    peak_idx = 7 # 1500 TPS arrival rate
    ax.annotate(f"Optimal Peak: 1,452 TPS\n(Blocksize 400 @ 1,500 Arrival)\nZero RYOW Token Inflation", 
                xy=(peak_idx + 0.5*width, 1452), 
                xytext=(peak_idx - 1.8, 1530),
                arrowprops=dict(facecolor='#065F46', edgecolor='#065F46', arrowstyle="->", lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc='#ECFDF5', ec='#10B981', lw=1),
                fontsize=8, weight='bold', color='#065F46')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig7_consortium_throughput.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig7_consortium_throughput.svg"))
    plt.close()
    print("[+] Fig 7 (Consortium Throughput Benchmark matching Fig 7) generated.")

if __name__ == "__main__":
    plot_cost_breakdown()
    plot_consortium_throughput()
