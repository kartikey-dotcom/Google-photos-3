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
if "show_pharmacist_mode" not in st.session_state:
    st.session_state.show_pharmacist_mode = False

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

def open_quick_scan():
    st.session_state.show_pharmacist_mode = True

@st.dialog("Pharmacist Quick-Scan Mode", width="large")
def show_pharmacist_modal():
    cols = st.columns([3, 2])
    with cols[0]:
        st.image("https://images.unsplash.com/photo-1584308666744-24d5e4708709?auto=format&fit=crop&w=1200&q=100", use_column_width=True)
    with cols[1]:
        st.markdown("<h2 style='color:#1a73e8; margin-bottom:0;'>METFORMIN 500MG ER</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#5f6368; margin-top:0;'>Hydrochloride Extended Release</h4>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<b>Prescribing Doctor:</b> Dr. R. Mehta", unsafe_allow_html=True)
        st.markdown("<b>Clinic:</b> Apollo Health Pharmacy Dispense", unsafe_allow_html=True)
        st.markdown("<b>Date of Issue:</b> Oct 28, 2024", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background:#f1f3f4; padding:12px; border-radius:8px; border:1px solid #dadce0;">
            <div style="font-size:12px; color:#5f6368;">Extracted Batch / License</div>
            <div style="font-size:18px; font-weight:700; font-family:monospace; color:#202124; display:flex; justify-content:space-between; align-items:center;">
                LOT: 4B391
                <span style="font-size:14px; background:#ffffff; border:1px solid #dadce0; padding:4px 8px; border-radius:4px; cursor:pointer;">📋 Copy</span>
            </div>
            <div style="font-size:18px; font-weight:700; font-family:monospace; color:#202124; display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                EXP: 11/2025
                <span style="font-size:14px; background:#ffffff; border:1px solid #dadce0; padding:4px 8px; border-radius:4px; cursor:pointer;">📋 Copy</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("Close Quick-Scan", use_container_width=True):
        st.session_state.show_pharmacist_mode = False
        st.rerun()

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

# Inject Custom CSS (Light Theme MD3 + Zoom logic)
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
    
    /* Action Dock */
    .action-dock {
        position: fixed;
        bottom: 0;
        right: 0;
        width: calc(100% - 244px);
        background-color: #ffffff;
        border-top: 1px solid #dadce0;
        padding: 16px 32px;
        z-index: 999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    @media (max-width: 768px) {
        .action-dock { width: 100%; }
    }
    
    /* Primary Dock Button */
    .btn-primary {
        background-color: #1a73e8 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 8px 24px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
    }
    .btn-primary:hover {
        background-color: #1765cc !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
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
        background-color: #e0e0e0;
        overflow: hidden;
    }
    .card-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Macro Zoom Class */
    .macro-zoom > img {
        transform: scale(2.5) translate(0%, -5%);
        transform-origin: center;
        filter: contrast(1.1) sharpen(1.2);
    }
    
    .mini-map {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 44px;
        height: 44px;
        border: 2px solid #ffffff;
        border-radius: 4px;
        background-color: #000;
        overflow: hidden;
        z-index: 10;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .mini-map img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.8;
    }
    .mini-map-indicator {
        position: absolute;
        top: 35%;
        left: 40%;
        width: 25%;
        height: 25%;
        border: 1px solid #34a853;
        box-shadow: 0 0 6px #34a853;
        background-color: rgba(52, 168, 83, 0.4);
    }
    
    /* Hover Actions (Checkmark and Star) */
    .card-hover-actions {
        position: absolute;
        top: 10px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 10px;
        opacity: 0.8;
        z-index: 15;
    }
    .hover-icon {
        background: rgba(255,255,255,0.9);
        color: #5f6368;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        border: 1px solid #dadce0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
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
        z-index: 15;
    }
    .card-overlay {
        position: absolute;
        bottom: 10px;
        left: 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        z-index: 15;
        align-items: flex-start;
    }
    .overlay-pill {
        background-color: rgba(255,255,255,0.95);
        color: #202124;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid var(--border);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .card-content { padding: 16px; }
    .card-title { font-size: 16px; font-weight: 600; margin-bottom: 4px; color: var(--text-main); }
    .card-subtitle { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
    
    /* Legacy Simple Grid */
    .legacy-img-container { width: 100%; aspect-ratio: 16/9; overflow: hidden; margin-bottom: 20px; border-radius: 12px; }
    .legacy-img-container img { width: 100%; height: 100%; object-fit: cover; }
    
    /* Hide bottom padding so dock doesnt overlay text */
    .block-container { padding-bottom: 100px !important; }
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
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 16px; border-radius: 12px; font-size: 12px; border: 1px solid #dadce0;">
        <span style="color:#202124; font-weight: 600;">👥 Caregiver Sharing</span><br>
        <span style="color:#5f6368;">Dr. Sarah Chen, Mark D.</span><br>
        <div style="margin-top: 8px; color:#1a73e8; cursor:pointer; font-weight:600;">Manage Access</div>
    </div>
    """, unsafe_allow_html=True)

# Data
family_photos = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?auto=format&fit=crop&w=400&q=80",
]

legacy_decoys = [
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=400&q=80", # Birthday Cake
    "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80", # Grocery produce/receipt
    "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=400&q=80", # Blurred Dog
    "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=400&q=80"  # Outdoor Park
]

health_sections = [
    {
        "date_header": "October 2024 • Recent Clinical Records & Prescriptions",
        "cards": [
            {
                "title": "Metformin HCl 500mg",
                "subtitle": "Oct 28, 2024 • Apollo Pharmacy Dispense",
                "tag": "METFORMIN 500MG ER",
                "overlay1": "Verified Salt: Metformin HCl ER",
                "overlay1_color": "#1a73e8",
                "overlay2": "Exp: Nov 2025",
                "img": "https://images.unsplash.com/photo-1584308666744-24d5e4708709?auto=format&fit=crop&w=800&q=80",
                "verified": "● Active Refill (30 Days)",
                "verified_color": "#0f9d58",
                "verified_bg": "#e6f4ea",
                "macro": True,
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
                "overlay1": "Verified Salt: Telmisartan 40mg",
                "overlay1_color": "#1a73e8",
                "overlay2": "1 Tab Daily OD",
                "img": "https://images.unsplash.com/photo-1583324113626-70df0f4deaab?auto=format&fit=crop&w=800&q=80",
                "verified": "● Active Refill (30 Days)",
                "verified_color": "#0f9d58",
                "verified_bg": "#e6f4ea",
                "macro": True,
                "dialog": {"drug": "Telmisartan", "strength": "40mg", "prescriber": "Dr. A. R. Khan", "substrate": "Handwritten Script", "batch": "N/A"}
            },
            {
                "title": "Metabolic & HbA1c Panel",
                "subtitle": "Oct 26, 2024 • Metropolis Healthcare Labs",
                "tag": "HBA1C: 7.2% (ELEVATED)",
                "overlay1": "Substrate: Lab Report",
                "overlay2": "⚠️ High: Above Target (4.0-5.6%)",
                "overlay2_color": "#b06000",
                "overlay2_bg": "#fef7e0",
                "img": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=800&q=80",
                "verified": "Metropolis Healthcare Labs",
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
                "dialog": {"drug": "Diagnostic Blood Panel", "strength": "N/A", "prescriber": "Dr. Sarah Chen", "substrate": "A4 Print with Blue Seal", "batch": "SID: 8849201"}
            },
            {
                "title": "Pharmacy Register Receipt",
                "subtitle": "Oct 16, 2024 • Total $65.03 Paid",
                "tag": "CITY DRUG PHARMACY",
                "overlay1": "Substrate: Thermal Paper",
                "overlay2": "Non-Prescription Cash Receipt ($65.03)",
                "img": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
                "verified": "Fiscal Non-Clinical Slip",
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
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
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
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
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
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
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
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
                "verified_color": "#5f6368",
                "verified_bg": "#f1f3f4",
                "macro": False,
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

if st.session_state.show_pharmacist_mode:
    show_pharmacist_modal()

# Rendering
if selected_nav == "🖼️ Photos":
    st.markdown('<div style="background-color: #f1f3f4; border-radius: 24px; padding: 10px 16px; color: #5f6368; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🔍</span> Search your photos, albums, and health records</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-weight: 500; color:#202124;'>Timeline</h4>", unsafe_allow_html=True)
    cols = st.columns(4)
    mixed = family_photos + legacy_decoys + [c['img'] for s in health_sections for c in s['cards']]
    import random
    random.seed(42)
    random.shuffle(mixed)
    for i, img in enumerate(mixed):
        with cols[i % 4]:
            st.markdown(f'<div class="legacy-img-container"><img src="{img}"></div>', unsafe_allow_html=True)

elif selected_nav == "🏥 Health Cabinet":
    
    # Search and Toggle Bar
    st.text_input("Search", key="search_query_input", placeholder="🔍 Search your photos, albums, and health records...", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chips, col_mode1, col_mode2 = st.columns([5, 1.5, 1.5])
    with col_chips:
        c1, c2, c3, c4 = st.columns(4)
        c1.button("💊 Substrate: Silver Foil", on_click=set_search, args=("metformin",))
        c2.button("✍️ Rx Doctor Script", on_click=set_search, args=("script",))
        c3.button("🩸 Lab Blood Reports", on_click=set_search, args=("lab",))
        c4.button("🧾 Pharmacy Receipts", on_click=set_search, args=("receipt",))
        
    with col_mode1:
        css = "toggle-active" if st.session_state.health_mode == "legacy" else ""
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        st.button("📸 Photos Legacy Search -8.2s delay", on_click=set_mode, args=("legacy",))
        st.markdown('</div>', unsafe_allow_html=True)
    with col_mode2:
        css = "toggle-active" if st.session_state.health_mode == "lens" else ""
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        st.button("🏥 Health Cabinet AI Lens", on_click=set_mode, args=("lens",))
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.health_mode == "lens":
        st.markdown('<div style="font-size: 12px; color: #5f6368; padding-bottom: 10px; margin-bottom: 20px;"><span style="background: rgba(26,115,232,0.1); color: #1a73e8; padding: 4px 8px; border-radius: 12px;">⚡ 22ms Latency</span> &nbsp; <span style="background: rgba(26,115,232,0.1); color: #1a73e8; padding: 4px 8px; border-radius: 12px;">🛡️ 0% Clutter Leakage</span> &nbsp; <span style="background: rgba(26,115,232,0.1); color: #1a73e8; padding: 4px 8px; border-radius: 12px;">🎯 Match: Clinical Records</span></div>', unsafe_allow_html=True)
        st.info("🛡️ **18 personal & family photos quarantined** from clinical stream • 8 clinical health records isolated & authenticated")
        
        for section in health_sections:
            st.markdown(f"<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>{section['date_header']}</h4>", unsafe_allow_html=True)
            cols = st.columns(4)
            for i, c in enumerate(section["cards"]):
                with cols[i % 4]:
                    # Macro Zoom Logic
                    macro_class = "macro-zoom" if c.get("macro") else ""
                    minimap_html = ""
                    if c.get("macro"):
                        minimap_html = f"""
                        <div class="mini-map">
                            <img src="{c['img']}">
                            <div class="mini-map-indicator"></div>
                        </div>
                        """
                        
                    # Overlay Logic
                    c1_bg = c.get("overlay1_bg", "rgba(255,255,255,0.95)")
                    c1_col = c.get("overlay1_color", "#202124")
                    c2_bg = c.get("overlay2_bg", "rgba(255,255,255,0.95)")
                    c2_col = c.get("overlay2_color", "#202124")
                    
                    st.markdown(f"""
                    <div class="evidence-card">
                        <div class="card-img-container {macro_class}">
                            <img src="{c['img']}">
                            {minimap_html}
                            <div class="card-hover-actions">
                                <div class="hover-icon">✔️</div>
                                <div class="hover-icon">⭐</div>
                            </div>
                            <div class="card-tag">{c['tag']}</div>
                            <div class="card-overlay">
                                <div class="overlay-pill" style="color:{c1_col}; background:{c1_bg};">{c['overlay1']}</div>
                                <div class="overlay-pill" style="color:{c2_col}; background:{c2_bg};">{c['overlay2']}</div>
                            </div>
                        </div>
                        <div class="card-content">
                            <div class="card-title">{c['title']}</div>
                            <div class="card-subtitle">{c['subtitle']}</div>
                            <div style="font-size: 11px; font-weight: 600; color: {c['verified_color']}; background: {c['verified_bg']}; padding: 4px 8px; border-radius: 12px; display: inline-block; margin-bottom: 12px;">{c['verified']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.button("🔍 Open Lightbox", key=f"btn_{c['title']}", on_click=open_lightbox, args=(c['title'],), use_container_width=True)

        # Bottom Dock for Actions
        st.markdown("""
        <div class="action-dock">
            <div style="font-weight: 600; color: #202124;">Selected Evidence: 2 Items Ready for Pharmacist Review</div>
        </div>
        """, unsafe_allow_html=True)
        # We overlay buttons by using a container positioned absolutely via css hack, or just render it inline.
        # Since Streamlit makes fixed positioning of interactive widgets hard, we'll just render it at the bottom.
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.markdown("<div style='padding-top:10px; font-weight:600; font-size:16px; color:#202124;'>Selected Evidence: 2 Items Ready for Pharmacist Review</div>", unsafe_allow_html=True)
        with col2:
            st.button("Share Caregiver Summary", use_container_width=True)
        with col3:
            st.button("⚡ Show Pharmacist Quick-Scan Mode", type="primary", use_container_width=True, on_click=open_quick_scan)

    else:
        # Legacy Mode (Failure State)
        st.markdown('<div style="font-size: 12px; color: #5f6368; padding-bottom: 10px; margin-bottom: 20px;"><span style="background: rgba(242,139,130,0.1); color: #d93025; padding: 4px 8px; border-radius: 12px;">⏱️ 4,200ms latency</span> &nbsp; <span style="background: rgba(242,139,130,0.1); color: #d93025; padding: 4px 8px; border-radius: 12px;">⚠️ 50.0% Personal Media Leakage</span> &nbsp; <span style="background: rgba(242,139,130,0.1); color: #d93025; padding: 4px 8px; border-radius: 12px;">Standard Wide Framing (No Macro OCR)</span></div>', unsafe_allow_html=True)
        st.warning("Showing 12 unranked results for search • Personal family media and food snapshots included")
        
        st.markdown(f"<h4 style='font-weight: 500; color:#202124; margin-top:20px;'>Search Results</h4>", unsafe_allow_html=True)
        cols = st.columns(4)
        
        # Inject the 4 requested decoys in the top row explicitly
        mixed = legacy_decoys + [health_sections[0]['cards'][0]['img'], family_photos[0], health_sections[0]['cards'][1]['img'], health_sections[1]['cards'][0]['img']]
        for i, img in enumerate(mixed):
            with cols[i % 4]:
                st.markdown(f'<div class="legacy-img-container"><img src="{img}"></div>', unsafe_allow_html=True)

else:
    st.info(f"You selected {selected_nav}. This is a placeholder for the MVP.")
