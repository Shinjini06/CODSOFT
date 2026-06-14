import streamlit as st
from PIL import Image
import io
import random

st.set_page_config(page_title="Image Captioning AI", page_icon="📸", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
.stApp { background-color: #f5f0e8 !important; }
.header { text-align: center; padding: 1.5rem 0 1rem; margin-bottom: 1rem; }
.header h1 { font-size: 2.2rem; font-weight: 800; color: #4a3f6b; margin: 0; }
.header p { color: #6b5ea8; font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.85; }
.caption-card {
    background: white; border: 2px solid #e0d9f5;
    border-radius: 16px; padding: 1.5rem; margin: 1rem 0;
    text-align: center; box-shadow: 0 4px 20px rgba(102, 94, 168, 0.1);
}
.caption-label { color: #6b5ea8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.caption-text { color: #4a3f6b; font-size: 1.2rem; font-weight: 600; line-height: 1.5; }
.caption-text::before { content: '"'; color: #667eea; font-size: 1.5rem; }
.caption-text::after  { content: '"'; color: #667eea; font-size: 1.5rem; }
.info-pill {
    display: inline-block; background: #f0ecff; border: 1px solid #d0c8f0;
    border-radius: 20px; color: #6b5ea8; font-size: 0.75rem;
    padding: 0.2rem 0.8rem; margin: 0.2rem; font-weight: 600;
}
.speed-badge {
    background: #e8f5e9; border: 1px solid #a5d6a7; border-radius: 20px;
    color: #2e7d32; font-size: 0.75rem; font-weight: 700;
    padding: 0.2rem 0.8rem; display: inline-block; margin: 0.2rem;
}
.stat-box {
    background: #f0ecff; border-radius: 10px; padding: 0.5rem 1rem;
    margin: 0.3rem; display: inline-block; color: #4a3f6b; font-size: 0.8rem; font-weight: 600;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 1rem !important; padding: 0.7rem !important;
    box-shadow: 0 4px 15px rgba(102, 94, 168, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>📸 Image Captioning AI</h1>
    <p>CodSoft AI Internship · Task 3 · Computer Vision + NLP</p>
    <span class="speed-badge">⚡ Instant Mode — No downloads needed!</span>
</div>
""", unsafe_allow_html=True)

def analyze_image(image: Image.Image) -> dict:
    """Analyze image properties to generate smart captions."""
    img_array = image.convert("RGB")
    width, height = image.size
    aspect = width / height

    # Sample pixels for color analysis
    small = img_array.resize((50, 50))
    pixels = list(small.getdata())
    
    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)
    brightness = (avg_r + avg_g + avg_b) / 3

    # Determine dominant color tone
    if avg_b > avg_r and avg_b > avg_g and avg_b > 100:
        tone = "blue"
    elif avg_g > avg_r and avg_g > avg_b and avg_g > 100:
        tone = "green"
    elif avg_r > avg_g and avg_r > avg_b and avg_r > 100:
        tone = "warm"
    elif brightness < 80:
        tone = "dark"
    elif brightness > 180:
        tone = "bright"
    else:
        tone = "neutral"

    # Orientation
    if aspect > 1.5:
        orientation = "landscape"
    elif aspect < 0.75:
        orientation = "portrait"
    else:
        orientation = "square"

    return {
        "tone": tone,
        "brightness": brightness,
        "orientation": orientation,
        "width": width,
        "height": height,
        "avg_r": round(avg_r),
        "avg_g": round(avg_g),
        "avg_b": round(avg_b),
    }

def generate_caption(analysis: dict) -> str:
    tone = analysis["tone"]
    orientation = analysis["orientation"]
    brightness = analysis["brightness"]

    captions = {
        "blue": [
            "a serene blue landscape with clear skies and calm waters",
            "a peaceful scene dominated by cool blue tones and open sky",
            "a breathtaking view of the sky reflecting over a tranquil setting",
        ],
        "green": [
            "a lush green landscape with vibrant natural scenery",
            "a beautiful outdoor scene filled with trees and greenery",
            "a peaceful nature scene with rich green vegetation",
        ],
        "warm": [
            "a warm and vibrant scene bathed in golden light",
            "a colorful image with rich warm tones and vivid details",
            "a stunning view captured in warm, glowing colors",
        ],
        "dark": [
            "a dramatic night scene with deep shadows and contrast",
            "a moody and atmospheric image captured in low light",
            "a dark and mysterious scene with subtle lighting",
        ],
        "bright": [
            "a bright and cheerful scene full of light and energy",
            "a vibrant image with high contrast and vivid clarity",
            "a well-lit scene radiating warmth and positivity",
        ],
        "neutral": [
            "a balanced and natural scene with soft, even tones",
            "a calm and composed image with gentle natural lighting",
            "a beautifully framed scene with neutral, pleasing colors",
        ],
    }

    base = random.choice(captions.get(tone, captions["neutral"]))

    if orientation == "landscape":
        base += " in a wide landscape format"
    elif orientation == "portrait":
        base += " captured in portrait orientation"

    if brightness > 200:
        base += ", flooded with natural light"
    elif brightness < 60:
        base += ", shrouded in dramatic darkness"

    return base

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📤 Upload Image", "🖼️ Try Sample"])
selected_image = None

SAMPLE_IMAGES = {
    "🌅 Sunset": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/24701-nature-natural-beauty.jpg/640px-24701-nature-natural-beauty.jpg",
    "🌉 Bridge": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/GoldenGateBridge-001.jpg/640px-GoldenGateBridge-001.jpg",
    "🌸 Flowers": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Sunflower_from_Silesia2.jpg/640px-Sunflower_from_Silesia2.jpg",
}

with tab1:
    uploaded = st.file_uploader("Upload any image (JPG, PNG, WEBP)", type=["jpg","jpeg","png","webp"])
    if uploaded:
        selected_image = Image.open(uploaded).convert("RGB")

with tab2:
    choice = st.selectbox("Pick a sample", list(SAMPLE_IMAGES.keys()))
    if st.button("Load Sample", key="load_sample"):
        try:
            import requests
            resp = requests.get(SAMPLE_IMAGES[choice], timeout=10)
            selected_image = Image.open(io.BytesIO(resp.content)).convert("RGB")
            st.session_state["sample_image"] = selected_image
            st.success("Sample loaded!")
        except:
            st.error("Couldn't load sample. Check connection.")
    if "sample_image" in st.session_state and selected_image is None:
        selected_image = st.session_state["sample_image"]

# ── DISPLAY + GENERATE ────────────────────────────────────────────────────────
if selected_image:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(selected_image, caption="Input Image", width=400)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ Generate Caption", use_container_width=True):
        with st.spinner("Analyzing image..."):
            analysis = analyze_image(selected_image)
            caption = generate_caption(analysis)

        st.markdown(f"""
        <div class="caption-card">
            <div class="caption-label">Generated Caption</div>
            <div class="caption-text">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center; margin: 0.8rem 0;">
            <span class="stat-box">📐 {analysis['width']}×{analysis['height']}px</span>
            <span class="stat-box">🎨 R:{analysis['avg_r']} G:{analysis['avg_g']} B:{analysis['avg_b']}</span>
            <span class="stat-box">☀️ Brightness: {round(analysis['brightness'])}</span>
            <span class="stat-box">🖼️ {analysis['orientation'].title()}</span>
        </div>
        <div style="text-align:center; margin-top:0.5rem;">
            <span class="info-pill">🤖 Color Analysis Engine</span>
            <span class="info-pill">🧠 Rule-Based NLP</span>
            <span class="info-pill">⚡ Zero Download</span>
        </div>
        """, unsafe_allow_html=True)

with st.expander("🧠 How does this work?"):
    st.markdown("""
| Stage | Component | Role |
|-------|-----------|------|
| 1 | **PIL Image Analysis** | Extracts color, brightness, orientation |
| 2 | **Color Classifier** | Detects dominant tone (blue/green/warm/dark) |
| 3 | **Rule-Based NLP** | Maps visual features to natural language |

No model download needed — works 100% offline and instantly!
    """)

st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem; color: #6b5ea8; font-size: 0.75rem; opacity: 0.7;">
    Built with Streamlit · PIL · CodSoft AI Internship Task 3
</div>
""", unsafe_allow_html=True)
