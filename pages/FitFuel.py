import streamlit as st

# Page config
st.set_page_config(page_title="HealthFit", page_icon="💪", layout="wide")

# Custom CSS for enhanced UI
st.markdown("""
<style>
    body {
        background-color: #f0f4f8;
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(180deg, #d1fae5, #ffffff);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .header h1 {
        color: #065f46;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .header p {
        font-size: 1.2rem;
        color: #374151;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    .feature-card {
        background-color: #1f2937;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: left;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        height: 280px;
        transition: transform 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0.5rem 0;
        color: #34d399;
    }
    .feature-card p {
        font-size: 1rem;
        line-height: 1.5;
        color: #e5e7eb;
    }
    .cta-button {
        display: flex;
        justify-content: center;
        margin: 3rem 0;
    }
    .cta-button a {
        background: linear-gradient(135deg, #10b981, #047857);
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
        background: linear-gradient(135deg, #047857, #065f46);
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .section-title {
        color: #065f46;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin: 2rem 0;
    }
    .row-gap {
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>💪 HealthFit: Your Personal Health & Fitness Companion</h1>
    <p>Empower your wellness journey with AI-driven tools for <b>BMI tracking</b>, <b>personalized health recommendations</b>, <b>nutrition planning</b>, <b>workout routines</b>, and <b>hydration tracking</b>.</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown('<h2 class="section-title">Our Wellness Tools</h2>', unsafe_allow_html=True)

# First Row
st.markdown('<div class="row-gap">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📏 BMI Calculator</h3>
        <p>Calculate your Body Mass Index instantly to understand your health status and set fitness goals.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🩺 Health Recommendation</h3>
        <p>Receive personalized health advice based on your lifestyle and medical data for optimal wellness.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🥗 Nutrition Planner</h3>
        <p>Create tailored meal plans that align with your dietary needs and health objectives.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Second Row
st.markdown('<div class="row-gap">', unsafe_allow_html=True)
col4, col5, col6 = st.columns([1, 1, 1], gap="medium")
with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>🏋️ Workout Planner</h3>
        <p>Design custom workout routines suited to your fitness level and goals, powered by AI insights.</p>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div class="feature-card">
        <h3>💧 Hydration Tracker</h3>
        <p>Monitor your daily water intake to stay hydrated and support overall health and performance.</p>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown("""
    <div class="feature-card">
        <h3>🧘 Stress Management</h3>
        <p>Access AI-guided mindfulness and stress-relief techniques to enhance mental well-being.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Call to Action Button
st.markdown("""
<div class="cta-button">
    <a href="https://health-plan-wiz.lovable.app/" target="_self">🚀 START YOUR WELLNESS JOURNEY</a>
</div>
""", unsafe_allow_html=True)