import streamlit as st
import os
import tensorflow as tf
from keras.models import load_model
import librosa
import numpy as np
import time

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Heartbeat Detection",
    page_icon="🫀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f8f9fa;
    }

    /* Main Container */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* Custom File Uploader */
    .stFileUploader > div {
        background-color: #ffffff;
        border: 2px dashed #dc3545;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stFileUploader > div:hover {
        border-color: #b91c26;
        background-color: #fff5f5;
        transform: translateY(-2px);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #dc3545, #b91c26) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3) !important;
        width: 100% !important;
        margin: 1rem 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(220, 53, 69, 0.4) !important;
    }

    /* Info Cards */
    .info-card {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .info-card h5 {
        color: #495057;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }

    .info-card p {
        color: #6c757d;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }

    /* Result Cards */
    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
        animation: slideIn 0.5s ease;
    }

    .result-artifact { border-left-color: #6c757d; }
    .result-aunlabelledtest { border-left-color: #17a2b8; }
    .result-bunlabelledtest { border-left-color: #20c997; }
    .result-extrahls { border-left-color: #ffc107; }
    .result-extrastole { border-left-color: #fd7e14; }
    .result-murmur { border-left-color: #dc3545; }
    .result-normal { border-left-color: #28a745; }
    .result-unlabelledtest { border-left-color: #6f42c1; }

    .result-condition {
        font-size: 2rem;
        font-weight: 700;
        color: #2b2d42;
        margin-bottom: 1rem;
    }

    .result-confidence {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .result-description {
        color: #495057;
        line-height: 1.6;
        font-size: 16px;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #dc3545;
        margin-bottom: 0.3rem;
    }

    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Progress Bars */
    .confidence-item {
        margin: 0.8rem 0;
    }

    .confidence-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.3rem;
        font-weight: 500;
        color: #495057;
    }

    .confidence-bar {
        background-color: #e9ecef;
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 1s ease-in-out;
    }

    .conf-artifact { background-color: #6c757d; }
    .conf-aunlabelledtest { background-color: #17a2b8; }
    .conf-bunlabelledtest { background-color: #20c997; }
    .conf-extrahls { background-color: #ffc107; }
    .conf-extrastole { background-color: #fd7e14; }
    .conf-murmur { background-color: #dc3545; }
    .conf-normal { background-color: #28a745; }
    .conf-unlabelledtest { background-color: #6f42c1; }

    /* Feature Box Styling */
    .main-header {
        font-size: 2.5rem;
        color: #dc3545;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .feature-box {
        background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .feature-box h4 {
        margin-bottom: 10px;
        font-size: 1.3rem;
    }
    .feature-box p {
        font-size: 1rem;
        line-height: 1.5;
    }

    /* Audio Player */
    .stAudio {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }

    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Success/Warning Messages */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        color: #155724;
    }

    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        color: #856404;
    }

    .stError {
        background-color: #f8d7da;
        border: 1px solid #dc3545;
        border-radius: 8px;
        color: #721c24;
    }

    /* Hide Streamlit Elements */
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper Functions
# ----------------------------
@st.cache_resource
def load_ml_model():
    try:
        model = tf.keras.models.load_model("Heartbeat_audioclassification.keras")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# ----------------------------
# Condition Information
# ----------------------------
condition_info = {
    0: {
        'name': 'Artifact',
        'class': 'result-artifact',
        'emoji': '⚡',
        'description': 'Audio artifacts detected - this may be due to noise, poor recording quality, or technical interference in the heartbeat recording.',
        'recommendation': 'Please try recording again in a quieter environment with better audio quality. Ensure proper placement of recording device.',
        'confidence_class': 'conf-artifact'
    },
    1: {
        'name': 'A-Unlabelled Test',
        'class': 'result-aunlabelledtest',
        'emoji': '🔍',
        'description': 'An unlabelled cardiac pattern (Type A) has been detected. This requires further medical evaluation for proper classification.',
        'recommendation': 'Consult with a cardiologist for comprehensive cardiac evaluation and proper diagnosis of this heart pattern.',
        'confidence_class': 'conf-aunlabelledtest'
    },
    2: {
        'name': 'B-Unlabelled Test',
        'class': 'result-bunlabelledtest',
        'emoji': '🔬',
        'description': 'An unlabelled cardiac pattern (Type B) has been identified. Professional medical assessment is needed for accurate classification.',
        'recommendation': 'Schedule an appointment with a cardiac specialist for detailed heart examination and proper diagnosis.',
        'confidence_class': 'conf-bunlabelledtest'
    },
    3: {
        'name': 'Extrahls',
        'class': 'result-extrahls',
        'emoji': '🎵',
        'description': 'Extra heart sounds (gallops) detected - these are additional sounds that may indicate cardiac conditions like heart failure or ventricular dysfunction.',
        'recommendation': 'Medical evaluation recommended. Extra heart sounds can be significant and may require cardiac assessment and treatment.',
        'confidence_class': 'conf-extrahls'
    },
    4: {
        'name': 'Extrasystole',
        'class': 'result-extrastole',
        'emoji': '💓',
        'description': 'Extrasystoles (premature heartbeats) detected. These are early heartbeats that can be benign or indicate underlying cardiac issues.',
        'recommendation': 'Consult with a cardiologist to determine if these irregular beats require treatment or monitoring.',
        'confidence_class': 'conf-extrastole'
    },
    5: {
        'name': 'Murmur',
        'class': 'result-murmur',
        'emoji': '🌊',
        'description': 'A heart murmur has been detected. This is an extra sound during heartbeat cycle, which can be innocent or indicate heart valve problems.',
        'recommendation': 'Cardiac evaluation recommended to determine if the murmur is benign or requires treatment. Further tests like echocardiogram may be needed.',
        'confidence_class': 'conf-murmur'
    },
    6: {
        'name': 'Normal',
        'class': 'result-normal',
        'emoji': '✅',
        'description': 'Excellent news! Normal heart sounds detected. Your cardiac rhythm appears healthy with regular heart beats and normal sound patterns.',
        'recommendation': 'Continue maintaining good cardiovascular health with regular exercise, healthy diet, and routine check-ups.',
        'confidence_class': 'conf-normal'
    },
    7: {
        'name': 'Unlabelled Test',
        'class': 'result-unlabelledtest',
        'emoji': '❓',
        'description': 'An unclassified cardiac pattern has been detected. This pattern doesn\'t match standard categories and needs professional evaluation.',
        'recommendation': 'Medical consultation strongly recommended for proper cardiac assessment and diagnosis of this unusual heart pattern.',
        'confidence_class': 'conf-unlabelledtest'
    }
}

# Header
st.markdown('<h1 class="main-header">🫀 Cardiac Sound Analysis for Heart Health</h1>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>💓 Heart Sound Analysis</h4>
        <p>Analyze heartbeat sounds to detect various cardiac conditions and abnormalities.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Condition Detection</h4>
        <p>Detect Artifact, Murmurs, Extrasystoles, Extrahls, and other heart conditions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>💡 Detailed Reports</h4>
        <p>Comprehensive analysis with confidence scores and medical recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Main Application
# ----------------------------
def main():
    # Load model
    model = load_ml_model()

    if model is None:
        st.error("⚠️ Model could not be loaded. Please check if the model file exists.")
        st.stop()

    # File Upload Section
    st.markdown("### Upload Heartbeat Audio File 🎵")
    file = st.file_uploader(
        "Choose a heartbeat audio file for analysis (WAV, MP3, M4A):",
        type=["wav", "mp3", "m4a"],
        help="Upload a heartbeat recording for AI analysis. Recommended duration: 3-10 seconds"
    )

    if file is not None:
        # File Information Display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>📄</div>
                <div class='metric-label'>{file.name}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{file.size / 1024:.1f} KB</div>
                <div class='metric-label'>File Size</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>🎵</div>
                <div class='metric-label'>{file.type}</div>
            </div>
            """, unsafe_allow_html=True)

        # Audio Preview
        st.markdown("### Audio Preview 🎧")
        st.audio(file, format=file.type)

        # Analysis Button
        st.markdown("### Start Cardiac Analysis 🔬")

        if st.button("Analyze Heartbeat Sounds 🫀"):
            try:
                with st.spinner("🫀 AI is analyzing your heartbeat sounds..."):
                    # Progress indicator
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.015)
                        progress_bar.progress(i + 1)

                    # Load and process audio
                    y, sr = librosa.load(file, duration=3, offset=0.5)
                    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
                    mfcc = mfcc.reshape(1, -1)

                    # Make prediction
                    prediction = model.predict(mfcc)
                    predicted_label = np.argmax(prediction, axis=-1)[0]
                    confidence = np.max(prediction) * 100

                    # Clear progress bar
                    progress_bar.empty()

                    # Display Results
                    st.markdown("### Cardiac Analysis Results 📊")

                    condition = condition_info[predicted_label]

                    # Main Result Card
                    st.markdown(f"""
                    <div class='result-card {condition['class']}'>
                        <div class='result-condition'>
                            {condition['emoji']} {condition['name']}
                        </div>
                        <div class='result-confidence'>
                            Confidence Level: {confidence:.1f}%
                        </div>
                        <div class='result-description'>
                            <p><b>🔍 Analysis:</b> {condition['description']}</p>
                            <p><b>💡 Recommendation:</b> {condition['recommendation']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Detailed Analysis Metrics
                    st.markdown("### Detailed Analysis 📈")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value'>{condition['name']}</div>
                            <div class='metric-label'>Primary Detection</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value'>{confidence:.1f}%</div>
                            <div class='metric-label'>Confidence Score</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value'>40</div>
                            <div class='metric-label'>MFCC Features</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Confidence Breakdown
                    st.markdown("### All Conditions Analysis 🎯")
                    st.markdown("""
                    <div class='info-card'>
                        <h5>Confidence Breakdown</h5>
                        <p>Here's how confident our AI is about each possible cardiac condition:</p>
                    </div>
                    """, unsafe_allow_html=True)

                    for i, (label, info) in enumerate(condition_info.items()):
                        conf_value = prediction[0][i] * 100
                        st.markdown(f"""
                        <div class='confidence-item'>
                            <div class='confidence-label'>
                                <span>{info['emoji']} <strong>{info['name']}</strong></span>
                                <span><strong>{conf_value:.1f}%</strong></span>
                            </div>
                            <div class='confidence-bar'>
                                <div class='confidence-fill {info['confidence_class']}' style='width: {conf_value}%;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Medical Disclaimer and Recommendations
                    if predicted_label == 6:  # Normal
                        st.success(
                            "🎉 Great news! Your heartbeat patterns appear normal. Continue maintaining good cardiovascular health!")
                    else:
                        st.warning(
                            "⚠️ This cardiac screening suggests you should consult with a cardiologist for proper medical evaluation and personalized treatment advice.")

                    st.info(
                        "🏥 **Important:** This AI cardiac screening tool is designed to assist in early detection and should not replace professional medical diagnosis. Please consult with qualified cardiologists for comprehensive evaluation and treatment.")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("Please ensure you uploaded a valid audio file and try again. Supported formats: WAV, MP3, M4A")

    else:
        # Footer Information
        st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>💓</div>
            <div class='metric-label'>Cardiac AI Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>⚡</div>
            <div class='metric-label'>Real-time Processing</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>🎯</div>
            <div class='metric-label'>Medical-Grade Precision</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()