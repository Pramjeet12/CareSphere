import streamlit as st
import requests
import os
import easyocr
import tempfile
from groq import Groq
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
from typing import List, Tuple
from dotenv import load_dotenv
import os


# --- Groq API Setup ---
load_dotenv()  # reads .env file (kept locally, not uploaded)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY)


# --- OCR Setup ---
reader = easyocr.Reader(['en'])


# --- Image Enhancement Functions ---
def enhance_image_quality(image_path: str) -> str:
    """Enhance image quality for better OCR results"""
    try:
        # Read image with OpenCV
        img = cv2.imread(image_path)

        # Convert to PIL Image for easier manipulation
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # 1. Resize image if too small
        width, height = pil_img.size
        if width < 800 or height < 600:
            scale_factor = max(800 / width, 600 / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)

        # 2. Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(2.0)

        # 3. Enhance brightness
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(1.2)

        # 4. Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(2.0)

        # 5. Apply unsharp mask filter
        pil_img = pil_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Convert back to OpenCV format
        enhanced_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # 6. Apply additional OpenCV enhancements
        # Convert to grayscale
        gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # Apply Gaussian blur and then unsharp masking
        blurred = cv2.GaussianBlur(enhanced_gray, (0, 0), 2.0)
        unsharp_mask = cv2.addWeighted(enhanced_gray, 1.5, blurred, -0.5, 0)

        # Apply morphological operations to clean up text
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(unsharp_mask, cv2.MORPH_CLOSE, kernel)

        # Save enhanced image
        enhanced_path = image_path.replace('.jpg', '_enhanced.jpg')
        cv2.imwrite(enhanced_path, cleaned)

        return enhanced_path

    except Exception as e:
        st.warning(f"Image enhancement failed: {e}. Using original image.")
        return image_path


def extract_text_multiple_methods(image_path: str) -> List[str]:
    """Extract text using multiple OCR methods for better accuracy"""
    extracted_texts = []

    try:
        # Method 1: EasyOCR (good for multiple languages and handwriting)
        result_easyocr = reader.readtext(image_path, detail=0)
        text_easyocr = " ".join(result_easyocr).strip()
        if text_easyocr:
            extracted_texts.append(("EasyOCR", text_easyocr))
    except Exception as e:
        st.warning(f"EasyOCR failed: {e}")

    try:
        # Method 2: Pytesseract with different PSM modes
        img = cv2.imread(image_path)

        # PSM 6: Uniform block of text
        text_tesseract_6 = pytesseract.image_to_string(img,
                                                       config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ').strip()
        if text_tesseract_6:
            extracted_texts.append(("Tesseract PSM-6", text_tesseract_6))

        # PSM 8: Single word
        text_tesseract_8 = pytesseract.image_to_string(img, config='--psm 8').strip()
        if text_tesseract_8:
            extracted_texts.append(("Tesseract PSM-8", text_tesseract_8))

        # PSM 13: Raw line (no specific word or character limits)
        text_tesseract_13 = pytesseract.image_to_string(img, config='--psm 13').strip()
        if text_tesseract_13:
            extracted_texts.append(("Tesseract PSM-13", text_tesseract_13))

    except Exception as e:
        st.warning(f"Tesseract OCR failed: {e}")

    return extracted_texts


def preprocess_text_for_medicine_detection(text: str) -> str:
    """Clean and preprocess extracted text for better medicine identification"""
    # Remove special characters but keep spaces and alphanumeric
    cleaned = re.sub(r'[^a-zA-Z0-9\s\-\.]', ' ', text)

    # Remove extra whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Convert to lowercase for consistency
    cleaned = cleaned.lower()

    return cleaned


def get_groq_medicine_identification(extracted_texts: List[Tuple[str, str]]) -> str:
    """Use Groq LLM to identify medicine from extracted text"""
    try:
        # Combine all extracted texts
        all_texts = "\n".join([f"Method {method}: {text}" for method, text in extracted_texts])

        prompt = f"""
        You are an expert pharmacist and medical AI assistant specializing in medicine identification.

        I have extracted the following text from a medicine strip/tablet image using multiple OCR methods:

        {all_texts}

        Based on this extracted text, please:

        1. **IDENTIFY THE MEDICINE**: Determine the most likely medicine name (generic and brand names if possible)
        2. **CONFIDENCE LEVEL**: Rate your confidence (High/Medium/Low) in the identification
        3. **REASONING**: Explain why you think this is the identified medicine
        4. **ALTERNATIVE POSSIBILITIES**: List 2-3 other possible medicines if uncertainty exists

        **Special Instructions:**
        - Consider all types of medications (prescription, OTC, vitamins, supplements)
        - If the text is unclear or fragmented, make educated guesses based on partial matches
        - Consider common medicine name patterns and pharmaceutical naming conventions
        - Even for damaged/unclear text, try to provide the best possible identification

        **Format your response as:**
        PRIMARY IDENTIFICATION: [Medicine Name]
        CONFIDENCE: [High/Medium/Low]
        REASONING: [Why this medicine]
        ALTERNATIVES: [Other possibilities]
        """

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system",
                 "content": "You are an expert pharmacist AI specializing in comprehensive medicine identification."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3,  # Lower temperature for more consistent results
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error in medicine identification: {e}"


def get_groq_medicine_information(medicine_name: str) -> str:
    """Get detailed information about the identified medicine"""
    try:
        prompt = f"""
        As an AI medical assistant, provide comprehensive information about "{medicine_name}".

        Please include:
        1. **Primary Uses**: What this medicine is prescribed for and its medical applications
        2. **Mechanism of Action**: How it works in the body (simplified explanation)
        3. **Common Conditions Treated**: List of conditions this medication typically addresses
        4. **Common Side Effects**: Most frequently reported side effects
        5. **Important Precautions**: Drug interactions, contraindications, and special warnings
        6. **Administration Guidelines**: General guidance on how and when to take it
        7. **Warning Signs**: Symptoms that require immediate medical attention

        **Important Notes:**
        - Do NOT provide specific dosage information
        - Always end with "Consult your healthcare provider for personalized advice"
        - Keep explanations clear and patient-friendly
        - Include both generic and brand name information if applicable
        - Limit response to 300 words
        """

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system",
                 "content": "You are a medical AI assistant providing comprehensive medication information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error getting medicine information: {e}"


def get_medicine_safety_check(medicine_name: str, patient_context: str = "general patient") -> str:
    """Get safety information and warnings for the medicine"""
    try:
        prompt = f"""
        As a clinical pharmacist AI, provide safety information for "{medicine_name}" for a {patient_context}.

        Please focus on:
        1. **Drug Interactions**: Important interactions with common medications
        2. **Contraindications**: When this medicine should NOT be used
        3. **Special Monitoring**: Lab tests or monitoring that may be required
        4. **Emergency Warning Signs**: Symptoms requiring immediate medical attention
        5. **Special Populations**: Considerations for elderly, pregnant women, children
        6. **Food/Alcohol Interactions**: How food or alcohol affects this medication

        Keep response concise (under 200 words) and clinically relevant.
        End with "Always inform your doctor about all medications and supplements you're taking."
        """

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system",
                 "content": "You are a clinical pharmacist AI specializing in drug safety for all patients."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.2,  # Very low temperature for safety information
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error getting safety information: {e}"


def get_groq_chatbot_response(summary_prompt: str) -> str:
    """Get chatbot response for summary"""
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful AI medicine information assistant."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=400,
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"


# --- Streamlit UI ---
st.set_page_config(
    page_title="AI-Powered Medicine Scanner",
    page_icon="💊",
    layout="wide"
)

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin: 10px 0;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .options-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .upload-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 AI Powered Medicine Scanner & Information System</h1>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Advanced OCR</h4>
        <p>Multiple OCR engines for damaged or unclear medicine images.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🧠 AI Medicine ID</h4>
        <p>LLM-powered medicine identification with confidence scoring.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>⚕️ Complete Med Info</h4>
        <p>Comprehensive information about uses, effects, and safety.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# File uploader and options
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📷 Upload Medicine Image")
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        help="Upload clear images of medicine strips, tablets, bottles, or prescription labels. The AI can handle damaged or unclear images too!"
    )

with col2:
    st.markdown("### 🎛️ Processing Options")
    st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)  # Adds a 20px gap
    enhance_image = st.checkbox("✨ Enhance Image Quality", value=True, help="Recommended for blurry or damaged images")
    multiple_ocr = st.checkbox("🔄 Use Multiple OCR Methods", value=True, help="Better accuracy for unclear text")
    detailed_analysis = st.checkbox("📊 Detailed Safety Analysis", value=False, help="Include drug interaction warnings")

# Main scanning button
if st.button("🔎 Scan & Analyze Medicine", type="primary", use_container_width=True):
    if uploaded_file:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 📸 Original Image")
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Step 1: Image Enhancement
        if enhance_image:
            with st.spinner("🔧 Enhancing image quality for better recognition..."):
                enhanced_path = enhance_image_quality(tmp_path)

                with col2:
                    st.markdown("### ✨ Enhanced Image")
                    if os.path.exists(enhanced_path):
                        st.image(enhanced_path, caption="Enhanced for OCR", use_column_width=True)
                    else:
                        enhanced_path = tmp_path
                        st.info("Using original image")
        else:
            enhanced_path = tmp_path

        # Step 2: Text Extraction
        with st.spinner("📖 Extracting text from image using advanced OCR..."):
            if multiple_ocr:
                extracted_texts = extract_text_multiple_methods(enhanced_path)
            else:
                # Use only EasyOCR
                result = reader.readtext(enhanced_path, detail=0)
                extracted_text = " ".join(result)
                extracted_texts = [("EasyOCR", extracted_text)]

        # Display extracted text
        if extracted_texts:
            st.markdown("### 📝 Extracted Text Results")
            for method, text in extracted_texts:
                with st.expander(f"🔍 {method} Results"):
                    st.code(text if text.strip() else "No text detected by this method")

        # Step 3: Medicine Identification using AI
        if extracted_texts:
            with st.spinner("🤖 AI is analyzing and identifying the medicine..."):
                identification_result = get_groq_medicine_identification(extracted_texts)

            # Display identification results in styled container
            st.markdown(f"""
                <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; border: 1px solid #b3d9e6;'>
                    <h5 style='color:#1e3a8a;'>🎯 AI Medicine Identification Results:</h5>
                    <p style='font-size:16px; color:#1e3a8a;'>{identification_result}</p>
                </div>
            """, unsafe_allow_html=True)

            # Step 4: Extract medicine name for detailed information
            lines = identification_result.split('\n')
            primary_medicine = ""
            for line in lines:
                if line.startswith("PRIMARY IDENTIFICATION:"):
                    primary_medicine = line.replace("PRIMARY IDENTIFICATION:", "").strip()
                    break

            if primary_medicine and primary_medicine.lower() not in ["unknown", "unclear", "not identified"]:
                # Get detailed medicine information
                with st.spinner("📚 Fetching detailed medicine information..."):
                    medicine_info = get_groq_medicine_information(primary_medicine)

                st.markdown(f"""
                    <div style='background-color: #f0f9ff; padding: 20px; border-radius: 10px; border: 1px solid #a7c7e7;'>
                        <h5 style='color:#1e40af;'>💊 Detailed Information - {primary_medicine}:</h5>
                        <p style='font-size:16px; color:#1e40af;'>{medicine_info}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Safety information if requested
                if detailed_analysis:
                    with st.spinner("⚠️ Analyzing safety information..."):
                        safety_info = get_medicine_safety_check(primary_medicine)

                    st.markdown(f"""
                        <div style='background-color: #fef2f2; padding: 20px; border-radius: 10px; border: 1px solid #f87171;'>
                            <h5 style='color:#dc2626;'>⚠️ Safety Information & Warnings:</h5>
                            <p style='font-size:16px; color:#dc2626;'>{safety_info}</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Generate summary
                summary_prompt = f"Provide a brief summary of the medicine scanning results for {primary_medicine}, including its main uses and key information patients should know."
                summary = get_groq_chatbot_response(summary_prompt)
                st.markdown(f"""
                    <div style='background-color: #edf2f4; padding: 20px; border-radius: 10px; border: 1px solid #ccc;'>
                        <h5 style='color:#2b2d42;'>📋 Medicine Information Summary:</h5>
                        <p style='font-size:16px; color:#2b2d42;'>{summary}</p>
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.error(
                "❌ No text could be extracted from the image. Please try with a clearer image or different lighting.")

        # Cleanup temporary files
        try:
            os.remove(tmp_path)
            if enhance_image and os.path.exists(enhanced_path) and enhanced_path != tmp_path:
                os.remove(enhanced_path)
        except:
            pass

    else:
        st.error("📷 Please upload an image first!")

# Additional features section
st.markdown("---")
st.markdown("### 💡 Tips for Better Results")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📸 Image Quality Tips:**
    - 🔆 Use good lighting, avoid shadows
    - 📱 Hold phone steady, avoid blur
    - 🔍 Get close to the text on medicine
    - ⚡ Use flash if needed for dark images
    - 📋 Include prescription labels when possible
    """)

with col2:
    st.markdown("""
    **💊 Medicine Types Supported:**
    - 💊 Prescription medications
    - 🏪 Over-the-counter drugs
    - 💉 Vitamins and supplements
    - 🧬 Generic and brand-name drugs
    - 🩹 Topical medications and creams
    """)

# Emergency information
st.markdown("""
---
### 🚨 Important Medical Information
**This AI assistant provides general information only:**
- 📞 Always consult your healthcare provider for medical advice
- 🏥 For medical emergencies, call emergency services immediately
- 📋 Keep medication information handy for medical consultations
- 💊 Never stop or change medications without consulting your doctor

*⚠️ This AI assistant is for informational purposes only and does not replace professional medical advice, diagnosis, or treatment.*
""")
