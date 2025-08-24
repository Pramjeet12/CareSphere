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
    page_title="Lung Detection",
    page_icon="🫁",
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
        border: 2px dashed #007bff;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stFileUploader > div:hover {
        border-color: #0056b3;
        background-color: #f0f8ff;
        transform: translateY(-2px);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #0056b3) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3) !important;
        width: 100% !important;
        margin: 1rem 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4) !important;
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

    .result-asthma { border-left-color: #dc3545; }
    .result-bronchial { border-left-color: #17a2b8; }
    .result-copd { border-left-color: #ffc107; }
    .result-healthy { border-left-color: #28a745; }
    .result-pneumonia { border-left-color: #e83e8c; }

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
        color: #007bff;
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

    .conf-asthma { background-color: #dc3545; }
    .conf-bronchial { background-color: #17a2b8; }
    .conf-copd { background-color: #ffc107; }
    .conf-healthy { background-color: #28a745; }
    .conf-pneumonia { background-color: #e83e8c; }

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
        background-color: #d1edff;
        border: 1px solid #007bff;
        border-radius: 8px;
        color: #004085;
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
        model = tf.keras.models.load_model("Asthma_audioclassification.keras")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


# ----------------------------
# Condition Information
# ----------------------------
condition_info = {
    0: {
        'name': 'Asthma',
        'class': 'result-asthma',
        'emoji': '🫁',
        'description': 'The AI has detected respiratory patterns consistent with asthma. This includes characteristic wheeze patterns and airway obstruction indicators in the audio analysis.',
        'recommendation': 'Please consult with a pulmonologist or your primary care physician for proper diagnosis and treatment planning. Early intervention can significantly improve quality of life.',
        'confidence_class': 'conf-asthma'
    },
    1: {
        'name': 'Bronchial',
        'class': 'result-bronchial',
        'emoji': '🌬️',
        'description': 'Bronchial has been detected in the breath patterns. The audio shows signs of bronchial tube irritation and inflammation.',
        'recommendation': 'Seek medical advice for appropriate bronchial treatment and management. Your doctor may recommend anti-inflammatory treatments or further testing.',
        'confidence_class': 'conf-bronchial'
    },
    2: {
        'name': 'Chronic Obstructive Pulmonary Disease',
        'class': 'result-copd',
        'emoji': '⚠️',
        'description': 'The analysis suggests possible Chronic Obstructive Pulmonary Disease. Audio indicates airflow limitation and breathing difficulties.',
        'recommendation': 'Medical evaluation is strongly recommended for COPD assessment and management. Early diagnosis and treatment can help slow disease progression.',
        'confidence_class': 'conf-copd'
    },
    3: {
        'name': 'Healthy',
        'class': 'result-healthy',
        'emoji': '✅',
        'description': 'Excellent news! Normal breathing patterns have been detected. Your respiratory health appears to be in good condition based on the audio analysis.',
        'recommendation': 'Continue maintaining good respiratory health with regular exercise, clean air exposure, and avoiding smoking. Keep up the good work!',
        'confidence_class': 'conf-healthy'
    },
    4: {
        'name': 'Pneumonia',
        'class': 'result-pneumonia',
        'emoji': '🚨',
        'description': 'The respiratory patterns may indicate pneumonia. The audio analysis shows signs consistent with lung infection and possible fluid accumulation.',
        'recommendation': 'Immediate medical consultation is strongly recommended for proper diagnosis and treatment. Pneumonia requires prompt medical attention.',
        'confidence_class': 'conf-pneumonia'
    }
}


# Page Header
# ----------------------------
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .feature-box {
        background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); /* Fresh healthcare gradient */
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;   /* Center text horizontally */
        text-align: center;    /* Ensure text is centered */
        box-shadow: 0 4px 10px rgba(0,0,0,0.2); /* Smooth shadow for depth */
    }
    .feature-box h4 {
        margin-bottom: 10px;
        font-size: 1.3rem;
    }
    .feature-box p {
        font-size: 1rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🫁 Respiratory Sound Analysis for Lung Health</h1>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🌬️ Breath Sound Analysis</h4>
        <p>Analyze breath sounds to detect unique patterns linked to lung health conditions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Condition Detection</h4>
        <p>Detect conditions like Asthma, Bronchial, COPD, Pneumonia, or Healthy state.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>💡 Insightful Results</h4>
        <p>Receive easy to understand reports with confidence scores and insights.</p>
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
    st.markdown("### Upload Audio File📁")
    file = st.file_uploader(
        "Choose an audio file for analysis (WAV, MP3, M4A):",
        type=["wav", "mp3", "m4a"],
        help="Upload a breath sound recording for AI analysis. Recommended duration: 3-10 seconds"
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
        st.markdown("### Audio Preview🎧")
        st.audio(file, format=file.type)

        # Analysis Button
        st.markdown("### Start Analysis🔬")

        if st.button("Analyze Breath Sounds🤖"):
            try:
                with st.spinner("🤖 AI is analyzing your breath sounds..."):
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
                    st.markdown("### Analysis Results📊")

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
                    st.markdown("### Detailed Analysis📈")
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
                    st.markdown("### All Conditions Analysis🎯")
                    st.markdown("""
                    <div class='info-card'>
                        <h5>Confidence Breakdown</h5>
                        <p>Here's how confident our AI is about each possible condition:</p>
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
                    if predicted_label == 3:  # Healthy
                        st.success(
                            "🎉 Great news! Your breathing patterns appear healthy. Continue maintaining good respiratory health!")
                    else:
                        st.warning(
                            "⚠️ This screening suggests you should consult with a healthcare professional for proper medical evaluation and personalized treatment advice.")

                    st.info(
                        "🏥 **Important:** This AI screening tool is designed to assist in early detection and should not replace professional medical diagnosis. Please consult with qualified healthcare professionals for comprehensive evaluation and treatment.")

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
            <div class='metric-value'>🔬</div>
            <div class='metric-label'>AI-Powered Analysis</div>
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
            <div class='metric-label'>Clinical-Grade Accuracy</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()