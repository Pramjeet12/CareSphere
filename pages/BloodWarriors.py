import streamlit as st
import requests
from datetime import datetime
import urllib.parse

# Streamlit App Configuration
st.set_page_config(
    page_title="BloodConnect",
    page_icon="🩸",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #dc3545;
        margin-bottom: 30px;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        color: #dc3545;
        margin: 30px 0 20px 0;
        border-bottom: 3px solid #dc3545;
        padding-bottom: 5px;
        font-weight: bold;
        font-size: 2em;
    }
    .feature-box {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        transition: transform 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
    }
    .feature-box h4 {
        margin-bottom: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    .feature-box p {
        font-size: 14px;
        margin: 0;
        opacity: 0.9;
    }
    .info-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #dc3545;
    }
    .info-card h4 {
        color: #dc3545;
        margin-bottom: 15px;
    }
    .blood-type-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    .blood-type-card {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        transition: transform 0.3s ease;
    }
    .blood-type-card:hover {
        transform: translateY(-3px);
    }
    .blood-type-card h3 {
        margin: 0;
        font-size: 2em;
    }
    .blood-type-card p {
        margin: 5px 0 0 0;
        font-size: 0.9em;
        opacity: 0.9;
    }
    .emergency-banner {
        background: linear-gradient(45deg, #ff4757, #ff3838);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .requirements-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    .requirement-item {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .requirement-item h5 {
        color: #28a745;
        margin-bottom: 8px;
    }
    .benefits-list {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    }
    .webapp-embed {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        margin: 40px 0;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 15px 40px;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c82333 0%, #a71e2a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🩸 BloodConnect - Save Lives Together</h1>", unsafe_allow_html=True)

# Emergency Banner
st.markdown("""
<div class="emergency-banner">
    <h3>🔔 Urgent: Blood Needed Every 2 Seconds!</h3>
    <p>Your donation can save up to 3 lives. Be a hero today!</p>
</div>
""", unsafe_allow_html=True)

# Feature boxes at the top (2 rows of 3)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Find Blood Donors</h4>
        <p>Search for blood donors by blood type and location instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🩸 Donate Blood</h4>
        <p>Register as a donor and help save lives in your community.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>📱 Real-time Updates</h4>
        <p>Get instant notifications about blood requirements near you.</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h4>🏥 Hospital Network</h4>
        <p>Connected with major hospitals and blood banks across India.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-box">
        <h4>📊 Track Donations</h4>
        <p>Keep track of your donation history and impact on lives saved.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-box">
        <h4>🛡️ Safe & Secure</h4>
        <p>All donor information is kept secure and confidential.</p>
    </div>
    """, unsafe_allow_html=True)

# Blood Types Information
st.markdown("<h2 class='section-header'>🩸 Blood Types & Compatibility</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="blood-type-grid">
    <div class="blood-type-card">
        <h3>A+</h3>
        <p>Can donate to A+, AB+</p>
    </div>
    <div class="blood-type-card">
        <h3>A-</h3>
        <p>Can donate to A+, A-, AB+, AB-</p>
    </div>
    <div class="blood-type-card">
        <h3>B+</h3>
        <p>Can donate to B+, AB+</p>
    </div>
    <div class="blood-type-card">
        <h3>B-</h3>
        <p>Can donate to B+, B-, AB+, AB-</p>
    </div>
    <div class="blood-type-card">
        <h3>AB+</h3>
        <p>Universal Recipient</p>
    </div>
    <div class="blood-type-card">
        <h3>AB-</h3>
        <p>Can donate to AB+, AB-</p>
    </div>
    <div class="blood-type-card">
        <h3>O+</h3>
        <p>Can donate to A+, B+, AB+, O+</p>
    </div>
    <div class="blood-type-card">
        <h3>O-</h3>
        <p>Universal Donor</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Who Can Donate Blood
st.markdown("<h2 class='section-header'>✅ Who Can Donate Blood?</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="requirements-grid">
    <div class="requirement-item">
        <h5>👤 Age Requirements</h5>
        <p>Between 18-65 years old. First-time donors should be between 18-60 years.</p>
    </div>
    <div class="requirement-item">
        <h5>⚖️ Weight Requirements</h5>
        <p>Minimum 45 kg (99 lbs) for safe donation without health complications.</p>
    </div>
    <div class="requirement-item">
        <h5>🩺 Health Status</h5>
        <p>Good general health, no fever, cold, or flu symptoms in the past week.</p>
    </div>
    <div class="requirement-item">
        <h5>💊 Medication Check</h5>
        <p>Not taking antibiotics or certain medications. Consult staff about your medications.</p>
    </div>
    <div class="requirement-item">
        <h5>🍷 Lifestyle Factors</h5>
        <p>No alcohol consumption 24 hours before donation. Well-rested and hydrated.</p>
    </div>
    <div class="requirement-item">
        <h5>⏰ Previous Donation</h5>
        <p>At least 56 days (8 weeks) since your last whole blood donation.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Benefits of Blood Donation
st.markdown("<h2 class='section-header'>🎁 Benefits of Blood Donation</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🏥 Health Benefits</h4>
        <ul>
            <li>Free mini health checkup</li>
            <li>Reduces risk of heart disease</li>
            <li>Helps maintain healthy iron levels effectively</li>
            <li>Burns approximately 650 calories</li>
            <li>Stimulates production of new blood cells</li>
            <li>May help identify unknown health issues</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>💝 Social Impact</h4>
        <ul>
            <li>Save up to 3 lives with one donation</li>
            <li>Help patients with cancer, surgery, accidents</li>
            <li>Support emergency medical situations</li>
            <li>Contribute to community health</li>
            <li>Experience the joy of giving back</li>
            <li>Inspire others to donate blood</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Blood Donation Process
# Blood Donation Process Section
st.markdown("<h2 class='section-header'>📋 Blood Donation Process</h2>", unsafe_allow_html=True)

# Custom CSS for process step boxes
st.markdown("""
<style>
    .process-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        height: 220px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-left: 5px solid #2c3e50;
        transition: transform 0.2s ease-in-out;
    }
    .process-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }
    .process-card h2 {
        margin: 0;
        font-size: 28px;
        color: #2c3e50;
    }
    .process-card h4 {
        margin: 8px 0;
        font-size: 18px;
        color: #34495e;
    }
    .process-card p {
        font-size: 14px;
        color: #555;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Process steps
process_steps = [
    {"step": "1️⃣", "title": "Registration", "desc": "Fill out donor information form and show ID"},
    {"step": "2️⃣", "title": "Health Screening", "desc": "Mini physical exam, questionnaire, and vital signs check"},
    {"step": "3️⃣", "title": "Donation", "desc": "Comfortable donation process takes about 8-12 minutes"},
    {"step": "4️⃣", "title": "Recovery", "desc": "Rest and refreshments provided for 10-15 minutes"}
]

# Display steps in columns
cols = st.columns(4)
for i, step in enumerate(process_steps):
    with cols[i]:
        st.markdown(f"""
        <div class="process-card">
            <h2>{step['step']}</h2>
            <h4>{step['title']}</h4>
            <p>{step['desc']}</p>
        </div>
        """, unsafe_allow_html=True)




# Web App Integration
st.markdown("<h2 class='section-header'>🌐 Blood Bank Management System</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="webapp-embed">
    <h3>🩸 Complete Blood Bank Management Platform</h3>
    <p>Access our comprehensive blood bank management system for donor registration, 
    blood inventory management, and emergency blood requests.</p>
    <p><strong>Features included:</strong></p>
    <p>• Real-time blood inventory • Donor management • Hospital requests • Emergency alerts • Reports & Analytics</p>
</div>
""", unsafe_allow_html=True)



# Embed the webapp using iframe
st.markdown("### 📱 Integrated Dashboard")
st.markdown("""
<iframe src="https://bb-b1v5.onrender.com" 
        width="100%" 
        height="800" 
        frameborder="0"
        style="border-radius: 15px; box-shadow: 0 8px 30px rgba(0,0,0,0.1);">
</iframe>
""", unsafe_allow_html=True)

# Alternative link if iframe doesn't work
st.markdown("---")
st.markdown("### 🔗 Direct Access")
st.markdown("**If the embedded system doesn't load properly, click here:**")
st.link_button("🌐 Direct Link to Blood Bank System", "https://bb-b1v5.onrender.com", use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
            border-radius: 15px; margin-top: 30px; color: white;'>
    <h3>🩸 BloodConnect - Connecting Lives</h3>
    <p>Every drop counts. Every donor matters. Together, we save lives.</p>
    <p><strong>🚨 Remember: In emergency, call 108 immediately!</strong></p>
    <p><small>Powered by AI • Secure • Reliable • Available 24/7</small></p>
</div>
""", unsafe_allow_html=True)