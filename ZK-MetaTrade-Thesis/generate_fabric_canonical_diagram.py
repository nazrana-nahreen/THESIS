import os
import matplotlib
import tempfile
import numpy as np

temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon, PathPatch
from matplotlib.path import Path

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = r"g:\gdownloads\ll\ZK-MetaTrade-Thesis\figures"
os.makedirs(output_dir, exist_ok=True)

def draw_ledger_flag(ax, x, y, w, h, color='#2563EB', text="L1"):
    """Draws a stylized wavy ledger flag like the official Hyperledger Fabric docs."""
    # Path with a subtle wave at the bottom
    verts = [
        (x, y),
        (x + w, y),
        (x + w, y - h*0.8),
        (x + w*0.75, y - h*1.0),
        (x + w*0.25, y - h*0.7),
        (x, y - h*0.9),
        (x, y)
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor=color, edgecolor='#0F172A', lw=1.2)
    ax.add_patch(patch)
    ax.text(x + w/2, y - h*0.45, text, ha='center', va='center', fontsize=7.5, weight='bold', color='white')

def draw_chaincode_badge(ax, x, y, w, h, color='#3B82F6', text="S1"):
    """Draws a small chaincode badge on top of a peer."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", fc=color, ec='#0F172A', lw=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7.5, weight='bold', color='white')

def draw_endorsement_triangle(ax, x, y, w, h, color='#8B5CF6', text="R1"):
    """Draws a triangular endorsement policy badge on top of chaincode package."""
    pts = [[x, y], [x + w/2, y + h], [x + w, y]]
    tri = patches.Polygon(pts, closed=True, fc=color, ec='#0F172A', lw=1.1)
    ax.add_patch(tri)
    ax.text(x + w/2, y + h*0.35, text, ha='center', va='center', fontsize=6.8, weight='bold', color='white')

def generate_canonical_fabric_architecture():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette matching official Hyperledger documentation
    c_org1 = '#A855F7'      # Purple (Org 1 - Buyer / Metaverse)
    c_org2 = '#64748B'      # Slate Gray (Org 2 - Seller / Creator Studio)
    c_org3 = '#F59E0B'      # Amber / Orange (Org 3 - Base Model Trainers)
    c_orderer = '#10B981'   # Green (Orderer Node)
    c_channel1 = '#2563EB'  # Blue (C1: 'mychannel' - AIGC Trading)
    c_channel2 = '#DC2626'  # Red (C2: 'auditchannel' - Royalties & Escrow)
    c_bg_container = '#E2E8F0' # Soft slate container bg

    # Title
    ax.text(50, 97.5, "Hyperledger Fabric Canonical Network Architecture for ZK-MetaTrade",
            ha='center', va='center', fontsize=13, weight='bold', color='#0F172A')
    ax.text(50, 95.0, "Consortium Topology: Channels, Peers, 30-Orderer Raft Cluster, Chaincodes & MSP/CAs (IBM/Linux Foundation Standard)",
            ha='center', va='center', fontsize=8.5, color='#475569')

    # =========================================================================
    # 1. MAIN CONSORTIUM CONTAINER (ROUNDED BLUE/GRAY BOX ON RIGHT)
    # =========================================================================
    main_box = FancyBboxPatch((24, 4), 74, 88, boxstyle="round,pad=1.5", fc='#EEF2F6', ec='#1E293B', lw=2.0)
    ax.add_patch(main_box)
    ax.text(26, 89.5, "ZK-MetaTrade Consortium Network Boundary", fontsize=9.5, weight='bold', color='#1E293B')

    # =========================================================================
    # 2. LEFT SIDE: APPLICATIONS (A1, A2, A3) & CAs (CA0, CA1, CA2, CA3)
    # =========================================================================
    
    # Application A1 (Buyer Bob - Metaverse App, Org1)
    a1 = FancyBboxPatch((3, 72), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org1, ec='#0F172A', lw=1.4)
    ax.add_patch(a1)
    ax.text(5.75, 75.25, "A1", ha='center', va='center', fontsize=9.5, weight='bold', color='white')
    ax.text(5.75, 70.0, "Buyer App\n(Org1)", ha='center', fontsize=6.5, weight='bold', color='#6B21A8')

    # Application A2 (Seller Alice - Creator Studio, Org2)
    a2 = FancyBboxPatch((9.5, 72), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org2, ec='#0F172A', lw=1.4)
    ax.add_patch(a2)
    ax.text(12.25, 75.25, "A2", ha='center', va='center', fontsize=9.5, weight='bold', color='white')
    ax.text(12.25, 70.0, "Seller App\n(Org2)", ha='center', fontsize=6.5, weight='bold', color='#334155')

    # Application A3 (Model Foundation - Base Trainers, Org3)
    a3 = FancyBboxPatch((16, 72), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org3, ec='#0F172A', lw=1.4)
    ax.add_patch(a3)
    ax.text(18.75, 75.25, "A3", ha='center', va='center', fontsize=9.5, weight='bold', color='white')
    ax.text(18.75, 70.0, "Trainer App\n(Org3)", ha='center', fontsize=6.5, weight='bold', color='#B45309')

    # Certificate Authorities (Bottom Left)
    # CA0 (OrdererOrg CA)
    ca0 = FancyBboxPatch((3, 20), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_orderer, ec='#0F172A', lw=1.4)
    ax.add_patch(ca0)
    ax.text(5.75, 23.25, "CA0", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(5.75, 17.5, "Orderer CA", ha='center', fontsize=6.2, color='#065F46')

    # CA1 (Org1 CA)
    ca1 = FancyBboxPatch((3, 8), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org1, ec='#0F172A', lw=1.4)
    ax.add_patch(ca1)
    ax.text(5.75, 11.25, "CA1", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(5.75, 5.5, "Org1 CA", ha='center', fontsize=6.2, color='#6B21A8')

    # CA2 (Org2 CA)
    ca2 = FancyBboxPatch((9.5, 8), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org2, ec='#0F172A', lw=1.4)
    ax.add_patch(ca2)
    ax.text(12.25, 11.25, "CA2", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(12.25, 5.5, "Org2 CA", ha='center', fontsize=6.2, color='#334155')

    # CA3 (Org3 CA)
    ca3 = FancyBboxPatch((16, 8), 5.5, 6.5, boxstyle="round,pad=0.3", fc=c_org3, ec='#0F172A', lw=1.4)
    ax.add_patch(ca3)
    ax.text(18.75, 11.25, "CA3", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(18.75, 5.5, "Org3 CA", ha='center', fontsize=6.2, color='#B45309')

    # =========================================================================
    # 3. CHANNELS INSIDE CONSORTIUM (HORIZONTAL ELLIPSES)
    # =========================================================================
    # Channel 1: C1 ('mychannel' - Main Trading Channel)
    c1_ellipse = Ellipse((58, 48), 52, 9, fc='#DBEAFE', ec=c_channel1, lw=2.2)
    ax.add_patch(c1_ellipse)
    ax.text(58, 48, "C1  ('mychannel' - AIGC Trading & Asset Registry Channel)", 
            ha='center', va='center', fontsize=8.5, weight='bold', color='#1E40AF')

    # Channel 2: C2 ('auditchannel' - Royalty Settlement & Escrow Channel)
    c2_ellipse = Ellipse((64, 32), 48, 8, fc='#FEE2E2', ec=c_channel2, lw=2.0)
    ax.add_patch(c2_ellipse)
    ax.text(64, 32, "C2  ('auditchannel' - DAG Royalty & Token Settlement Channel)", 
            ha='center', va='center', fontsize=8.0, weight='bold', color='#991B1B')

    # =========================================================================
    # 4. PEERS (P1, P2, P3) CONNECTED TO CHANNELS
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # PEER P1 (Org1 - peer0.org1, Purple)
    # -------------------------------------------------------------------------
    p1_box = FancyBboxPatch((38, 68), 7, 7, boxstyle="round,pad=0.2", fc=c_org1, ec='#0F172A', lw=1.5)
    ax.add_patch(p1_box)
    ax.text(41.5, 71.5, "P1", ha='center', va='center', fontsize=11, weight='bold', color='white')
    ax.text(41.5, 76.5, "peer0.org1", ha='center', fontsize=7, weight='bold', color='#6B21A8')

    # P1 Chaincode badge (S5: digital_asset)
    draw_chaincode_badge(ax, 34, 73, 3.2, 3.2, color='#3B82F6', text="S1")
    ax.text(32, 74.5, "dam.js", ha='right', va='center', fontsize=6.2, color='#1E40AF', weight='bold')

    # P1 Ledger Flag (L1: mychannel ledger)
    draw_ledger_flag(ax, 34, 69, 3.5, 4.5, color=c_channel1, text="L1")

    # P1 Connection Line to C1
    ax.plot([41.5, 41.5], [68, 52.5], color=c_channel1, lw=2.2)

    # -------------------------------------------------------------------------
    # PEER P2 (Org2 - peer0.org2, Gray / Endorser on both C1 & C2)
    # -------------------------------------------------------------------------
    p2_box = FancyBboxPatch((54, 68), 7, 7, boxstyle="round,pad=0.2", fc=c_org2, ec='#0F172A', lw=1.5)
    ax.add_patch(p2_box)
    ax.text(57.5, 71.5, "P2", ha='center', va='center', fontsize=11, weight='bold', color='white')
    ax.text(57.5, 76.5, "peer0.org2", ha='center', fontsize=7, weight='bold', color='#334155')

    # P2 Chaincodes: S1 (blue) and S2 (_transferMulti, red)
    draw_chaincode_badge(ax, 50, 73, 3.2, 3.2, color='#3B82F6', text="S1")
    draw_chaincode_badge(ax, 61.8, 73, 3.2, 3.2, color='#EF4444', text="S2")
    ax.text(66, 74.5, "erc20.js\n(_transferMulti)", ha='left', va='center', fontsize=5.8, color='#B91C1C', weight='bold')

    # P2 Ledgers: L1 (blue flag) and L2 (red flag)
    draw_ledger_flag(ax, 50, 69, 3.5, 4.5, color=c_channel1, text="L1")
    draw_ledger_flag(ax, 61.8, 69, 3.5, 4.5, color=c_channel2, text="L2")

    # P2 Connection Lines: to C1 (blue) and through to C2 (red)
    ax.plot([57.5, 57.5], [68, 52.5], color=c_channel1, lw=2.2)
    ax.plot([57.5, 57.5], [43.5, 36.0], color=c_channel2, lw=2.2)

    # -------------------------------------------------------------------------
    # PEER P3 (Org3 - peer0.org3 / Trainer Anchor Peer, Amber)
    # -------------------------------------------------------------------------
    p3_box = FancyBboxPatch((82, 68), 7, 7, boxstyle="round,pad=0.2", fc=c_org3, ec='#0F172A', lw=1.5)
    ax.add_patch(p3_box)
    ax.text(85.5, 71.5, "P3", ha='center', va='center', fontsize=11, weight='bold', color='white')
    ax.text(85.5, 76.5, "peer0.org3", ha='center', fontsize=7, weight='bold', color='#B45309')

    # P3 Chaincodes: S1 and S2
    draw_chaincode_badge(ax, 78, 73, 3.2, 3.2, color='#3B82F6', text="S1")
    draw_chaincode_badge(ax, 89.8, 73, 3.2, 3.2, color='#EF4444', text="S2")

    # P3 Ledgers: L1 and L2
    draw_ledger_flag(ax, 78, 69, 3.5, 4.5, color=c_channel1, text="L1")
    draw_ledger_flag(ax, 89.8, 69, 3.5, 4.5, color=c_channel2, text="L2")

    # P3 Connection Lines: to C1 and C2
    ax.plot([85.5, 85.5], [68, 52.5], color=c_channel1, lw=2.2)
    ax.plot([85.5, 85.5], [43.5, 36.0], color=c_channel2, lw=2.2)

    # =========================================================================
    # 5. ORDERER NODE (O - 30 RAFT CLUSTER HUB)
    # =========================================================================
    o_box = FancyBboxPatch((72, 46), 6.5, 7.5, boxstyle="round,pad=0.2", fc=c_orderer, ec='#0F172A', lw=1.6)
    ax.add_patch(o_box)
    ax.text(75.25, 50.5, "O", ha='center', va='center', fontsize=12, weight='bold', color='white')
    ax.text(75.25, 54.5, "Raft Leader", ha='center', fontsize=6.8, weight='bold', color='#065F46')

    # Orderer connection plugs at the bottom (Plug 1 blue, Plug 2 red)
    plug1 = patches.Circle((73.8, 45.8), 0.9, fc='#1D4ED8', ec='#0F172A', lw=1)
    ax.add_patch(plug1)
    ax.text(73.8, 45.8, "1", ha='center', va='center', fontsize=5.8, color='white', weight='bold')

    plug2 = patches.Circle((76.5, 45.8), 0.9, fc='#DC2626', ec='#0F172A', lw=1)
    ax.add_patch(plug2)
    ax.text(76.5, 45.8, "2", ha='center', va='center', fontsize=5.8, color='white', weight='bold')

    # Orderer Ledgers: L1 (blue) and L2 (red)
    draw_ledger_flag(ax, 79.5, 48, 3.5, 4.2, color=c_channel1, text="L1")
    draw_ledger_flag(ax, 79.5, 53, 3.5, 4.2, color=c_channel2, text="L2")

    # Orderer connections to C1 and C2
    ax.plot([73.8, 73.8], [44.9, 48.0], color=c_channel1, lw=2.0)
    ax.plot([76.5, 76.5], [44.9, 36.0], color=c_channel2, lw=2.0)

    # 30 Raft Orderer Cluster Annotation Badge
    raft_tag = FancyBboxPatch((83, 44), 14, 5.0, boxstyle="round,pad=0.3", fc='#ECFDF5', ec='#10B981', lw=1)
    ax.add_patch(raft_tag)
    ax.text(90, 46.5, "30 Raft Orderers Cluster\nCFT Consensus (500ms)", ha='center', va='center', fontsize=6.2, weight='bold', color='#065F46')
    ax.plot([80, 83], [50, 47], color='#10B981', lw=1, ls=':')

    # =========================================================================
    # 6. APPLICATION CONNECTIVITY LINES (ROUTED INTO CHANNELS)
    # =========================================================================
    # A1, A2, A3 connecting to Channel 1 (Blue lines)
    ax.plot([5.75, 5.75, 34], [72, 54, 54], color=c_channel1, lw=1.8)
    ax.plot([12.25, 12.25], [72, 54], color=c_channel1, lw=1.8)
    ax.plot([18.75, 18.75], [72, 54], color=c_channel1, lw=1.8)
    ax.annotate("", xy=(34, 52), xytext=(34, 54), arrowprops=dict(arrowstyle="->", color=c_channel1, lw=1.8))

    # A2, A3 connecting to Channel 2 (Red lines)
    ax.plot([13.5, 13.5, 42], [72, 38, 38], color=c_channel2, lw=1.6)
    ax.plot([20.0, 20.0], [72, 38], color=c_channel2, lw=1.6)
    ax.annotate("", xy=(42, 35), xytext=(42, 38), arrowprops=dict(arrowstyle="->", color=c_channel2, lw=1.6))

    # =========================================================================
    # 7. CHAINCODES & ENDORSEMENT POLICIES (BOTTOM PACKAGES CC1.1 & CC2)
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # Chaincode CC1.1 (dam v1.3 - Asset Lifecycle on Channel 1)
    # -------------------------------------------------------------------------
    cc1_box = FancyBboxPatch((46, 10), 18, 7.5, boxstyle="round,pad=0.2", fc='#1E3A8A', ec='#0F172A', lw=1.4)
    ax.add_patch(cc1_box)
    ax.text(55, 13.75, "CC1.1: dam v1.3", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(55, 11.2, "(AIGC Asset & Hash Registry)", ha='center', fontsize=6.2, color='#93C5FD')

    # Endorsement Triangles on CC1.1: R1 (Org1), R2 (Org2), R3 (Org3), R0 (Orderer)
    draw_endorsement_triangle(ax, 47.5, 17.5, 3.2, 3.8, color=c_org1, text="R1")
    draw_endorsement_triangle(ax, 51.5, 17.5, 3.2, 3.8, color=c_org2, text="R2")
    draw_endorsement_triangle(ax, 55.5, 17.5, 3.2, 3.8, color=c_org3, text="R3")
    draw_endorsement_triangle(ax, 59.5, 17.5, 3.2, 3.8, color=c_orderer, text="R0")

    # Dashed connection from CC1.1 to Channel 1 (C1)
    ax.plot([42, 42, 46], [48, 14, 14], color=c_channel1, lw=1.4, ls='--')

    # -------------------------------------------------------------------------
    # Chaincode CC2 (tokenERC20.js - Atomic _transferMulti on Channel 2)
    # -------------------------------------------------------------------------
    cc2_box = FancyBboxPatch((72, 10), 18, 7.5, boxstyle="round,pad=0.2", fc='#991B1B', ec='#0F172A', lw=1.4)
    ax.add_patch(cc2_box)
    ax.text(81, 13.75, "CC2: tokenERC20", ha='center', va='center', fontsize=8.5, weight='bold', color='white')
    ax.text(81, 11.2, "(_transferMulti In-Memory Map)", ha='center', fontsize=6.2, color='#FCA5A5', weight='bold')

    # Endorsement Triangles on CC2: R2 (Org2), R3 (Org3), R0 (Orderer)
    draw_endorsement_triangle(ax, 74.5, 17.5, 3.2, 3.8, color=c_org2, text="R2")
    draw_endorsement_triangle(ax, 78.5, 17.5, 3.2, 3.8, color=c_org3, text="R3")
    draw_endorsement_triangle(ax, 82.5, 17.5, 3.2, 3.8, color=c_orderer, text="R0")

    # Dashed connection from CC2 to Channel 2 (C2)
    ax.plot([66, 66, 72], [32, 14, 14], color=c_channel2, lw=1.4, ls='--')

    # =========================================================================
    # 8. LEGEND & ANNOTATIONS (BOTTOM LEFT)
    # =========================================================================
    legend_box = FancyBboxPatch((2, 32), 20, 24, boxstyle="round,pad=0.4", fc='white', ec='#CBD5E1', lw=1)
    ax.add_patch(legend_box)
    ax.text(12, 53.5, "ARCHITECTURAL LEGEND", ha='center', weight='bold', fontsize=7.5, color='#0F172A')

    # Legend items
    ax.text(3.5, 49.5, "• A1..A3: Applications / Clients", fontsize=6.8, color='#334155')
    ax.text(3.5, 46.5, "• P1..P3: Peer Nodes (Endorsers)", fontsize=6.8, color='#334155')
    ax.text(3.5, 43.5, "• O: 30-Orderer Raft Cluster", fontsize=6.8, color='#065F46', weight='bold')
    ax.text(3.5, 40.5, "• C1, C2: Isolated Fabric Channels", fontsize=6.8, color='#1E40AF')
    ax.text(3.5, 37.5, "• L1, L2: Channel World Ledgers", fontsize=6.8, color='#334155')
    ax.text(3.5, 34.5, "• S1, S2: Chaincodes (Smart Contracts)", fontsize=6.8, color='#334155')

    plt.tight_layout()
    png_path = os.path.join(output_dir, "fig8_hyperledger_canonical_topology.png")
    svg_path = os.path.join(output_dir, "fig8_hyperledger_canonical_topology.svg")
    plt.savefig(png_path, dpi=300)
    plt.savefig(svg_path)
    plt.close()

    print("[+] Canonical Hyperledger Fabric Topology (Fig 8) generated successfully:")
    print("    PNG:", png_path)
    print("    SVG:", svg_path)

if __name__ == "__main__":
    generate_canonical_fabric_architecture()
