import streamlit as st
import time

st.set_page_config(layout="wide", page_title="Google Photos", initial_sidebar_state="expanded")

# Initialize session state for search
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

def set_search(query):
    st.session_state.search_query = query

# Inject Custom CSS to override Streamlit's default styling
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
    
    /* Interactive Sidebar Menu */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 2px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 8px 16px 8px 16px !important;
        border-radius: 0 20px 20px 0 !important;
        margin-left: -1rem !important;
        margin-right: 1rem !important;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: #f1f3f4 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #e8f0fe !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] p {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }
    
    /* Hide Radio Circles in Sidebar */
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:nth-child(1) {
        display: none !important;
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
    
    /* Suggestion Chips (Overrides default stButton) */
    [data-testid="stButton"] button {
        border-radius: 16px !important;
        padding: 4px 16px !important;
        background-color: #ffffff !important;
        border: 1px solid #dadce0 !important;
        color: #5f6368 !important;
        font-size: 13px !important;
        min-height: 32px !important;
        height: 32px !important;
        line-height: 1 !important;
        margin-top: -10px !important;
        transition: all 0.2s;
    }
    [data-testid="stButton"] button:hover {
        background-color: #f1f3f4 !important;
        color: #202124 !important;
        border-color: #bdc1c6 !important;
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
    
    /* Legacy Image Grid Container for Sidebar Features */
    .legacy-img-container {
        width: 100%;
        aspect-ratio: 1;
        overflow: hidden;
        margin-bottom: 15px;
        border-radius: 8px;
    }
    .legacy-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Bounding Boxes */
    .bbox {
        position: absolute;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 4px;
        border-radius: 2px;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.8);
    }
    .bbox.red {
        border: 2px solid #ea4335;
        color: #ea4335;
        background-color: rgba(234, 67, 53, 0.15);
    }
    .bbox.yellow {
        border: 2px solid #fbbc04;
        color: #fbbc04;
        background-color: rgba(251, 188, 4, 0.15);
    }
    .bbox.blue {
        border: 2px solid #4285f4;
        color: #4285f4;
        background-color: rgba(66, 133, 244, 0.15);
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
    
    selected_nav = st.radio("Navigation", menu_options, index=0, label_visibility="collapsed")
    
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


# Core Data
family_photos = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?auto=format&fit=crop&w=400&q=80",
]

document_photos = [
    "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1586282391129-76a6df230234?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1568667256549-094345857637?auto=format&fit=crop&w=400&q=80",
]

explore_faces = [
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80",
]

explore_places = [
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=400&q=80",
]

sections = [
    {
        "date_header": "Today • Sunday, Jun 2, 2024",
        "location": "Nagarjuna Sagar Field Site",
        "cards": [
            {
                "title": "LOT-GR-408 / SL-14 B-28",
                "subtitle": "Rough Natural Travertine • 11:24 AM IST",
                "tag": "TARGET",
                "overlay1": "300mm Scale",
                "overlay2": "Verified Match",
                "img": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=800&q=80",
                "action": "👁️ Inspector Lightbox",
                "primary": True,
                "score": "Parity 1.0",
                "keywords": ["stone", "slab", "travertine", "rock", "yard", "marble", "rough", "construction", "material"],
                "bboxes": [
                    {"type": "red", "text": "LOT-GR-408 / SL-14 B-28", "top": "15%", "right": "5%"},
                    {"type": "yellow", "text": "300mm Scale", "bottom": "35%", "left": "10%"}
                ]
            },
            {
                "title": "STATUARIO-LOT-09",
                "subtitle": "Polished Calacatta Bundle • May 28, 2024",
                "tag": "REFERENCE",
                "overlay1": "Polished Slab",
                "overlay2": "Non-target",
                "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
                "action": "↗️ Differential",
                "primary": False,
                "score": "Non-match",
                "keywords": ["stone", "marble", "white", "polished", "slab", "statuario", "warehouse", "quartz"]
            },
            {
                "title": "BLK-99 // SECT-04",
                "subtitle": "Quarried Black Granite • Jun 2, 2024",
                "tag": "QUARRY",
                "overlay1": "Granite",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["granite", "black", "block", "quarry", "stone", "rock", "raw", "heavy"]
            },
            {
                "title": "BALAJI-CHALLAN-49102",
                "subtitle": "Delivery Memo • 11:15 AM IST",
                "tag": "DOCUMENT",
                "overlay1": "Fiscal",
                "overlay2": "Challan",
                "img": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80",
                "action": "🔍 Cross-Ref Challan",
                "primary": False,
                "score": "Indexed",
                "keywords": ["document", "paper", "receipt", "challan", "invoice", "memo", "delivery", "slip", "bill"]
            }
        ]
    },
    {
        "date_header": "Nov 8, 2025 • Jubilee Hills",
        "location": "Villa 42 (Plumbing Offset)",
        "cards": [
            {
                "title": "OFFSET 150mm -> VP 08/11",
                "subtitle": "PVC Pipe Chase • 09:14 AM IST",
                "tag": "TARGET",
                "overlay1": "Substrate: Brick",
                "overlay2": "OFFSET 150mm",
                "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
                "action": "👁️ Inspector Lightbox",
                "primary": True,
                "score": "Parity 1.0",
                "keywords": ["pipe", "plumbing", "pvc", "brick", "wall", "rough-in", "measurement", "tape", "offset", "water", "plumber"],
                "bboxes": [
                    {"type": "yellow", "text": "OFFSET 150mm -> VP 08/11", "top": "40%", "left": "20%"}
                ]
            },
            {
                "title": "ELEC-CONDUIT-11",
                "subtitle": "Chased electrical conduit • 10:20 AM IST",
                "tag": "DECOY",
                "overlay1": "Substrate: Brick",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["electrical", "wire", "conduit", "brick", "wall", "chase", "piping", "electrician"]
            },
            {
                "title": "SLAB-CORE-05",
                "subtitle": "Sunken slab core cut • 11:05 AM IST",
                "tag": "DECOY",
                "overlay1": "Concrete",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["core", "cut", "hole", "concrete", "slab", "floor", "drill"]
            },
            {
                "title": "HVAC-HANGER-02",
                "subtitle": "Ceiling HVAC hanger markings • 02:15 PM IST",
                "tag": "DECOY",
                "overlay1": "Concrete",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["hvac", "ceiling", "hanger", "duct", "concrete", "markings", "vent"]
            }
        ]
    },
    {
        "date_header": "Aug 18, 2025 • Madhapur Commercial",
        "location": "M35 Lab Cube Report",
        "cards": [
            {
                "title": "M35 GRADE 41.2 N/mm2",
                "subtitle": "Lab test certificate • 04:30 PM IST",
                "tag": "TARGET",
                "overlay1": "A4 Certificate",
                "overlay2": "M35 GRADE",
                "img": "https://images.unsplash.com/photo-1568667256549-094345857637?auto=format&fit=crop&w=800&q=80",
                "action": "👁️ Inspector Lightbox",
                "primary": True,
                "score": "Parity 1.0",
                "keywords": ["document", "paper", "report", "certificate", "lab", "test", "m35", "concrete", "grade", "seal", "stamp", "quality"],
                "bboxes": [
                    {"type": "blue", "text": "M35 GRADE 28 DAYS 41.2 N/mm2", "top": "50%", "left": "10%"}
                ]
            },
            {
                "title": "RMC-POUR-14",
                "subtitle": "Transit concrete pour • 08:15 AM IST",
                "tag": "DECOY",
                "overlay1": "Concrete",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["concrete", "pour", "truck", "transit", "rmc", "site", "cement", "mixer"]
            },
            {
                "title": "CUBE-TEST-01",
                "subtitle": "Concrete test cubes on water tank • 09:00 AM IST",
                "tag": "DECOY",
                "overlay1": "Concrete",
                "overlay2": "Negative",
                "img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&q=80",
                "action": "📄 View Site Log",
                "primary": False,
                "score": "Negative",
                "keywords": ["concrete", "cube", "test", "water", "curing", "tank", "cement", "sample"]
            }
        ]
    }
]

site_photos = [c["img"] for s in sections for c in s["cards"]]


# ==========================================
# UI RENDERING BASED ON SIDEBAR SELECTION
# ==========================================

if selected_nav in ["🖼️ Photos", "📁 Evidence Partition"]:
    
    # 2. INTERACTIVE TOP BAR SEARCH
    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input("Search", key="search_query", placeholder="🔍 Try searching: 'plumbing', 'stone slab', 'concrete', 'certificate', or 'pipe'", label_visibility="collapsed")
    with col2:
        if st.session_state.search_query:
            st.markdown('<div style="background-color: #fef7e0; color: #b06000; padding: 6px 12px; border-radius: 16px; font-size: 12px; border: 1px solid #fbbc04; font-weight: 600; text-align: center; margin-top: 2px;">✨ Evidence Lens: Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background-color: #f1f3f4; color: #5f6368; padding: 6px 12px; border-radius: 16px; font-size: 12px; border: 1px solid #dadce0; font-weight: 600; text-align: center; margin-top: 2px;">✨ Evidence Lens</div>', unsafe_allow_html=True)
            
    # Interactive Suggestion Chips
    s_cols = st.columns([1.2, 1.2, 1.2, 1.2, 1.2, 4])
    s_cols[0].button("🔧 Plumbing", on_click=set_search, args=("plumbing",))
    s_cols[1].button("🪨 Stone Slab", on_click=set_search, args=("stone slab",))
    s_cols[2].button("🏗️ Concrete", on_click=set_search, args=("concrete",))
    s_cols[3].button("📄 Lab Report", on_click=set_search, args=("lab report",))
    if st.session_state.search_query:
        s_cols[4].button("✖ Clear", on_click=set_search, args=("",))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Header
    st.markdown('<div style="font-size: 12px; color: #5f6368; text-align: right; padding-top: 10px; border-bottom: 1px solid #dadce0; padding-bottom: 10px; margin-bottom: 20px;">⚡ 18ms latency | 🛡️ Clean Verification (0% Contamination)</div>', unsafe_allow_html=True)
    
    st.info("🛡️ **24 domestic & family photos quarantined from work stream.** Analyzing site assets...")
    
    has_results = False
    
    for section in sections:
        if st.session_state.search_query:
            q = st.session_state.search_query.lower()
            filtered_cards = [
                c for c in section["cards"] 
                if q in c["title"].lower() 
                or q in c["tag"].lower() 
                or q in c["subtitle"].lower()
                or any(q in kw.lower() for kw in c.get("keywords", []))
            ]
        else:
            filtered_cards = section["cards"]
            
        if filtered_cards:
            has_results = True
            st.markdown(f"<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>{section['date_header']} <span style='font-size:12px; background:#f1f3f4; padding:4px 10px; border-radius:12px; margin-left:10px; color:#5f6368; border: 1px solid #dadce0;'>{section['location']}</span></h4>", unsafe_allow_html=True)
            
            cols = st.columns(4)
            for i, c in enumerate(filtered_cards):
                with cols[i % 4]:
                    action_class = "card-action primary" if c["primary"] else "card-action"
                    
                    bboxes_html = ""
                    if "bboxes" in c:
                        for bbox in c["bboxes"]:
                            top = f"top: {bbox.get('top', 'auto')};"
                            bottom = f"bottom: {bbox.get('bottom', 'auto')};"
                            left = f"left: {bbox.get('left', 'auto')};"
                            right = f"right: {bbox.get('right', 'auto')};"
                            bboxes_html += f"""<div class="bbox {bbox['type']}" style="{top} {bottom} {left} {right}">{bbox['text']}</div>"""
                    
                    html = f"""
                    <div class="evidence-card">
                        <div class="card-img-container">
                            <img src="{c['img']}">
                            {bboxes_html}
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
                    
    if not has_results:
        st.info(f"No evidence assets found matching '{st.session_state.search_query}'. Try searching for 'plumbing', 'stone', 'document', or 'concrete'.")

elif selected_nav == "🧭 Explore":
    st.title("🧭 Explore")
    st.markdown("Discover places, people, and things.")
    st.markdown("#### People & Pets")
    cols = st.columns(6)
    for i, img in enumerate(explore_faces + [family_photos[2]]):
        with cols[i % 6]:
            st.markdown(f'<div class="legacy-img-container" style="border-radius: 50%;"><img src="{img}"></div>', unsafe_allow_html=True)
    
    st.markdown("#### Places")
    cols = st.columns(4)
    for i, img in enumerate(explore_places + [family_photos[0], site_photos[2]]):
        with cols[i % 4]:
            st.markdown(f'<div class="legacy-img-container" style="aspect-ratio: 16/9;"><img src="{img}"></div>', unsafe_allow_html=True)

elif selected_nav == "👥 Sharing":
    st.title("👥 Sharing")
    st.markdown("Albums and photos shared with you.")
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="legacy-img-container" style="aspect-ratio: 16/9; position: relative;"><img src="{family_photos[4]}"><div style="position: absolute; bottom: 10px; left: 10px; color: white; font-weight: bold; text-shadow: 1px 1px 3px black;">Family Vacation 2025</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="legacy-img-container" style="aspect-ratio: 16/9; position: relative;"><img src="{site_photos[5]}"><div style="position: absolute; bottom: 10px; left: 10px; color: white; font-weight: bold; text-shadow: 1px 1px 3px black;">Site Engineers (Madhapur)</div></div>', unsafe_allow_html=True)

elif selected_nav == "📚 Albums":
    st.title("📚 Albums")
    st.markdown("Your collections.")
    cols = st.columns(4)
    albums = [
        {"title": "Downloads", "img": document_photos[0]},
        {"title": "Jubilee Hills Delivery", "img": site_photos[8]},
        {"title": "WhatsApp Images", "img": family_photos[3]},
        {"title": "Favorites", "img": family_photos[2]}
    ]
    for i, a in enumerate(albums):
        with cols[i]:
            st.markdown(f'<div class="legacy-img-container" style="border-radius: 12px;"><img src="{a["img"]}"></div><div style="font-weight: 500;">{a["title"]}</div><div style="font-size: 12px; color: gray;">{i*12 + 4} items</div>', unsafe_allow_html=True)

elif selected_nav == "📄 Documents":
    st.title("📄 Documents")
    st.markdown("Automatically categorized receipts, notes, and lab reports.")
    st.markdown("<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>Receipts & Forms</h4>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, img in enumerate(document_photos):
        with cols[i]:
            st.markdown(f'<div class="legacy-img-container" style="aspect-ratio: 3/4;"><img src="{img}"></div>', unsafe_allow_html=True)

elif selected_nav == "🗑️ Trash":
    st.title("🗑️ Trash")
    st.markdown("Items here will be permanently deleted after 60 days.")
    cols = st.columns(6)
    trash_items = [site_photos[1], family_photos[5], document_photos[1]]
    for i, img in enumerate(trash_items):
        with cols[i]:
            st.markdown(f'<div class="legacy-img-container" style="opacity: 0.5; filter: grayscale(100%);"><img src="{img}"></div>', unsafe_allow_html=True)
