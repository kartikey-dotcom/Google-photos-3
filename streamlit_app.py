import streamlit as st

st.set_page_config(layout="wide", page_title="Google Photos | Evidence Partition", initial_sidebar_state="expanded")

# Inject Custom CSS to override Streamlit's default styling for Google Photos Light Mode
st.markdown("""
<style>
    /* Global Light Theme Settings */
    :root {
        --bg-color: #ffffff;
        --sidebar-bg: #ffffff;
        --text-main: #202124;
        --text-muted: #5f6368;
        --accent: #1a73e8;
        --border: #dadce0;
        --card-bg: #ffffff;
    }
    
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
        font-family: 'Google Sans', 'Roboto', sans-serif;
    }
    
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border);
    }
    
    /* Interactive Sidebar Menu (Radio Overrides) */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 2px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 10px 16px 10px 16px !important;
        border-radius: 0 20px 20px 0 !important;
        margin-left: -1rem !important;
        margin-right: 1rem !important;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: #f1f3f4 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #e8f0fe !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] p {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }
    
    /* Search Bar Styling */
    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: #f1f3f4;
        border-radius: 24px;
        border: 1px solid transparent;
        padding: 4px 12px;
        transition: background-color 0.2s, box-shadow 0.2s;
    }
    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        background-color: #ffffff;
        box-shadow: 0 1px 1px 0 rgba(65,69,73,0.3),0 1px 3px 1px rgba(65,69,73,0.15);
    }
    
    /* Main Area Horizontal Radio Toggle */
    .main-toggle [data-testid="stRadio"] > div {
        display: inline-flex;
        background-color: #f1f3f4;
        border-radius: 24px;
        padding: 4px;
        gap: 0px;
        border: 1px solid var(--border);
    }
    .main-toggle [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 8px 16px !important;
        border-radius: 20px !important;
        margin: 0 !important;
        cursor: pointer;
        color: var(--text-muted) !important;
    }
    .main-toggle [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    .main-toggle [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #e8f0fe !important;
    }
    .main-toggle [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] p {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }
    
    /* Filter Chips */
    .filter-row {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    }
    .chip {
        background-color: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 6px 16px;
        font-size: 13px;
        color: var(--text-main);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Evidence Cards */
    .evidence-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border);
        overflow: hidden;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .evidence-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
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
    }
    .card-tag {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: rgba(255,255,255,0.9);
        color: #202124;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        border: 1px solid var(--border);
    }
    .card-overlay {
        position: absolute;
        bottom: 10px;
        left: 10px;
        display: flex;
        gap: 8px;
    }
    .overlay-pill {
        background-color: rgba(255,255,255,0.9);
        color: #202124;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid var(--border);
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
        font-weight: 600;
        cursor: pointer;
    }
    .card-action.primary {
        background-color: var(--accent);
        color: #ffffff;
        border-color: var(--accent);
    }
    
</style>
""", unsafe_allow_html=True)

# 1. Interactive SIDEBAR Navigation
with st.sidebar:
    st.markdown("### 💠 Google Photos <span style='background:#f1f3f4; color:#5f6368; padding:2px 6px; border-radius:4px; font-size:10px; border:1px solid #dadce0;'>Labs</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu_options = [
        "🖼️ Photos",
        "🧭 Explore",
        "👥 Sharing",
        "📚 Albums",
        "📄 Documents",
        "📁 Evidence Partition",
        "🗑️ Trash"
    ]
    
    selected_nav = st.radio("Navigation", menu_options, index=5, label_visibility="collapsed")
    
    st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #f1f3f4; padding: 16px; border-radius: 12px; font-size: 12px; border: 1px solid #dadce0;">
        ☁️ <b style="color: #202124;">Storage Vault</b><br>
        <span style="color:#5f6368;">1.4 TB of 2 TB used</span><br>
        <div style="width:100%; height:4px; background:#dadce0; margin-top:8px; border-radius:2px;">
            <div style="width:70%; height:100%; background:#1a73e8; border-radius:2px;"></div>
        </div>
        <br>
        <span style="color:#1a73e8; font-weight:600;">Get more storage</span>
    </div>
    """, unsafe_allow_html=True)

# Handle UI based on Interactive Selection
if selected_nav == "📁 Evidence Partition":
    # 2. INTERACTIVE TOP BAR SEARCH
    col1, col2 = st.columns([5, 1])
    with col1:
        search_query = st.text_input("Search", value="", placeholder="🔍 e.g. LOT-GR-408 / SL-14 or STATUARIO", label_visibility="collapsed")
    with col2:
        st.markdown('<div style="background-color: #fef7e0; color: #b06000; padding: 6px 12px; border-radius: 16px; font-size: 12px; border: 1px solid #fbbc04; font-weight: 600; text-align: center; margin-top: 2px;">✨ Evidence Lens: Active</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    col_toggle, col_stats = st.columns([2, 1])
    with col_toggle:
        st.markdown('<div class="main-toggle">', unsafe_allow_html=True)
        view_mode = st.radio("Mode", ["🕘 Photos Legacy Mode", "✨ Evidence Lens Lab (Active)"], index=1, horizontal=True, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_stats:
        st.markdown('<div style="font-size: 12px; color: #5f6368; text-align: right; padding-top: 10px;">🔵 24 family photos quarantined • 4 evidence assets verified</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
    
    if view_mode == "✨ Evidence Lens Lab (Active)":
        # 4. MAIN GALLERY (Interactive)
        st.markdown("<h4 style='font-weight: 500; color:#202124;'>Today • Sunday, Jun 2, 2024 <span style='font-size:12px; background:#f1f3f4; padding:4px 10px; border-radius:12px; margin-left:10px; color:#5f6368; border: 1px solid #dadce0;'>Nagarjuna Sagar Field Site</span></h4>", unsafe_allow_html=True)
        
        all_cards = [
            {
                "title": "LOT-GR-408 / SL-14 B-28",
                "subtitle": "Rough Natural Travertine • 11:24 AM IST",
                "tag": "TARGET",
                "overlay1": "300mm Scale",
                "overlay2": "Verified Match",
                "img": "https://images.unsplash.com/photo-1618367588411-d9a90fefa880?auto=format&fit=crop&q=80&w=400&h=200",
                "action": "👁️ Inspector Lightbox",
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
                "action": "↗️ Differential",
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
        
        # Interactive Filtering Logic
        if search_query:
            filtered_cards = [c for c in all_cards if search_query.lower() in c["title"].lower() or search_query.lower() in c["tag"].lower()]
        else:
            filtered_cards = all_cards
            
        if not filtered_cards:
            st.info(f"No evidence assets found matching '{search_query}'. Try 'LOT-GR-408' or 'DOCUMENT'.")
        else:
            cols = st.columns(4)
            for i, c in enumerate(filtered_cards):
                with cols[i % 4]:
                    action_class = "card-action primary" if c["primary"] else "card-action"
                    
                    html = f"""
                    <div class="evidence-card">
                        <div class="card-img-container">
                            <img src="{c['img']}">
                            <div class="card-tag">{c['tag']}</div>
                            <div class="card-overlay">
                                <div class="overlay-pill">{c['overlay1']}</div>
                                <div class="overlay-pill" style="color:#1a73e8; border-color:#8ab4f8;">{c['overlay2']}</div>
                            </div>
                        </div>
                        <div class="card-content">
                            <div class="card-title">
                                <span>{c['title']}</span>
                                <span style="font-size:10px; background:#e8f0fe; color:#1a73e8; padding:2px 6px; border-radius:4px; font-weight:700;">{c['score']}</span>
                            </div>
                            <div class="card-subtitle">{c['subtitle']}</div>
                            <div class="{action_class}">{c['action']}</div>
                        </div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Legacy Mode active. Professional indexing disabled. 14 minutes estimated to find assets manually.")
else:
    st.info(f"You selected **{selected_nav}**. This section is not part of the Evidence Lens MVP.")

