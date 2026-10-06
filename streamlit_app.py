import streamlit as st

st.set_page_config(layout="wide", page_title="Google Photos | Evidence Partition", initial_sidebar_state="expanded")

# Inject Custom CSS to override Streamlit's default styling and match Google Photos Dark Mode
st.markdown("""
<style>
    /* Global Dark Theme Settings */
    :root {
        --bg-color: #202124;
        --sidebar-bg: #202124;
        --text-main: #e8eaed;
        --text-muted: #9aa0a6;
        --accent: #8ab4f8;
        --border: #3c4043;
        --card-bg: #303134;
    }
    
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
        font-family: 'Google Sans', 'Roboto', sans-serif;
    }
    
    /* Hide top header */
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border);
    }
    
    /* Top Bar Search */
    .top-bar {
        display: flex;
        align-items: center;
        padding: 10px 24px;
        border-bottom: 1px solid var(--border);
        margin-top: -60px;
        margin-bottom: 20px;
    }
    
    .search-box {
        background-color: #303134;
        border-radius: 8px;
        padding: 10px 20px;
        width: 60%;
        display: flex;
        align-items: center;
        color: var(--text-main);
        margin: 0 auto;
    }
    
    /* Filter Chips */
    .filter-row {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    }
    .chip {
        background-color: #303134;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 6px 16px;
        font-size: 13px;
        color: var(--text-main);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .chip.active {
        background-color: #41331c;
        border-color: #fbbc04;
        color: #fbbc04;
    }
    
    /* Evidence Cards */
    .evidence-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border);
        overflow: hidden;
        margin-bottom: 20px;
    }
    .card-img-container {
        position: relative;
        height: 180px;
        width: 100%;
        background-color: #000;
    }
    .card-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.8;
    }
    .card-tag {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: rgba(0,0,0,0.6);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        border: 1px solid #5f6368;
    }
    .card-overlay {
        position: absolute;
        bottom: 10px;
        left: 10px;
        display: flex;
        gap: 8px;
    }
    .overlay-pill {
        background-color: rgba(32, 33, 36, 0.8);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        border: 1px solid #5f6368;
    }
    
    .card-content {
        padding: 16px;
    }
    .card-title {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 4px;
        color: var(--text-main);
        display: flex;
        justify-content: space-between;
    }
    .card-subtitle {
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 16px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .card-action {
        width: 100%;
        background-color: transparent;
        border: 1px solid var(--border);
        color: var(--accent);
        padding: 8px;
        border-radius: 20px;
        text-align: center;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
    }
    .card-action.primary {
        background-color: #8ab4f8;
        color: #202124;
    }
    
</style>
""", unsafe_allow_html=True)

# 1. SIDEBAR Navigation (Mocking Google Photos left menu)
with st.sidebar:
    st.markdown("### 💠 Google Photos <span style='background:#303134; padding:2px 6px; border-radius:4px; font-size:10px; border:1px solid #5f6368;'>Labs</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("🖼️ Photos")
    st.markdown("🧭 Explore")
    st.markdown("👥 Sharing")
    st.markdown("📚 Albums")
    st.markdown("📄 Documents")
    st.markdown("""
    <div style="background-color: #4285f422; color: #8ab4f8; padding: 10px; border-radius: 0 20px 20px 0; margin-left: -1rem; margin-bottom: 8px; font-weight: 600;">
        📁 Evidence Partition
    </div>
    """, unsafe_allow_html=True)
    st.markdown("🗑️ Trash")
    
    st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #303134; padding: 16px; border-radius: 12px; font-size: 12px;">
        ☁️ <b>Storage Vault</b><br>
        <span style="color:#9aa0a6;">1.4 TB of 2 TB used</span><br>
        <div style="width:100%; height:4px; background:#5f6368; margin-top:8px; border-radius:2px;">
            <div style="width:70%; height:100%; background:#8ab4f8; border-radius:2px;"></div>
        </div>
        <br>
        <span style="color:#8ab4f8;">Get more storage</span>
    </div>
    """, unsafe_allow_html=True)

# 2. TOP BAR
st.markdown("""
<div class="top-bar">
    <div class="search-box">
        🔍 LOT-GR-408 / SL-14
        <span style="margin-left: auto; background-color: #41331c; color: #fbbc04; padding: 4px 12px; border-radius: 16px; font-size: 12px; border: 1px solid #fbbc04;">✨ Evidence Lens: Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. FILTERS & METRICS
st.markdown("""
<div class="filter-row">
    <div class="chip">📍 Nagarjuna Sagar Yard (May 2024) ✕</div>
    <div class="chip">💠 Substrate: Rough Natural Stone ✕</div>
    <div class="chip">✏️ Marking: Wax Grease Pencil</div>
    <div class="chip">👁️ Overlays: Visible</div>
</div>
<div class="filter-row">
    <div class="chip">⚡ 18ms latency</div>
    <div class="chip">🛡️ Clean Verification</div>
</div>
<div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #3c4043; padding-bottom: 15px;">
    <div>
        <span style="background-color: #303134; color: #9aa0a6; padding: 8px 16px; border-radius: 16px 0 0 16px; border: 1px solid #3c4043; font-size: 13px;">🕘 Photos Legacy Mode</span><span style="background-color: #4285f444; color: #8ab4f8; padding: 8px 16px; border-radius: 0 16px 16px 0; border: 1px solid #8ab4f8; font-size: 13px;">✨ Evidence Lens Lab (Active)</span>
    </div>
    <div style="font-size: 12px; color: #9aa0a6;">
        🔵 24 family photos from Himachal quarantined • 4 physical evidence assets verified
    </div>
</div>
""", unsafe_allow_html=True)

# 4. MAIN GALLERY
st.markdown("<h4 style='font-weight: 500;'>Today • Sunday, Jun 2, 2024 <span style='font-size:12px; background:#303134; padding:4px 10px; border-radius:12px; margin-left:10px; color:#9aa0a6;'>Nagarjuna Sagar Field Site</span></h4>", unsafe_allow_html=True)

# Cards Data based on mockup
cards = [
    {
        "title": "LOT-GR-408 / SL-14 B-28",
        "subtitle": "Rough Natural Travertine • 11:24 AM IST",
        "tag": "TARGET",
        "overlay1": "300mm Scale",
        "overlay2": "Verified Match",
        "img": "https://images.unsplash.com/photo-1618367588411-d9a90fefa880?auto=format&fit=crop&q=80&w=400&h=200",
        "action": "👁️ Open in Inspector Lightbox",
        "primary": True,
        "score": "Parity 1.0"
    },
    {
        "title": "STATUARIO-LOT-09",
        "subtitle": "Polished Calacatta Bundle • May 28, 2024",
        "tag": "REFERENCE",
        "overlay1": "Polished Slab",
        "overlay2": "Non-target",
        "img": "https://images.unsplash.com/photo-1588805214470-381a1795db2c?auto=format&fit=crop&q=80&w=400&h=200",
        "action": "↗️ View Differential",
        "primary": False,
        "score": "Non-match"
    },
    {
        "title": "BLK-99 // SECT-04",
        "subtitle": "Quarried Black Granite • Jun 2, 2024",
        "tag": "QUARRY",
        "overlay1": "Granite",
        "overlay2": "Negative",
        "img": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?auto=format&fit=crop&q=80&w=400&h=200",
        "action": "📄 View Site Log",
        "primary": False,
        "score": "Negative"
    },
    {
        "title": "BALAJI-CHALLAN-49102",
        "subtitle": "Delivery Memo • 11:15 AM IST",
        "tag": "DOCUMENT",
        "overlay1": "Fiscal",
        "overlay2": "Challan",
        "img": "https://images.unsplash.com/photo-1618424181497-157f25b6ce7e?auto=format&fit=crop&q=80&w=400&h=200",
        "action": "🔍 Cross-Ref Challan",
        "primary": False,
        "score": "Indexed"
    }
]

cols = st.columns(4)

for i, c in enumerate(cards):
    with cols[i]:
        action_class = "card-action primary" if c["primary"] else "card-action"
        
        html = f"""
        <div class="evidence-card">
            <div class="card-img-container">
                <img src="{c['img']}">
                <div class="card-tag">{c['tag']}</div>
                <div class="card-overlay">
                    <div class="overlay-pill">{c['overlay1']}</div>
                    <div class="overlay-pill" style="color:#8ab4f8; border-color:#8ab4f8;">{c['overlay2']}</div>
                </div>
            </div>
            <div class="card-content">
                <div class="card-title">
                    <span>{c['title']}</span>
                    <span style="font-size:10px; background:#4285f422; color:#8ab4f8; padding:2px 6px; border-radius:4px;">{c['score']}</span>
                </div>
                <div class="card-subtitle">{c['subtitle']}</div>
                <div class="{action_class}">{c['action']}</div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
