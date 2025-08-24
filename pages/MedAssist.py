import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os


# --- Groq API Setup ---
load_dotenv()  # reads .env file (kept locally, not uploaded)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY)


# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="MedAssist", page_icon="🏥", layout="centered")

# ----------------------------
# Page Header
# ----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #000000;'>MedAssist 🧑‍⚕️</h1>
    <h4 style='text-align: center; color: #36454F;'>Your AI Medical Information Companion</h4>
    <div style="display: flex; align-items: flex-start; margin-top: 20px;">
        <!-- Text Section -->
        <div style="flex: 1; text-align: center;">
            <p style="font-size: 1.1rem; line-height: 1.6; color:#333;">
                <b>What is MedAssist?</b><br>
                MedAssist is your AI-powered medical assistant that provides reliable and accurate health guidance. 
                Get trusted insights about symptoms, treatments, lifestyle recommendations, and when to seek professional care. 
                It's designed to support your health journey with evidence-based medical knowledge, empowering you to make informed decisions for better wellness.
            </p>
        </div>
    </div>
    <hr style='margin-top:10px;margin-bottom:25px; border-color: #cfe2ff;'>
""", unsafe_allow_html=True)



# ----------------------------
# User Input
# ----------------------------
st.markdown("### Ask MedAssist💬")
user_input = st.text_area(
    "Type your medical question here (e.g. symptoms, treatments, diet, prevention):",
    height=150,
    placeholder="What are the symptoms of diabetes? How can I prevent heart disease? What should I know about vaccines?"
)

# ----------------------------
# Handle User Query
# ----------------------------
if st.button("Ask MedAssist🤖"):
    if not user_input.strip():
        st.warning("Please enter a medical question⚠️.")
    else:
        try:
            system_prompt = (
                "You are Med-Bot, an empathetic and highly knowledgeable AI assistant specializing in medical information and health support. "
                "Your primary goal is to provide accurate, helpful, and compassionate medical information to patients, "
                "caregivers, and the general public seeking health guidance.\n\n"
                "Key Guidelines for your responses:\n"
                "1. Medical Information Focus: Provide comprehensive information about various medical conditions, treatments, symptoms, "
                "prevention strategies, lifestyle recommendations, and general health guidance for all diseases and health conditions.\n"
                "2. Non-Diagnostic: Explicitly state that you are an AI assistant and cannot provide medical diagnoses, prescribe treatments, or replace a doctor's advice. "
                "Always recommend consulting a qualified healthcare professional for personal medical concerns.\n"
                "3. Symptom Guidance: If asked about symptoms, describe common symptoms of various conditions and advise on when to seek immediate medical attention or consult a doctor. "
                "Do NOT attempt to diagnose or tell the user what condition they have.\n"
                "4. Treatment & Lifestyle Guidance: Offer general treatment information, dietary advice, lifestyle recommendations, and stress the importance of personalized medical advice from healthcare professionals.\n"
                "5. Emotional Support: Respond with empathy and understanding. If the user expresses distress, offer words of comfort and suggest seeking support from mental health professionals, "
                "support groups, or trusted family/friends.\n"
                "6. Concise & Clear: Provide information clearly and concisely, avoiding overly technical jargon.\n"
                "7. Encourage Professional Consultation: Always end by encouraging the user to consult their doctor or a healthcare specialist for personalized advice."
            )

            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=800,
                temperature=0.6,
                top_p=0.9
            )

            reply = response.choices[0].message.content.strip()

            st.markdown("""
                <div style='background-color: #edf2f4; padding: 20px; border-radius: 10px; border: 1px solid #ccc;'>
                    <h5 style='color:#2b2d42;'>Med-Bot says🤖:</h5>
                    <p style='font-size:14px; color:#2b2d42;'>🗨️ """ + reply + """</p>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("🚨 Error from Groq API:")
            st.code(str(e))
