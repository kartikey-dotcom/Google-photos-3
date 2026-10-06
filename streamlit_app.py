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
        --bg-color: #202124;
        --sidebar-bg: #202124;
        --text-main: #e8eaed;
        --text-muted: #9aa0a6;
        --accent: #8ab4f8;
        --border: #3c4043;
        --card-bg: #303134;
        --hover-bg: #3c4043;
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
        background-color: #394457 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] p {
        color: #d2e3fc !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:nth-child(1) { display: none !important; }
    
    /* Inputs & Buttons */
    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: #303134;
        border-radius: 24px;
        border: 1px solid transparent;
        color: var(--text-main);
    }
    [data-testid="stButton"] button {
        border-radius: 16px !important;
        padding: 4px 16px !important;
        background-color: #303134 !important;
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
        background-color: #394457 !important;
        border-color: #8ab4f8 !important;
        color: #d2e3fc !important;
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
        background-color: rgba(32,33,36,0.9);
        color: #e8eaed;
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
        background-color: rgba(32,33,36,0.9);
        color: #e8eaed;
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
    st.markdown("### 💠 Photos <span style='background:#303134; color:#9aa0a6; padding:2px 6px; border-radius:4px; font-size:10px;'>Labs</span>", unsafe_allow_html=True)
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
    <div style="padding: 16px; border-radius: 12px; font-size: 12px; border: 1px solid #3c4043;">
        <span style="color:#e8eaed; font-weight: 600;">👥 Caregiver Sharing</span><br>
        <span style="color:#9aa0a6;">Dr. Sarah Chen, Mark D.</span><br>
        <div style="margin-top: 8px; color:#8ab4f8; cursor:pointer;">Manage Access</div>
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
                "img": "https://images.unsplash.com/photo-1584308666744-24d5e4708709?auto=format&fit=crop&w=800&q=80",
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
                "img": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=800&q=80",
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
    st.markdown('<div style="background-color: #303134; border-radius: 24px; padding: 10px 16px; color: #9aa0a6; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🔍</span> Search your photos, albums, and health records</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-weight: 500; color:#e8eaed;'>Timeline</h4>", unsafe_allow_html=True)
    cols = st.columns(4)
    mixed = family_photos + [c['img'] for s in health_sections for c in s['cards']]
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
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; padding-bottom: 10px; margin-bottom: 20px;"><span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">⚡ 22ms Latency</span> &nbsp; <span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">🛡️ 0% Clutter Leakage</span> &nbsp; <span style="background: rgba(138,180,248,0.1); color: #8ab4f8; padding: 4px 8px; border-radius: 12px;">🎯 Match: Clinical Records</span></div>', unsafe_allow_html=True)
        st.info("🛡️ **18 personal & family photos quarantined** from clinical stream • 8 clinical health records isolated & authenticated")
        
        for section in health_sections:
            st.markdown(f"<h4 style='font-weight: 500; color:#e8eaed; margin-top:20px;'>{section['date_header']}</h4>", unsafe_allow_html=True)
            cols = st.columns(4)
            for i, c in enumerate(section["cards"]):
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
                                <div class="overlay-pill" style="color:#8ab4f8; border-color:#8ab4f8;">{c['overlay2']}</div>
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
        
        st.markdown(f"<h4 style='font-weight: 500; color:#e8eaed; margin-top:20px;'>Search Results</h4>", unsafe_allow_html=True)
        cols = st.columns(4)
        
        mixed = [health_sections[0]['cards'][0]['img'], family_photos[0], family_photos[1], health_sections[0]['cards'][1]['img'], family_photos[2], health_sections[0]['cards'][2]['img'], family_photos[3], health_sections[1]['cards'][0]['img']]
        for i, img in enumerate(mixed):
            with cols[i % 4]:
                st.markdown(f'<div class="legacy-img-container"><img src="{img}"></div>', unsafe_allow_html=True)

else:
    st.info(f"You selected {selected_nav}. This is a placeholder for the MVP.")
