import os
import matplotlib
import tempfile

temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = r"g:\gdownloads\ll\ZK-MetaTrade-Thesis\figures"
os.makedirs(output_dir, exist_ok=True)

def plot_fabric_architecture():
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette
    c_org1_border = '#2563EB'
    c_org1_bg = '#EFF6FF'
    c_org2_border = '#059669'
    c_org2_bg = '#ECFDF5'
    c_raft_border = '#DC2626'
    c_raft_bg = '#FEF2F2'
    c_gray_bg = '#F8FAFC'
    c_dark = '#0F172A'

    # Title
    ax.text(50, 97.5, "FIGURE 5. High-Level Enterprise Consortium Architecture (Hyperledger Fabric v2.5)",
            ha='center', va='center', fontsize=13, weight='bold', color=c_dark)
    ax.text(50, 95, "Live Testbed Implementation: 30 Raft Orderers, 2 Organizations, and dam Chaincode v1.3 with _transferMulti",
            ha='center', va='center', fontsize=8.5, color='#475569')

    # =========================================================================
    # 1. EXTERNAL ENTITIES (LEFT SIDE & TOP)
    # =========================================================================
    
    # Buyer Client Box
    rect_buyer = patches.FancyBboxPatch((2, 75), 18, 16, boxstyle="round,pad=0.8", fc='#DBEAFE', ec='#1D4ED8', lw=1.5)
    ax.add_patch(rect_buyer)
    ax.text(11, 87, "Buyer Client", ha='center', weight='bold', fontsize=9, color='#1E40AF')
    ax.text(11, 82.5, "Org1 Admin\n(Metaverse User)", ha='center', fontsize=7.5, color='#1E3A8A')
    ax.text(11, 77.5, "Balance: 850 TKN", ha='center', weight='bold', fontsize=7.5, color='#1D4ED8')

    # Seller Client Box
    rect_seller = patches.FancyBboxPatch((2, 53), 18, 16, boxstyle="round,pad=0.8", fc='#D1FAE5', ec='#047857', lw=1.5)
    ax.add_patch(rect_seller)
    ax.text(11, 65, "Seller Client", ha='center', weight='bold', fontsize=9, color='#065F46')
    ax.text(11, 60.5, "Org2 User1\n(AIGC Creator)", ha='center', fontsize=7.5, color='#064E3B')
    ax.text(11, 55.5, "Balance: 90 TKN", ha='center', weight='bold', fontsize=7.5, color='#047857')

    # Ancestor Model Owner Box
    rect_anc = patches.FancyBboxPatch((2, 31), 18, 16, boxstyle="round,pad=0.8", fc='#FEF3C7', ec='#D97706', lw=1.5)
    ax.add_patch(rect_anc)
    ax.text(11, 43, "Ancestor Owner", ha='center', weight='bold', fontsize=9, color='#B45309')
    ax.text(11, 38.5, "Org2 Admin\n(Base SDXL Trainer)", ha='center', fontsize=7.5, color='#78350F')
    ax.text(11, 33.5, "Balance: 60 TKN", ha='center', weight='bold', fontsize=7.5, color='#B45309')

    # Off-Chain IPFS Decentralized Storage Box
    rect_ipfs = patches.FancyBboxPatch((2, 9), 18, 16, boxstyle="round,pad=0.8", fc='#F3E8FF', ec='#9333EA', lw=1.5)
    ax.add_patch(rect_ipfs)
    ax.text(11, 21, "IPFS Storage", ha='center', weight='bold', fontsize=9, color='#6B21A8')
    ax.text(11, 16, "Encrypted 3D Payload\n($D_{enc}$ Content URI)", ha='center', fontsize=7.5, color='#581C87')
    ax.text(11, 11, "Off-Chain Cluster", ha='center', weight='bold', fontsize=7, color='#7E22CE')

    # =========================================================================
    # 2. REST API & DAPP GATEWAY (CONNECTOR COLUMN)
    # =========================================================================
    rect_gateway = patches.FancyBboxPatch((23, 40), 9, 38, boxstyle="round,pad=0.6", fc='#F1F5F9', ec='#64748B', lw=1.2)
    ax.add_patch(rect_gateway)
    ax.text(27.5, 73, "Web3 DApp\n& Gateway", ha='center', weight='bold', fontsize=8, color='#334155')
    ax.text(27.5, 63, "• Fabric SDK\n• gRPC Stubs\n• TLS Auth\n• Event Hub", ha='center', fontsize=6.8, color='#475569')
    ax.text(27.5, 46, "REST API\nProxy", ha='center', weight='bold', fontsize=7.5, color='#0284C7')

    # Arrows from Clients to Gateway
    ax.annotate("", xy=(23, 72), xytext=(20, 81), arrowprops=dict(arrowstyle="->", color='#1D4ED8', lw=1.2))
    ax.annotate("", xy=(23, 60), xytext=(20, 60), arrowprops=dict(arrowstyle="->", color='#047857', lw=1.2))
    ax.annotate("", xy=(23, 48), xytext=(20, 40), arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.2))

    # =========================================================================
    # 3. CONSORTIUM BLOCKCHAIN NETWORK (BIG DASHED CONTAINER)
    # =========================================================================
    rect_consortium = patches.FancyBboxPatch((35, 6), 63, 86, boxstyle="round,pad=1.2", fc='white', ec='#2563EB', lw=1.8, ls='--')
    ax.add_patch(rect_consortium)
    ax.text(37, 89.5, "Hyperledger Fabric Consortium Network (Channel: 'mychannel')", fontsize=10, weight='bold', color='#1E3A8A')

    # -------------------------------------------------------------------------
    # 3A. COMPANY / ORG 1 (BLUE CONTAINER)
    # -------------------------------------------------------------------------
    rect_org1 = patches.FancyBboxPatch((37, 49), 28, 38, boxstyle="round,pad=0.8", fc=c_org1_bg, ec=c_org1_border, lw=1.5)
    ax.add_patch(rect_org1)
    ax.text(51, 83.5, "Organization 1 (Org1MSP)", ha='center', weight='bold', fontsize=9.5, color='#1E40AF')

    # Peer 0 Org 1
    rect_peer1 = patches.FancyBboxPatch((39, 56), 15, 23, boxstyle="round,pad=0.5", fc='white', ec='#1D4ED8', lw=1.2)
    ax.add_patch(rect_peer1)
    ax.text(46.5, 75, "peer0.org1", ha='center', weight='bold', fontsize=8.5, color='#1E40AF')
    ax.text(46.5, 71, "(Port 7051)", ha='center', fontsize=7, color='#64748B')
    ax.text(46.5, 67, "Endorser &\nAnchor Peer", ha='center', fontsize=6.8, color='#1E293B')

    # State DB (Ledger)
    rect_db1 = patches.FancyBboxPatch((40, 58), 13, 6, boxstyle="round,pad=0.3", fc='#DBEAFE', ec='#1D4ED8', lw=0.8)
    ax.add_patch(rect_db1)
    ax.text(46.5, 61, "State DB (World)", ha='center', weight='bold', fontsize=6.5, color='#1E40AF')

    # MSP & CA for Org1
    rect_msp1 = patches.Circle((59, 72), 3.2, fc='#BFDBFE', ec='#1D4ED8', lw=1)
    ax.add_patch(rect_msp1)
    ax.text(59, 71.5, "MSP", ha='center', va='center', weight='bold', fontsize=7, color='#1E40AF')

    rect_ca1 = patches.Circle((59, 58), 3.2, fc='#FEF08A', ec='#CA8A04', lw=1)
    ax.add_patch(rect_ca1)
    ax.text(59, 57.5, "CA 1", ha='center', va='center', weight='bold', fontsize=7, color='#854D0E')

    # -------------------------------------------------------------------------
    # 3B. COMPANY / ORG 2 (GREEN CONTAINER)
    # -------------------------------------------------------------------------
    rect_org2 = patches.FancyBboxPatch((37, 9), 28, 37, boxstyle="round,pad=0.8", fc=c_org2_bg, ec=c_org2_border, lw=1.5)
    ax.add_patch(rect_org2)
    ax.text(51, 42.5, "Organization 2 (Org2MSP)", ha='center', weight='bold', fontsize=9.5, color='#065F46')

    # Peer 0 Org 2
    rect_peer2 = patches.FancyBboxPatch((39, 15), 15, 23, boxstyle="round,pad=0.5", fc='white', ec='#047857', lw=1.2)
    ax.add_patch(rect_peer2)
    ax.text(46.5, 34, "peer0.org2", ha='center', weight='bold', fontsize=8.5, color='#065F46')
    ax.text(46.5, 30, "(Port 8051)", ha='center', fontsize=7, color='#64748B')
    ax.text(46.5, 26, "Endorser &\nAnchor Peer", ha='center', fontsize=6.8, color='#1E293B')

    # State DB (Ledger)
    rect_db2 = patches.FancyBboxPatch((40, 17), 13, 6, boxstyle="round,pad=0.3", fc='#D1FAE5', ec='#047857', lw=0.8)
    ax.add_patch(rect_db2)
    ax.text(46.5, 20, "State DB (World)", ha='center', weight='bold', fontsize=6.5, color='#065F46')

    # MSP & CA for Org2
    rect_msp2 = patches.Circle((59, 31), 3.2, fc='#A7F3D0', ec='#047857', lw=1)
    ax.add_patch(rect_msp2)
    ax.text(59, 30.5, "MSP", ha='center', va='center', weight='bold', fontsize=7, color='#065F46')

    rect_ca2 = patches.Circle((59, 18), 3.2, fc='#FEF08A', ec='#CA8A04', lw=1)
    ax.add_patch(rect_ca2)
    ax.text(59, 17.5, "CA 2", ha='center', va='center', weight='bold', fontsize=7, color='#854D0E')

    # -------------------------------------------------------------------------
    # 3C. RAFT ORDERING SERVICE (RED CONTAINER IN CENTER / RIGHT)
    # -------------------------------------------------------------------------
    rect_raft = patches.FancyBboxPatch((68, 50), 28, 37, boxstyle="round,pad=0.8", fc=c_raft_bg, ec=c_raft_border, lw=1.5)
    ax.add_patch(rect_raft)
    ax.text(82, 83.5, "Raft Ordering Service (OrdererOrg)", ha='center', weight='bold', fontsize=9, color='#B91C1C')

    # Central Orderer Circle
    circle_ord1 = patches.Circle((82, 69), 6, fc='#FEE2E2', ec='#DC2626', lw=1.5)
    ax.add_patch(circle_ord1)
    ax.text(82, 70, "Raft Leader", ha='center', weight='bold', fontsize=7.5, color='#991B1B')
    ax.text(82, 66.5, "orderer (7050)", ha='center', fontsize=6.5, color='#B91C1C')

    # Surrounding Raft Consensus Nodes (Representing 30 Orderers)
    ax.text(82, 59, "30 Raft Orderer Nodes Cluster\n(orderer, orderer2 ... orderer30)\nBFT Crash-Fault Tolerant Cluster", 
            ha='center', fontsize=6.8, color='#7F1D1D')
    ax.text(82, 52.5, "Consensus Batch Interval: 500ms", ha='center', weight='bold', fontsize=6.8, color='#991B1B')

    # -------------------------------------------------------------------------
    # 3D. DEPLOYED CHAINCODE & AUDIT HIGHLIGHT BOX (BOTTOM RIGHT)
    # -------------------------------------------------------------------------
    rect_cc = patches.FancyBboxPatch((68, 9), 28, 37, boxstyle="round,pad=0.8", fc='#FAF5FF', ec='#7C3AED', lw=1.5)
    ax.add_patch(rect_cc)
    ax.text(82, 42.5, "Deployed Chaincode: dam v1.3", ha='center', weight='bold', fontsize=9.5, color='#6D28D9')
    
    # Chaincode components
    rect_cc_box1 = patches.Rectangle((70, 26), 24, 13, fc='white', ec='#7C3AED', lw=0.8)
    ax.add_patch(rect_cc_box1)
    ax.text(82, 35, "tokenERC20.js (_transferMulti)", ha='center', weight='bold', fontsize=7.2, color='#6D28D9')
    ax.text(82, 30.5, "• Atomic In-Memory Map Routing\n• Resolves Stale Read (RYOW)\n• Insufficient Funds Guard", ha='center', fontsize=6.2, color='#4C1D95')

    rect_cc_box2 = patches.Rectangle((70, 11), 24, 13, fc='white', ec='#7C3AED', lw=0.8)
    ax.add_patch(rect_cc_box2)
    ax.text(82, 20.5, "digital_asset.js (DAM Logic)", ha='center', weight='bold', fontsize=7.2, color='#6D28D9')
    ax.text(82, 16, "• 10% Multi-Parent DAG Royalty\n• Re-registration Lock Guard\n• Root Item ('none') Handling", ha='center', fontsize=6.2, color='#4C1D95')

    # =========================================================================
    # 4. TRANSACTION & CONSENSUS INTERACTION ARROWS
    # =========================================================================
    
    # Gateway to Peers (Endorsement Proposal)
    ax.annotate("", xy=(39, 67), xytext=(32, 67), arrowprops=dict(arrowstyle="->", color='#1D4ED8', lw=1.2))
    ax.text(32, 69, "① Proposal", fontsize=6.5, color='#1D4ED8', weight='bold')

    ax.annotate("", xy=(39, 27), xytext=(32, 46), arrowprops=dict(arrowstyle="->", color='#047857', lw=1.2))
    ax.text(32, 36, "① Proposal", fontsize=6.5, color='#047857', weight='bold')

    # Peers to Orderer (Submit Endorsed Transaction)
    ax.annotate("", xy=(68, 71), xytext=(54, 71), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.2))
    ax.text(56, 73, "② Endorsed Tx", fontsize=6.5, color='#DC2626', weight='bold')

    ax.annotate("", xy=(76, 63), xytext=(54, 27), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.2, ls=':'))

    # Orderer to Peers (Deliver Ordered Blocks)
    ax.annotate("", xy=(54, 65), xytext=(68, 65), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2, ls='--'))
    ax.text(58, 63, "③ Deliver Block", fontsize=6.5, color='#059669', weight='bold')

    ax.annotate("", xy=(54, 23), xytext=(70, 52), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2, ls='--'))
    ax.text(61, 38, "③ Deliver Block", fontsize=6.5, color='#059669', weight='bold')

    # Bottom Banner: Verified Token Conservation
    rect_bar = patches.FancyBboxPatch((2, 1), 96, 4.5, boxstyle="round,pad=0.3", fc='#0F172A', ec='#38BDF8', lw=1)
    ax.add_patch(rect_bar)
    ax.text(50, 3.2, "EMPIRICALLY VERIFIED ON LIVE NETWORK: Buyer (850) + Seller (90) + Ancestor (60) + Escrows (0) = 1000 TOKENS (EXACT CONSERVATION)", 
            ha='center', va='center', weight='bold', fontsize=7.5, color='#38BDF8')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig5_consortium_fabric_architecture.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig5_consortium_fabric_architecture.svg"))
    plt.close()
    print("[+] Fig 5 (Consortium Fabric Architecture) generated successfully.")

if __name__ == "__main__":
    plot_fabric_architecture()
