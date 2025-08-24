import streamlit as st

# Page config
st.set_page_config(page_title="MultiDx Prediction", page_icon="🩺", layout="wide")

# Custom CSS for enhanced UI
st.markdown("""
<style>
    body {
        background-color: #f5f7fa;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(180deg, #e3f2fd, #ffffff);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .header h1 {
        color: #1a3c5e;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .header p {
        font-size: 1.2rem;
        color: #4a5568;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    .feature-card {
        background-color: #17202a;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        height: 280px;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0.5rem 0;
        color: #60a5fa;
    }
    .feature-card p {
        font-size: 1rem;
        line-height: 1.5;
        color: #e2e8f0;
    }
    .cta-button {
        display: flex;
        justify-content: center;
        margin: 3rem 0;
    }
    .cta-button a {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.8rem;
        font-weight: bold;
        text-decoration: none;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    .cta-button a:hover {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .section-title {
        color: #1a3c5e;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🧬 MultiDxPred: Smarter Health Predictions with AI</h1>
    <p>Empowering you with cutting-edge AI to assess risks for <b>Diabetes</b>, <b>Lung Cancer</b>, and <b>Heart Attack</b> — using medical report data for personalized health predictions.</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown('<h2 class="section-title">Our Health Prediction Tools</h2>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🧬 Diabetes Risk Assessment</h3>
        <p>Analyze your medical data with AI to evaluate diabetes risk, leveraging key health indicators for accurate predictions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🫁 Lung Cancer Detection</h3>
        <p>Utilize advanced machine learning to detect early lung cancer risks based on symptoms and medical history.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>❤️ Heart Attack Risk</h3>
        <p>Assess your heart health with AI-driven predictions using critical clinical parameters to estimate heart attack risk.</p>
    </div>
    """, unsafe_allow_html=True)

# Call to Action Button
st.markdown("""
<div class="cta-button">
    <a href="https://predictive-wellness.lovable.app/" target="_self">🚀 LAUNCH PREDICTOR</a>
</div>
""", unsafe_allow_html=True)