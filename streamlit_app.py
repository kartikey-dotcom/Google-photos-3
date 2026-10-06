import streamlit as st
import time

st.set_page_config(layout="wide", page_title="Google Photos - Health Cabinet", initial_sidebar_state="expanded")

# Initialize state
if "search_query" not in st.session_state:
    st.session_state.search_query = "Metformin 500mg"
if "health_mode" not in st.session_state:
    st.session_state.health_mode = "lens" # "lens" or "legacy"
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None

def set_mode(mode):
    if st.session_state.health_mode != mode:
        st.session_state.health_mode = mode
        if mode == "legacy":
            st.session_state.is_loading = True
        else:
            st.session_state.is_loading = False

def set_search(q):
    st.session_state.search_query = q

def open_lightbox(card_title):
    st.session_state.selected_card = card_title

@st.dialog("Clinical Info Panel", width="large")
def show_lightbox(c):
    cols = st.columns([2, 1])
    with cols[0]:
        st.image(c['img'], use_column_width=True)
    with cols[1]:
        if 'dialog' in c:
            d = c['dialog']
            st.markdown(f"### {d['drug']}")
            st.markdown(f"**Strength:** {d['strength']}")
            st.markdown(f"**Prescribed By:** {d['prescriber']}")
            st.markdown(f"**Extraction Substrate:** {d['substrate']}")
            st.markdown(f"**Detected Batch:** {d['batch']}")
            st.markdown("---")
            st.info("Verified by Health Cabinet AI Lens")

# Simulate Latency on state change
if st.session_state.is_loading:
    with st.spinner("Searching your photos, documents, and memories..."):
        time.sleep(4.0)
    st.session_state.is_loading = False

# Inject Custom CSS (Dark Theme MD3)
st.markdown("""
<style>
    /* Global Dark Theme Settings */
    :root {
        --bg-color: #ffffff;
        --sidebar-bg: #ffffff;
        --text-main: #202124;
        --text-muted: #5f6368;
        --accent: #1a73e8;
        --border: #dadce0;
        --card-bg: #ffffff;
        --hover-bg: #f1f3f4;
    }
    
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
        font-family: 'Google Sans', 'Roboto', sans-serif;
    }
    
    header {visibility: hidden;}
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 8px 16px !important;
        border-radius: 0 20px 20px 0 !important;
        margin-left: -1rem !important;
        margin-right: 1rem !important;
        cursor: pointer;
        transition: background-color 0.2s ease;
        color: var(--text-main) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: var(--hover-bg) !important;
    }
    /* Highlight for Health Cabinet */
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #e8f0fe !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] p {
        color: #1a73e8 !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:nth-child(1) { display: none !important; }
    
    /* Inputs & Buttons */
    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: #f1f3f4;
        border-radius: 24px;
        border: 1px solid transparent;
        color: var(--text-main);
    }
    [data-testid="stButton"] button {
        border-radius: 16px !important;
        padding: 4px 16px !important;
        background-color: #ffffff !important;
        border: 1px solid var(--border) !important;
        color: var(--text-muted) !important;
        font-size: 13px !important;
        transition: all 0.2s;
    }
    [data-testid="stButton"] button:hover {
        background-color: var(--hover-bg) !important;
        color: var(--text-main) !important;
    }
    
    /* Active Toggle Button */
    .toggle-active > button {
        background-color: #e8f0fe !important;
        border-color: #8ab4f8 !important;
        color: #1a73e8 !important;
    }
    
    /* Cards */
    .evidence-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border);
        overflow: hidden;
        margin-bottom: 20px;
        position: relative;
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
    
    /* Bounding Boxes */
    .bbox {
        position: absolute;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 4px;
        border-radius: 2px;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.8);
    }
    .bbox.red { border: 2px solid #f28b82; color: #f28b82; background-color: rgba(242, 139, 130, 0.15); }
    .bbox.yellow { border: 2px solid #fde293; color: #fde293; background-color: rgba(253, 226, 147, 0.15); }
    .bbox.blue { border: 2px solid #aecbfa; color: #aecbfa; background-color: rgba(174, 203, 250, 0.15); }
    
    /* Hover Actions (Checkmark and Star) */
    .card-hover-actions {
        position: absolute;
        top: 10px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 10px;
        opacity: 0.8;
    }
    .hover-icon {
        background: rgba(0,0,0,0.6);
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .card-tag {
        position: absolute;
        top: 40px;
        left: 10px;
        background-color: rgba(255,255,255,0.9);
        color: #202124;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
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
        font-weight: 500;
        border: 1px solid var(--border);
    }
    
    .card-content { padding: 16px; }
    .card-title { font-size: 16px; font-weight: 600; margin-bottom: 4px; color: var(--text-main); }
    .card-subtitle { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
    .verified-pill { font-size: 11px; color: var(--accent); background: rgba(138,180,248,0.1); padding: 4px 8px; border-radius: 12px; display: inline-block; }
    
    /* Legacy Simple Grid */
    .legacy-img-container { width: 100%; aspect-ratio: 16/9; overflow: hidden; margin-bottom: 20px; border-radius: 12px; }
    .legacy-img-container img { width: 100%; height: 100%; object-fit: cover; }
</style>
""", unsafe_allow_html=True)

# 1. SIDEBAR Navigation
with st.sidebar:
    st.markdown("### 💠 Photos <span style='background:#f1f3f4; color:#5f6368; padding:2px 6px; border-radius:4px; font-size:10px;'>Labs</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu_options = [
        "🖼️ Photos",
        "🧭 Explore",
        "👥 Sharing",
        "📚 Albums",
        "📄 Documents",
        "🏥 Health Cabinet",
        "🗑️ Trash"
    ]
    selected_nav = st.radio("Navigation", menu_options, index=5, label_visibility="collapsed")
    


# Data
family_photos = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?auto=format&fit=crop&w=400&q=80",
]

health_sections = [
    {
        "date_header": "October 2024 • Recent Clinical Records & Prescriptions",
        "cards": [
            {
                "title": "Metformin HCl 500mg",
                "subtitle": "Oct 28, 2024 • Apollo Pharmacy Dispense",
                "tag": "METFORMIN 500MG ER",
                "overlay1": "Substrate: Silver Foil",
                "overlay2": "Lot: 4B391",
                "img": "https://images.unsplash.com/photo-1631549916768-4119b2e5f926?auto=format&fit=crop&w=800&q=80",
                "verified": "Verified Salt: Metformin HCl",
                "bboxes": [
                    {"type": "blue", "text": "METFORMIN 500MG ER", "top": "25%", "left": "15%"},
                    {"type": "red", "text": "Exp: 11/2025", "bottom": "20%", "right": "10%"}
                ],
                "dialog": {
                    "drug": "Metformin Hydrochloride Extended Release",
                    "strength": "500mg",
                    "prescriber": "Apollo Pharmacy Dispense (Dr. R. Mehta)",
                    "substrate": "Specular Metallic Blister Pack",
                    "batch": "4B391 • Exp: 11/2025"
                }
            },
            {
                "title": "Hypertension Rx (Telmisartan)",
                "subtitle": "Oct 14, 2024 • Dr. A. R. Khan (Cardiology)",
                "tag": "TELMISARTAN 40MG",
                "overlay1": "Substrate: Doctor Script",
                "overlay2": "1 Tab Daily OD",
                "img": "https://images.unsplash.com/photo-1583324113626-70df0f4deaab?auto=format&fit=crop&w=800&q=80",
                "verified": "Verified Seal: City Hospital",
                "bboxes": [{"type": "yellow", "text": "Telmisartan 40mg (OD)", "top": "40%", "left": "25%"}],
                "dialog": {"drug": "Telmisartan", "strength": "40mg", "prescriber": "Dr. A. R. Khan", "substrate": "Handwritten Script", "batch": "N/A"}
            },
            {
                "title": "Metabolic & HbA1c Panel",
                "subtitle": "Oct 26, 2024 • Metropolis Healthcare Labs",
                "tag": "HBA1C: 7.2% (ELEVATED)",
                "overlay1": "Substrate: Lab Report",
                "overlay2": "Range: 4.0-5.6%",
                "img": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
                "verified": "Metropolis Healthcare Labs",
                "bboxes": [{"type": "red", "text": "HbA1c: 7.2%", "top": "50%", "left": "30%"}],
                "dialog": {"drug": "Diagnostic Blood Panel", "strength": "N/A", "prescriber": "Dr. Sarah Chen", "substrate": "A4 Print with Blue Seal", "batch": "SID: 8849201"}
            },
            {
                "title": "Pharmacy Register Receipt",
                "subtitle": "Oct 16, 2024 • Total $65.03 Paid",
                "tag": "CITY DRUG PHARMACY",
                "overlay1": "Substrate: Thermal Paper",
                "overlay2": "4 Meds Listed",
                "img": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
                "verified": "Fiscal Non-Clinical Slip",
                "bboxes": [{"type": "blue", "text": "Total: $65.03", "bottom": "15%", "right": "20%"}],
                "dialog": {"drug": "Multiple (Fiscal)", "strength": "N/A", "prescriber": "N/A", "substrate": "Thermal Receipt", "batch": "Trans: #4928"}
            }
        ]
    },
    {
        "date_header": "August 2024 • Diagnostic Panel & Annual Checkup",
        "cards": [
            {
                "title": "CBC Complete Blood Count",
                "subtitle": "Aug 12, 2024 • City Lab Services",
                "tag": "WBC: 6.8 K/uL",
                "overlay1": "Substrate: Lab Report",
                "overlay2": "Normal Range",
                "img": "https://images.unsplash.com/photo-1638202993928-7267aad84c31?auto=format&fit=crop&w=800&q=80",
                "verified": "Verified Seal: City Lab",
                "bboxes": [{"type": "yellow", "text": "WBC: 6.8", "top": "30%", "left": "40%"}],
                "dialog": {"drug": "CBC Panel", "strength": "N/A", "prescriber": "Self", "substrate": "A4 Print", "batch": "SID: 77391"}
            },
            {
                "title": "Thyroid Profile (TSH)",
                "subtitle": "Aug 12, 2024 • City Lab Services",
                "tag": "TSH: 2.1 mIU/L",
                "overlay1": "Substrate: Lab Report",
                "overlay2": "Euthyroid",
                "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
                "verified": "Verified Seal: City Lab",
                "bboxes": [{"type": "blue", "text": "TSH: 2.1", "top": "40%", "left": "20%"}],
                "dialog": {"drug": "Thyroid Panel", "strength": "N/A", "prescriber": "Self", "substrate": "A4 Print", "batch": "SID: 77391"}
            },
            {
                "title": "Cardiologist Follow-up Note",
                "subtitle": "Aug 05, 2024 • Dr. A. R. Khan",
                "tag": "BP: 120/80",
                "overlay1": "Substrate: Doctor Script",
                "overlay2": "Stable",
                "img": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80",
                "verified": "Verified Signature",
                "bboxes": [{"type": "red", "text": "BP: 120/80", "top": "60%", "left": "50%"}],
                "dialog": {"drug": "Clinical Note", "strength": "N/A", "prescriber": "Dr. A. R. Khan", "substrate": "Handwritten Note", "batch": "N/A"}
            },
            {
                "title": "Influenza Vaccination Record",
                "subtitle": "Aug 01, 2024 • Apex Clinic",
                "tag": "FLUZONE QUAD",
                "overlay1": "Substrate: Cardstock",
                "overlay2": "Administered",
                "img": "https://images.unsplash.com/photo-1605289982774-9a6fef564df8?auto=format&fit=crop&w=800&q=80",
                "verified": "Apex Clinic",
                "bboxes": [{"type": "yellow", "text": "FluZone 0.5mL", "bottom": "40%", "left": "20%"}],
                "dialog": {"drug": "FluZone Quadrivalent", "strength": "0.5mL", "prescriber": "Apex Clinic Staff", "substrate": "Printed Cardstock", "batch": "Lot: 9942Z"}
            }
        ]
    }
]

# Handle Dialogs
if st.session_state.selected_card:
    for s in health_sections:
        for c in s['cards']:
            if c['title'] == st.session_state.selected_card:
                show_lightbox(c)
                st.session_state.selected_card = None


# Rendering
if selected_nav == "🖼️ Photos":
    st.markdown('<div style="background-color: #f1f3f4; border-radius: 24px; padding: 10px 16px; color: #9aa0a6; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🔍</span> Search your photos, albums, and health records</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-weight: 500; color:#202124;'>Timeline</h4>", unsafe_allow_html=True)
    cols = st.columns(4)
    mixed = family_photos + [c['img'] for s in health_sections for c in s['cards']]
    import random
    random.seed(42)
    random.shuffle(mixed)
    for i, img in enumerate(mixed):
        with cols[i % 4]:
            st.markdown(f'<div class="legacy-img-container"><img src="{img}"></div>', unsafe_allow_html=True)

elif selected_nav == "🏥 Health Cabinet":
    
    # 1. Global Search Bar
    st.text_input("Search", key="search_query_input", placeholder="🔍 Search your photos, albums, and health records...", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    
    query = st.session_state.get('search_query', 'metformin')
    query_map = {
        'metformin': 'Metformin 500mg',
        'script': 'Rx Doctor Script',
        'lab': 'Lab Blood Reports',
        'receipt': 'Pharmacy Receipts'
    }
    display_query = query_map.get(query, query)
    
    # 2. Toggle Buttons Row (Directly below search bar)
    col_query, col_mode2 = st.columns([7, 2])
    with col_query:
        if query:
            st.markdown(f'<div style="background-color:#f1f3f4; padding:6px 12px; border-radius:16px; color:#202124; font-size:14px; display:inline-block; border:1px solid #dadce0;">🔍 {display_query} &nbsp; <span style="color:#5f6368; cursor:pointer;">✖</span></div>', unsafe_allow_html=True)
        else:
            st.empty()
        
    with col_mode2:
        css = "toggle-active" if st.session_state.health_mode == "lens" else ""
        st.markdown(f'<div class="{css}" style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
        st.button("🏥 Health Cabinet AI Lens", on_click=set_mode, args=("lens",), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Filter Chips Row
    c1, c2, c3, c4, c5 = st.columns([1.2, 1.2, 1.2, 1.2, 3])
    c1.button("💊 Substrate: Silver Foil", on_click=set_search, args=("metformin",))
    c2.button("✍️ Rx Doctor Script", on_click=set_search, args=("script",))
    c3.button("🩸 Lab Blood Reports", on_click=set_search, args=("lab",))
    c4.button("🧾 Pharmacy Receipts", on_click=set_search, args=("receipt",))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.health_mode == "lens":
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; padding-bottom: 10px; margin-bottom: 20px;"><span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">⚡ 22ms Latency</span> &nbsp; <span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">🛡️ 0% Clutter Leakage</span> &nbsp; <span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">🎯 Match: Clinical Records</span></div>', unsafe_allow_html=True)
        st.info("🛡️ **18 personal & family photos quarantined** from clinical stream • 8 clinical health records isolated & authenticated")
        
        for section in health_sections:
            filtered_cards = section["cards"]
            if query == "metformin":
                filtered_cards = [c for c in filtered_cards if "metformin" in c["title"].lower() or "metformin" in c.get("tag","").lower()]
            elif query == "script":
                filtered_cards = [c for c in filtered_cards if "rx" in c["title"].lower() or "script" in c.get("overlay1","").lower()]
            elif query == "lab":
                filtered_cards = [c for c in filtered_cards if "lab" in c["title"].lower() or "panel" in c["title"].lower()]
            elif query == "receipt":
                filtered_cards = [c for c in filtered_cards if "receipt" in c.get("overlay1","").lower() or "invoice" in c["title"].lower()]
                
            if not filtered_cards:
                continue
                
            st.markdown(f"<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>{section['date_header']}</h4>", unsafe_allow_html=True)
            cols = st.columns(4)
            for i, c in enumerate(filtered_cards):
                with cols[i % 4]:
                    bboxes_html = ""
                    for bbox in c.get("bboxes", []):
                        top = f"top: {bbox.get('top', 'auto')};"
                        bottom = f"bottom: {bbox.get('bottom', 'auto')};"
                        left = f"left: {bbox.get('left', 'auto')};"
                        right = f"right: {bbox.get('right', 'auto')};"
                        bboxes_html += f"""<div class="bbox {bbox['type']}" style="{top} {bottom} {left} {right}">{bbox['text']}</div>"""
                    
                    st.markdown(f"""
                    <div class="evidence-card">
                        <div class="card-img-container">
                            <img src="{c['img']}">
                            {bboxes_html}
                            <div class="card-hover-actions">
                                <div class="hover-icon">✔️</div>
                                <div class="hover-icon">⭐</div>
                            </div>
                            <div class="card-tag">{c['tag']}</div>
                            <div class="card-overlay">
                                <div class="overlay-pill">{c['overlay1']}</div>
                                <div class="overlay-pill" style="color:#1a73e8; border-color:#1a73e8;">{c['overlay2']}</div>
                            </div>
                        </div>
                        <div class="card-content">
                            <div class="card-title">{c['title']}</div>
                            <div class="card-subtitle">{c['subtitle']}</div>
                            <div class="verified-pill">✔️ {c['verified']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.button("🔍 Open Lightbox", key=f"btn_{c['title']}", on_click=open_lightbox, args=(c['title'],), use_container_width=True)

    else:
        # Legacy Mode (Failure State)
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; padding-bottom: 10px; margin-bottom: 20px;"><span style="background: rgba(242,139,130,0.1); color: #f28b82; padding: 4px 8px; border-radius: 12px;">⏱️ 4,200ms latency</span> &nbsp; <span style="background: rgba(242,139,130,0.1); color: #f28b82; padding: 4px 8px; border-radius: 12px;">⚠️ 48.0% Personal Contamination</span> &nbsp; <span style="background: rgba(242,139,130,0.1); color: #f28b82; padding: 4px 8px; border-radius: 12px;">No Exact Entity Match</span></div>', unsafe_allow_html=True)
        st.warning("Showing 12 unranked results for search • Personal family media and food snapshots included")
        
        st.markdown(f"<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>Search Results</h4>", unsafe_allow_html=True)
        cols = st.columns(4)
        
        mixed = [health_sections[0]['cards'][0]['img'], family_photos[0], family_photos[1], health_sections[0]['cards'][1]['img'], family_photos[2], health_sections[0]['cards'][2]['img'], family_photos[3], health_sections[1]['cards'][0]['img']]
        for i, img in enumerate(mixed):
            with cols[i % 4]:
                st.markdown(f'<div class="legacy-img-container"><img src="{img}"></div>', unsafe_allow_html=True)

elif selected_nav == "🧭 Explore":
    st.markdown("<h3 style='color:#202124; margin-bottom: 24px;'>Explore</h3>", unsafe_allow_html=True)
    
    # People
    st.markdown("<h5 style='color:#5f6368; margin-top: 20px; margin-bottom: 16px;'>People & pets</h5>", unsafe_allow_html=True)
    faces = [
        'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
        'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
        'https://images.unsplash.com/photo-1544005313-94ddf0286df2',
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
        'https://images.unsplash.com/photo-1517841905240-472988babdf9'
    ]
    people_html = ''
    for face in faces:
        people_html += f'<img src="{face}?auto=format&fit=crop&w=150&h=150&q=80" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-right: 16px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">'
    st.markdown(f"<div>{people_html}</div>", unsafe_allow_html=True)
    
    # Places
    st.markdown("<h5 style='color:#5f6368; margin-top: 40px; margin-bottom: 16px;'>Places</h5>", unsafe_allow_html=True)
    places = {
        'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9': 'New York',
        'https://images.unsplash.com/photo-1501594907352-04cda38ebc29': 'San Francisco',
        'https://images.unsplash.com/photo-1494522855154-9297ac14b55f': 'Chicago'
    }
    places_html = ''
    for place, name in places.items():
        places_html += f'<div style="display:inline-block; margin-right: 16px; cursor: pointer; border-radius: 12px; overflow: hidden; width: 120px; height: 160px; position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><img src="{place}?auto=format&fit=crop&w=200&h=300&q=80" style="width: 100%; height: 100%; object-fit: cover;"><div style="position: absolute; bottom: 8px; left: 8px; color: white; font-weight: 500; font-size: 14px; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">{name}</div></div>'
    st.markdown(f"<div>{places_html}</div>", unsafe_allow_html=True)
    
    # Things
    st.markdown("<h5 style='color:#5f6368; margin-top: 40px; margin-bottom: 16px;'>Things</h5>", unsafe_allow_html=True)
    things = {
        'https://images.unsplash.com/photo-1631549916768-4119b2e5f926': 'Prescriptions',
        'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d': 'Lab Reports',
        'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c': 'Receipts',
        'https://images.unsplash.com/photo-1504674900247-0877df9cc836': 'Food',
        'https://images.unsplash.com/photo-1519331379826-f10be5486c6f': 'Parks'
    }
    things_html = ''
    for thing, name in things.items():
        things_html += f'<div style="display:inline-block; margin-right: 16px; margin-bottom: 16px; cursor: pointer; border-radius: 12px; overflow: hidden; width: 120px; height: 120px; position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><img src="{thing}?auto=format&fit=crop&w=200&h=200&q=80" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.8);"><div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 500; font-size: 14px; text-align: center; text-shadow: 0 1px 3px rgba(0,0,0,0.9);">{name}</div></div>'
    st.markdown(f"<div>{things_html}</div>", unsafe_allow_html=True)

elif selected_nav == "👥 Sharing":
    st.markdown("<h3 style='color:#202124; margin-bottom: 24px;'>Sharing</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#5f6368; margin-bottom: 16px;'>Shared with you</h5>", unsafe_allow_html=True)
    st.info("Dr. Sarah Chen has shared 2 clinical documents with you.")
    
    st.markdown("<h5 style='color:#5f6368; margin-top: 24px; margin-bottom: 16px;'>Caregiver Access</h5>", unsafe_allow_html=True)
    st.markdown('''
    <div style="display:flex; align-items:center; padding:16px; border:1px solid #dadce0; border-radius:12px; max-width:600px;">
        <div style="width:48px; height:48px; border-radius:50%; background:#1a73e8; color:white; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:600; margin-right:16px;">SC</div>
        <div>
            <div style="font-weight:600; color:#202124;">Dr. Sarah Chen (Primary Care)</div>
            <div style="color:#5f6368; font-size:14px;">Can view Health Cabinet Lens only</div>
        </div>
        <div style="margin-left:auto; color:#1a73e8; font-weight:600; cursor:pointer;">Manage</div>
    </div>
    ''', unsafe_allow_html=True)

elif selected_nav == "📚 Albums":
    st.markdown("<h3 style='color:#202124; margin-bottom: 24px;'>Albums</h3>", unsafe_allow_html=True)
    albums = {
        '2024 Lab Reports': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d',
        'Summer Vacation': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e',
        'Prescriptions': 'https://images.unsplash.com/photo-1631549916768-4119b2e5f926',
        'Family': 'https://images.unsplash.com/photo-1511895426328-dc8714191300'
    }
    cols = st.columns(4)
    for i, (name, img) in enumerate(albums.items()):
        with cols[i % 4]:
            st.markdown(f'''
            <div style="margin-bottom:24px; cursor:pointer;">
                <div style="width:100%; aspect-ratio:1; border-radius:12px; overflow:hidden; margin-bottom:8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <img src="{img}?auto=format&fit=crop&w=400&h=400&q=80" style="width:100%; height:100%; object-fit:cover;">
                </div>
                <div style="font-weight:500; color:#202124;">{name}</div>
            </div>
            ''', unsafe_allow_html=True)

elif selected_nav == "📄 Documents":
    st.markdown("<h3 style='color:#202124; margin-bottom: 24px;'>Documents</h3>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; gap:16px; margin-bottom:24px;'><div style='padding:8px 16px; background:#e8f0fe; color:#1a73e8; border-radius:20px; font-weight:500; cursor:pointer;'>All</div><div style='padding:8px 16px; background:#f1f3f4; color:#5f6368; border-radius:20px; font-weight:500; cursor:pointer;'>Medical</div><div style='padding:8px 16px; background:#f1f3f4; color:#5f6368; border-radius:20px; font-weight:500; cursor:pointer;'>Receipts</div><div style='padding:8px 16px; background:#f1f3f4; color:#5f6368; border-radius:20px; font-weight:500; cursor:pointer;'>IDs</div></div>", unsafe_allow_html=True)
    docs = [
        'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d',
        'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c',
        'https://images.unsplash.com/photo-1638202993928-7267aad84c31',
        'https://images.unsplash.com/photo-1505751172876-fa1923c5c528'
    ]
    cols = st.columns(4)
    for i, img in enumerate(docs):
        with cols[i % 4]:
            st.markdown(f'<div style="width:100%; aspect-ratio:3/4; border-radius:8px; overflow:hidden; margin-bottom:20px; border:1px solid #dadce0;"><img src="{img}?auto=format&fit=crop&w=400&h=533&q=80" style="width:100%; height:100%; object-fit:cover;"></div>', unsafe_allow_html=True)

elif selected_nav == "🗑️ Trash":
    st.markdown("<h3 style='color:#202124; margin-bottom: 24px;'>Trash</h3>", unsafe_allow_html=True)
    st.markdown("<div style='padding:12px; background:#f1f3f4; color:#5f6368; border-radius:8px; font-size:14px; margin-bottom:24px;'>Items in trash will be permanently deleted after 60 days</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#5f6368; font-style:italic;'>No items in trash.</div>", unsafe_allow_html=True)
