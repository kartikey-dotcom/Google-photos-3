import streamlit as st
import json

st.set_page_config(layout="wide", page_title="Google Photos: Vibes")

# Custom CSS for a beautiful, premium, consumer gallery look
st.markdown("""
<style>
    /* Premium background and typography */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Vibe Title */
    .vibe-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #f472b6, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .vibe-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Image Cards */
    .vibe-card {
        border-radius: 16px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        position: relative;
    }
    .vibe-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
    }
    .vibe-card img {
        width: 100%;
        display: block;
        border-radius: 16px;
    }
    
    .vibe-label {
        position: absolute;
        bottom: 12px;
        left: 12px;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(4px);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        with open("vibe_assets.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

assets = load_data()

# Header
st.markdown('<div class="vibe-title">✨ AI Vibe Albums</div>', unsafe_allow_html=True)
st.markdown('<div class="vibe-subtitle">Google Photos now automatically curates your memories by their aesthetic mood, lighting, and cinematic feel.</div>', unsafe_allow_html=True)

if not assets:
    st.warning("No assets found. Please run `generate_assets.py` to create the mock data.")
    st.stop()

# Get unique vibes
vibes = sorted(list(set([a["vibe"] for a in assets])))

# Vibe Selector
selected_vibe = st.radio("Select an Aesthetic Mood:", ["All Vibes"] + vibes, horizontal=True)

st.markdown("---")

# Filter assets
if selected_vibe == "All Vibes":
    display_assets = assets
else:
    display_assets = [a for a in assets if a["vibe"] == selected_vibe]

if selected_vibe != "All Vibes":
    st.subheader(f"Mood: {selected_vibe} 🎨")
else:
    st.subheader("Your Entire Gallery")

# Masonry-like grid using columns
cols = st.columns(4)
for i, asset in enumerate(display_assets):
    with cols[i % 4]:
        # Wrap image in custom HTML for the hover effects and overlay badges
        st.markdown(f"""
        <div class="vibe-card">
            <img src="{asset['url']}" alt="{asset['vibe']}">
            <div class="vibe-label">✨ {asset['vibe']}</div>
        </div>
        """, unsafe_allow_html=True)
