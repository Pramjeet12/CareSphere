import streamlit as st
from streamlit_lottie import st_lottie
import requests

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

# ----------------------------
# Page Header
# ----------------------------
st.markdown("""
    <div style="text-align: center; padding-top: 20px; padding-bottom: 10px;">
        <h1 style="color: #36454F; font-size: 48px; margin-bottom: 5px;">Welcome to CareSphere 🌐</h1>
        <h4 style="color: #36454F; font-weight: 400;">Where care, connection, and innovation meet.</h4>
    </div>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.success("Select a page above.")

# ----------------------------
# Function to load Lottie animation
# ----------------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ----------------------------
# Lottie Animation
# ----------------------------
lottie_factory = load_lottieurl("https://lottie.host/d5e67235-ae5c-427b-937d-d4ba6c9c9589/XQug5dpK0s.json")
st_lottie(lottie_factory, key="factory")
