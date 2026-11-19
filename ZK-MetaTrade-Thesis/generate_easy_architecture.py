import os
import matplotlib
import tempfile

temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = r"g:\gdownloads\ll\ZK-MetaTrade-Thesis\figures"
os.makedirs(output_dir, exist_ok=True)

def draw_cylinder(ax, x, y, w, h, fc='#93C5FD', ec='#1D4ED8', label="CouchDB"):
    """Draws a nice 3D cylinder representing CouchDB / Database."""
    # Cylinder body
    rect = patches.Rectangle((x - w/2, y), w, h, fc=fc, ec='none')
    ax.add_patch(rect)
    # Left and right side lines
    ax.plot([x - w/2, x - w/2], [y, y + h], color=ec, lw=1.2)
    ax.plot([x + w/2, x + w/2], [y, y + h], color=ec, lw=1.2)
    # Bottom ellipse arc
    bottom_arc = patches.Arc((x, y), w, h*0.4, angle=0, theta1=180, theta2=360, color=ec, lw=1.2)
    ax.add_patch(bottom_arc)
    bottom_fill = patches.Ellipse((x, y), w, h*0.4, fc=fc, ec='none')
    ax.add_patch(bottom_fill)
    # Top ellipse (full)
    top_el = patches.Ellipse((x, y + h), w, h*0.4, fc='#BFDBFE', ec=ec, lw=1.2)
    ax.add_patch(top_el)
    # Subtle middle disc line for 3D layered look
    mid_arc = patches.Arc((x, y + h*0.5), w, h*0.4, angle=0, theta1=180, theta2=360, color=ec, lw=0.8, ls=':')
    ax.add_patch(mid_arc)
    # Label
    ax.text(x, y + h*0.45, label, ha='center', va='center', fontsize=6.8, weight='bold', color='#1E3A8A')

def draw_user_icon(ax, x, y, color='#1E40AF', scale=1.0):
    """Draws a clean user avatar icon (head + shoulders)."""
    # Head
    head = patches.Circle((x, y + 1.2*scale), 0.7*scale, fc=color, ec='none')
    ax.add_patch(head)
    # Shoulders (semi-circle / curved wedge)
    body = patches.Wedge((x, y - 0.5*scale), 1.5*scale, 0, 180, fc=color, ec='none')
    ax.add_patch(body)

def draw_server_rack(ax, x, y, w, h, label="REST Server"):
    """Draws a clean server rack icon."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", fc='#F8FAFC', ec='#475569', lw=1.4)
    ax.add_patch(box)
    slot_h = h / 3.4
    for i in range(3):
        sy = y + 0.3 + i * (slot_h + 0.2)
        sbox = patches.Rectangle((x + 0.4, sy), w - 0.8, slot_h, fc='#E2E8F0', ec='#94A3B8', lw=0.8)
        ax.add_patch(sbox)
        # LED indicator dots
        ax.add_patch(patches.Circle((x + 1.0, sy + slot_h/2), 0.25, fc='#22C55E', ec='none'))
        ax.add_patch(patches.Circle((x + 1.7, sy + slot_h/2), 0.25, fc='#3B82F6', ec='none'))
        # Vent lines
        ax.plot([x + 3.0, x + w - 1.0], [sy + slot_h/2, sy + slot_h/2], color='#94A3B8', lw=1.2, ls='--')
    ax.text(x + w/2, y - 1.2, label, ha='center', va='top', fontsize=8.5, weight='bold', color='#0F172A')

def create_intuitive_architecture():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background subtle styling
    ax.fill([0, 100, 100, 0], [0, 0, 100, 100], color='#FAFAFC')

    # Main Header
    ax.text(50, 97.5, "Hyperledger Fabric Enterprise Consortium Architecture", 
            ha='center', va='center', fontsize=15, weight='bold', color='#0F172A')
    ax.text(50, 95.0, "ZK-MetaTrade Multi-Organization AIGC Trading Network with Raft Consensus & State DB", 
            ha='center', va='center', fontsize=9.5, color='#475569')

    # =========================================================================
    # 1. USERS & CLIENT APPLICATIONS (LEFT COLUMN)
    # =========================================================================
    ax.text(12, 91, "Users & Client Applications", ha='center', va='center', fontsize=11, weight='bold', color='#1E293B')

    # Client Box 1: Metaverse Customer (Buyer)
    b1 = FancyBboxPatch((2, 73), 20, 14, boxstyle="round,pad=0.6", fc='#EFF6FF', ec='#3B82F6', lw=1.5)
    ax.add_patch(b1)
    draw_user_icon(ax, 6, 81.5, color='#2563EB', scale=0.9)
    ax.text(14, 83.5, "Buyer Bob", fontsize=9.5, weight='bold', color='#1E40AF')
    ax.text(14, 80.5, "• Metaverse Customer\n• Balance: 850 Tokens\n• Org1 Admin Identity", fontsize=7.2, color='#1E3A8A')
    ax.text(12, 74.8, "[Metaverse VR / Web App]", ha='center', fontsize=6.8, style='italic', color='#3B82F6')

    # Client Box 2: AIGC Seller (Creator)
    b2 = FancyBboxPatch((2, 55), 20, 14, boxstyle="round,pad=0.6", fc='#ECFDF5', ec='#10B981', lw=1.5)
    ax.add_patch(b2)
    draw_user_icon(ax, 6, 63.5, color='#059669', scale=0.9)
    ax.text(14, 65.5, "Seller Alice", fontsize=9.5, weight='bold', color='#065F46')
    ax.text(14, 62.5, "• 3D AIGC Creator\n• Balance: 90 Tokens\n• Org2 User1 Identity", fontsize=7.2, color='#064E3B')
    ax.text(12, 56.8, "[AI Studio Creator Portal]", ha='center', fontsize=6.8, style='italic', color='#059669')

    # Client Box 3: Ancestor Model Owner
    b3 = FancyBboxPatch((2, 37), 20, 14, boxstyle="round,pad=0.6", fc='#FEF3C7', ec='#F59E0B', lw=1.5)
    ax.add_patch(b3)
    draw_user_icon(ax, 6, 45.5, color='#D97706', scale=0.9)
    ax.text(14, 47.5, "Base Trainer", fontsize=9.5, weight='bold', color='#92400E')
    ax.text(14, 44.5, "• SDXL / LoRA Foundation\n• Balance: 60 Tokens\n• Receives 10% DAG Royalty", fontsize=7.2, color='#78350F')
    ax.text(12, 38.8, "[Model Foundation Org]", ha='center', fontsize=6.8, style='italic', color='#D97706')

    # Off-Chain IPFS Box
    b_ipfs = FancyBboxPatch((2, 18), 20, 15, boxstyle="round,pad=0.6", fc='#F5F3FF', ec='#8B5CF6', lw=1.5)
    ax.add_patch(b_ipfs)
    # Draw Storage icon / discs
    ax.add_patch(patches.Rectangle((4, 26), 4, 3, fc='#C4B5FD', ec='#7C3AED', lw=1))
    ax.text(6, 27.5, "IPFS", ha='center', va='center', fontsize=6.5, weight='bold', color='#5B21B6')
    ax.text(14, 28.5, "IPFS Storage", fontsize=9.5, weight='bold', color='#6D28D9')
    ax.text(14, 24.5, "• Encrypted 3D GLTF ($D_{enc}$)\n• SHA-256 Hash Matching\n• Decentralized Off-Chain", fontsize=7.2, color='#4C1D95')
    ax.text(12, 19.8, "URI: ipfs://QmCyberCar3D...", ha='center', fontsize=6.5, family='monospace', color='#7C3AED')

    # =========================================================================
    # 2. REST API / GATEWAY SERVER (MIDDLE LEFT)
    # =========================================================================
    draw_server_rack(ax, 26.5, 52, 6.5, 12, label="REST Server\n& Web3 Gateway")
    ax.text(29.7, 47.5, "Node.js Fabric SDK\n(gRPC / TLS Client)", ha='center', fontsize=6.8, color='#64748B')

    # Arrows from Users to REST Server
    ax.annotate("", xy=(26.5, 60), xytext=(22, 79), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))
    ax.annotate("", xy=(26.5, 58), xytext=(22, 62), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5))
    ax.annotate("", xy=(26.5, 56), xytext=(22, 45), arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.5))

    # =========================================================================
    # 3. CONSORTIUM BLOCKCHAIN NETWORK (LARGE DASHED BOUNDARY)
    # =========================================================================
    # Outer Consortium Boundary
    rect_consortium = FancyBboxPatch((36, 12), 62, 78, boxstyle="round,pad=1.0", fc='#FFFFFF', ec='#3B82F6', lw=2.0, ls='--')
    ax.add_patch(rect_consortium)
    ax.text(38, 88, "Hyperledger Fabric Consortium Boundary (Channel: 'mychannel')", 
            fontsize=10.5, weight='bold', color='#1E3A8A')

    # -------------------------------------------------------------------------
    # 3A. COMPANY A / ORGANIZATION 1 (TOP BLUE REGION)
    # -------------------------------------------------------------------------
    rect_comp_a = FancyBboxPatch((38, 52), 26, 33, boxstyle="round,pad=0.8", fc='#F0F7FF', ec='#2563EB', lw=1.6, ls='--')
    ax.add_patch(rect_comp_a)
    ax.text(39.5, 82.5, "Company A (Org1 - Consumer Platform)", fontsize=9.5, weight='bold', color='#1D4ED8')

    # Peer-1 (Green/Blue Circle like ResearchGate)
    c_p1 = patches.Circle((45, 69), 4.2, fc='#86EFAC', ec='#16A34A', lw=1.8)
    ax.add_patch(c_p1)
    ax.text(45, 70, "Peer-1", ha='center', va='center', weight='bold', fontsize=8.5, color='#065F46')
    ax.text(45, 67.5, "(Endorser)", ha='center', va='center', fontsize=6.5, color='#14532D')

    # CouchDB attached to Peer-1
    draw_cylinder(ax, 55, 65, 5.0, 7.0, fc='#BAE6FD', ec='#0284C7', label="CouchDB")
    ax.annotate("", xy=(52.5, 69), xytext=(49.2, 69), arrowprops=dict(arrowstyle="<->", color='#0284C7', lw=1.2))

    # MSP (Identity) Circle
    c_msp1 = patches.Circle((45, 57.5), 3.2, fc='#93C5FD', ec='#2563EB', lw=1.4)
    ax.add_patch(c_msp1)
    draw_user_icon(ax, 45, 57.5, color='#1E40AF', scale=0.55)
    ax.text(45, 54.8, "MSP", ha='center', va='center', weight='bold', fontsize=7.2, color='#1E40AF')

    # CA Server Circle
    c_ca1 = patches.Circle((55, 57.5), 3.2, fc='#FDE047', ec='#CA8A04', lw=1.4)
    ax.add_patch(c_ca1)
    ax.text(55, 58.5, "CA", ha='center', va='center', weight='bold', fontsize=8, color='#854D0E')
    ax.text(55, 56.5, "Server", ha='center', va='center', fontsize=6.5, color='#854D0E')

    # -------------------------------------------------------------------------
    # 3B. COMPANY B / ORGANIZATION 2 (BOTTOM RED/GREEN REGION)
    # -------------------------------------------------------------------------
    rect_comp_b = FancyBboxPatch((38, 15), 26, 33, boxstyle="round,pad=0.8", fc='#FEF2F2', ec='#EF4444', lw=1.6, ls='--')
    ax.add_patch(rect_comp_b)
    ax.text(39.5, 45.5, "Company B (Org2 - AI Creator Studio)", fontsize=9.5, weight='bold', color='#DC2626')

    # Peer-1 (Company B)
    c_p2 = patches.Circle((45, 32), 4.2, fc='#86EFAC', ec='#16A34A', lw=1.8)
    ax.add_patch(c_p2)
    ax.text(45, 33, "Peer-1", ha='center', va='center', weight='bold', fontsize=8.5, color='#065F46')
    ax.text(45, 30.5, "(Endorser)", ha='center', va='center', fontsize=6.5, color='#14532D')

    # CouchDB attached to Peer-2
    draw_cylinder(ax, 55, 28, 5.0, 7.0, fc='#BAE6FD', ec='#0284C7', label="CouchDB")
    ax.annotate("", xy=(52.5, 32), xytext=(49.2, 32), arrowprops=dict(arrowstyle="<->", color='#0284C7', lw=1.2))

    # MSP (Org2) Circle
    c_msp2 = patches.Circle((45, 20.5), 3.2, fc='#FCA5A5', ec='#DC2626', lw=1.4)
    ax.add_patch(c_msp2)
    draw_user_icon(ax, 45, 20.5, color='#991B1B', scale=0.55)
    ax.text(45, 17.8, "MSP", ha='center', va='center', weight='bold', fontsize=7.2, color='#991B1B')

    # CA Server 2
    c_ca2 = patches.Circle((55, 20.5), 3.2, fc='#FDE047', ec='#CA8A04', lw=1.4)
    ax.add_patch(c_ca2)
    ax.text(55, 21.5, "CA", ha='center', va='center', weight='bold', fontsize=8, color='#854D0E')
    ax.text(55, 19.5, "Server", ha='center', va='center', fontsize=6.5, color='#854D0E')

    # -------------------------------------------------------------------------
    # 3C. CENTRAL ORDERER NODE (EXACTLY LIKE RESEARCHGATE CENTER)
    # -------------------------------------------------------------------------
    c_ord = patches.Circle((75, 50), 6.5, fc='#FCA5A5', ec='#E11D48', lw=2.2)
    ax.add_patch(c_ord)
    ax.text(75, 52.2, "Orderer", ha='center', va='center', weight='bold', fontsize=9.5, color='#881337')
    ax.text(75, 49.5, "Node", ha='center', va='center', weight='bold', fontsize=9.5, color='#881337')
    ax.text(75, 46.8, "(Raft Leader)", ha='center', va='center', fontsize=7.0, color='#9F1239')

    # 30 Raft Orderers Callout Badge
    ord_badge = FancyBboxPatch((66, 36), 18, 5.5, boxstyle="round,pad=0.3", fc='#FFF1F2', ec='#FB7185', lw=1)
    ax.add_patch(ord_badge)
    ax.text(75, 38.8, "30 Raft Orderers Cluster", ha='center', weight='bold', fontsize=7.5, color='#BE123C')
    ax.text(75, 36.8, "CFT Consensus • 500ms Batch", ha='center', fontsize=6.5, color='#9F1239')

    # Connecting lines from orderer to cluster badge
    ax.plot([75, 75], [43.5, 41.5], color='#E11D48', lw=1.2, ls=':')

    # -------------------------------------------------------------------------
    # 3D. SMART CONTRACT / CHAINCODE LAYER (RIGHT SIDE)
    # -------------------------------------------------------------------------
    cc_panel = FancyBboxPatch((70, 60), 25, 25, boxstyle="round,pad=0.6", fc='#FAF5FF', ec='#9333EA', lw=1.5)
    ax.add_patch(cc_panel)
    ax.text(82.5, 82.5, "Deployed Chaincode (dam v1.3)", ha='center', weight='bold', fontsize=9, color='#6B21A8')

    # Sub-box 1: tokenERC20
    sc1 = patches.Rectangle((72, 71), 21, 9.5, fc='white', ec='#A855F7', lw=1)
    ax.add_patch(sc1)
    ax.text(82.5, 78.5, "tokenERC20.js", ha='center', weight='bold', fontsize=8, color='#7E22CE')
    ax.text(82.5, 75.0, "★ _transferMulti (Atomic Map)", ha='center', weight='bold', fontsize=7, color='#15803D')
    ax.text(82.5, 72.5, "Fixes RYOW Stale-Read Bug", ha='center', fontsize=6.5, color='#4B5563')

    # Sub-box 2: digital_asset
    sc2 = patches.Rectangle((72, 61.5), 21, 8.5, fc='white', ec='#A855F7', lw=1)
    ax.add_patch(sc2)
    ax.text(82.5, 68, "digital_asset.js", ha='center', weight='bold', fontsize=8, color='#7E22CE')
    ax.text(82.5, 65, "• Hash Verify ($H_c == H$)", ha='center', fontsize=6.8, color='#374151')
    ax.text(82.5, 62.5, "• 10% Multi-Parent DAG Royalty", ha='center', fontsize=6.8, color='#374151')

    # =========================================================================
    # 4. GREEN & COLORED COMMUNICATION ARROWS (LIKE RESEARCHGATE)
    # =========================================================================
    # 1. Rest Server -> Peer-1 Company A (Step 1 Proposal)
    ax.annotate("", xy=(41, 69), xytext=(33, 60),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2.0))
    ax.text(35, 66, "① Proposal", fontsize=7.5, weight='bold', color='#15803D')

    # 1. Rest Server -> Peer-1 Company B (Step 1 Proposal)
    ax.annotate("", xy=(41, 32), xytext=(33, 56),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2.0))
    ax.text(35, 41, "① Proposal", fontsize=7.5, weight='bold', color='#15803D')

    # 2. Peers to Orderer Node (Step 2 Endorsed Tx)
    ax.annotate("", xy=(69, 53), xytext=(49, 68),
                arrowprops=dict(arrowstyle="->", color='#E11D48', lw=1.8))
    ax.text(58, 62.5, "② Endorsed Tx", fontsize=7.5, weight='bold', color='#BE123C')

    ax.annotate("", xy=(69, 47), xytext=(49, 33),
                arrowprops=dict(arrowstyle="->", color='#E11D48', lw=1.8))
    ax.text(58, 38.5, "② Endorsed Tx", fontsize=7.5, weight='bold', color='#BE123C')

    # 3. Orderer back to Peers (Step 3 Broadcast Ordered Blocks)
    ax.annotate("", xy=(47, 72.5), xytext=(71, 55),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8, ls='--'))
    ax.text(54, 73, "③ Deliver Block", fontsize=7.5, weight='bold', color='#1D4ED8')

    ax.annotate("", xy=(47, 28.5), xytext=(71, 45),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8, ls='--'))
    ax.text(54, 25.5, "③ Deliver Block", fontsize=7.5, weight='bold', color='#1D4ED8')

    # Direct line between Peers (Gossip data protocol)
    ax.annotate("", xy=(45, 64), xytext=(45, 37),
                arrowprops=dict(arrowstyle="<->", color='#64748B', lw=1.2, ls=':'))
    ax.text(45.5, 50, "Gossip\nProtocol", ha='left', va='center', fontsize=6.8, color='#64748B')

    # =========================================================================
    # 5. BOTTOM SUMMARY BAR (AUDIT & EMPIRICAL CONSERVATION)
    # =========================================================================
    bar = FancyBboxPatch((4, 2.5), 92, 6.5, boxstyle="round,pad=0.4", fc='#0F172A', ec='#38BDF8', lw=1.5)
    ax.add_patch(bar)
    ax.text(50, 6.8, "LIVE NETWORK TEST VERIFICATION (HYPERLEDGER FABRIC v2.5.16 ON WSL2)", 
            ha='center', va='center', weight='bold', fontsize=8.5, color='#38BDF8')
    ax.text(50, 4.0, "Buyer Bob (850 TKN) + Seller Alice (90 TKN) + Base Trainer (60 TKN) + Escrow (0 TKN) = 1,000 TOKENS (EXACT CONSERVATION SATISFIED)", 
            ha='center', va='center', fontsize=8.0, color='#F8FAFC')

    plt.tight_layout()
    png_path = os.path.join(output_dir, "fig5_easy_consortium_architecture.png")
    svg_path = os.path.join(output_dir, "fig5_easy_consortium_architecture.svg")
    plt.savefig(png_path, dpi=300)
    plt.savefig(svg_path)
    
    # Also overwrite fig5_consortium_fabric_architecture with this upgraded, cleaner design!
    plt.savefig(os.path.join(output_dir, "fig5_consortium_fabric_architecture.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "fig5_consortium_fabric_architecture.svg"))

    plt.close()
    print("[+] Intuitive ResearchGate-style Consortium Architecture generated successfully at:")
    print("    PNG:", png_path)
    print("    SVG:", svg_path)

if __name__ == "__main__":
    create_intuitive_architecture()
