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
st.set_page_config(page_title="HerAssist", page_icon="🌸", layout="centered")

# ----------------------------
# Page Header
# ----------------------------
# ----------------------------
# Page Header
# ----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #d63384;'>FemCare Assistant 🌸</h1>
    <h4 style='text-align: center; color: #6f42c1;'>Your Trusted Women's Health Companion</h4>
    <div style="display: flex; align-items: flex-start; margin-top: 20px;">
        <!-- Text Section -->
        <div style="flex: 1; text-align: center;">
            <p style="font-size: 1.1rem; line-height: 1.6; color:#333;">
                <b>What is FemCare Assistant?</b><br>
                FemCare Assistant is your AI-powered women's health companion designed specifically for women and girls.
                Get reliable information about pregnancy, menstrual health, reproductive wellness, and women's safety.
                We're here to support you through every stage of your health journey with compassionate, evidence-based guidance, care, trust, strength, and wellness.
            </p>
        </div>
    </div>
    <hr style='margin-top:10px;margin-bottom:25px; border-color: #f8d7da;'>
""", unsafe_allow_html=True)

# ----------------------------
# Health Categories
# ----------------------------
st.markdown("### 🌺 How may I assist you today?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background-color: #fff0f6; padding: 15px; border-radius: 10px; text-align: center; 
                border: 1px solid #f8d7da; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
        <h5 style='color: #d63384; margin-bottom: 8px;'>🤰 Pregnancy</h5>
        <p style='font-size: 14px; margin: 0;'>Prenatal care, symptoms, nutrition, safety tips.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; text-align: center; 
                border: 1px solid #b6d7ff; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
        <h5 style='color: #0d6efd; margin-bottom: 8px;'>🩸 Menstrual Health</h5>
        <p style='font-size: 14px; margin: 0;'>Periods, PMS, cycle tracking, pain management.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color: #f0fff0; padding: 15px; border-radius: 10px; text-align: center; 
                border: 1px solid #b3e5b3; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
        <h5 style='color: #198754; margin-bottom: 8px;'>🛡️ Women's Wellness</h5>
        <p style='font-size: 14px; margin: 0;'>Reproductive health, safety, general wellness.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ----------------------------
# Quick Topics
# ----------------------------
st.markdown("### Popular Topics 💭")

quick_topics = [
    # Pregnancy
    "What are early pregnancy symptoms?",
    "How to manage period cramps naturally?",
    "Safe exercises during pregnancy?",
    "When should I take a pregnancy test?",
    "What foods to avoid during pregnancy?",
    "How to prepare for labor and delivery?",
    "Tips for a healthy pregnancy diet?",
    "How to deal with morning sickness?",
    "Importance of prenatal vitamins?",
    "Pregnancy complications to be aware of?",

    # Menstrual Health
    "How to track my menstrual cycle?",
    "Natural remedies for irregular periods?",
    "Why does PMS happen?",
    "How to maintain hygiene during periods?",
    "Best practices for menstrual pain relief?",
    "Heavy periods when to seek help?",
    "What are common causes of missed periods?",

    # Reproductive Wellness
    "Postpartum depression signs?",
    "Birth control options explained?",
    "How does fertility tracking work?",
    "What are common causes of infertility?",
    "Tips for improving reproductive health",
    "When should I see a gynecologist?",
    "Understanding PCOS and its symptoms?",

    # Women’s Safety & General Wellness
    "Safe travel tips during pregnancy?",
    "How to stay safe during late-night travel?",
    "Self-defense basics every woman should know?",
    "Warning signs of domestic abuse?",
    "How stress affects women’s health?",
    "Best vitamins and supplements for women?"
]


selected_topic = st.selectbox("Choose a quick topic or ask your own question:",
                              ["Select a topic..."] + quick_topics)

# ----------------------------
# User Input
# ----------------------------
st.markdown("### Ask FemCare Assistant 🎀")

# Use selected topic if available, otherwise empty text area
initial_text = selected_topic if selected_topic != "Select a topic..." else ""

user_input = st.text_area(
    "Ask your question about women's health, pregnancy, periods, or wellness:",
    value=initial_text,
    height=150,
    placeholder="What are the signs of ovulation? Is it safe to exercise during pregnancy?"
)


# ----------------------------
# Handle User Query
# ----------------------------
if st.button("Ask FemCare Assistant 🌸", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a question about women's health ⚠️")
    else:
        try:
            with st.spinner("FemCare Assistant is thinking... 💭"):
                system_prompt = (
                    "You are FemCare Assistant, a compassionate and knowledgeable AI assistant specializing in women's health, "
                    "pregnancy care, menstrual health, and women's wellness. You provide supportive, accurate, and empathetic guidance "
                    "specifically tailored for women and girls of all ages.\n\n"

                    "Your Specialization Areas:\n"
                    "1. Pregnancy & Prenatal Care: Provide information about pregnancy symptoms, stages, nutrition, exercise, "
                    "prenatal vitamins, common concerns, labor preparation, and postpartum care.\n"
                    "2. Menstrual Health: Offer guidance on menstrual cycles, period symptoms, PMS, PMDD, irregular periods, "
                    "menstrual hygiene, and cycle tracking.\n"
                    "3. Reproductive Health: Share information about fertility, ovulation, contraception, reproductive anatomy, "
                    "and common gynecological concerns.\n"
                    "4. Women's Safety & Wellness: Provide advice on women's health screenings, preventive care, mental health "
                    "during hormonal changes, and general wellness tips for women.\n"
                    "5. Adolescent Health: Address concerns specific to teenage girls, including puberty, first periods, "
                    "body changes, and health education.\n\n"

                    "Communication Style:\n"
                    "- Use warm, supportive, and non-judgmental language\n"
                    "- Be culturally sensitive and inclusive\n"
                    "- Provide practical, actionable advice when appropriate\n"
                    "- Use emojis sparingly but appropriately to convey warmth\n"
                    "- Address sensitive topics with care and discretion\n\n"

                    "Important Guidelines:\n"
                    "- Always clarify that you're an AI assistant providing general information, not medical diagnosis or treatment\n"
                    "- Emphasize the importance of consulting healthcare providers for personalized medical advice\n"
                    "- For concerning symptoms, always recommend seeking professional medical care\n"
                    "- Be especially cautious with pregnancy-related advice and always recommend prenatal care\n"
                    "- Provide emotional support while maintaining professional boundaries\n"
                    "- Include relevant lifestyle tips and self-care suggestions when appropriate\n"
                    "- Always end responses by encouraging professional consultation for specific health concerns\n\n"

                    "FORMATTING INSTRUCTIONS:\n"
                    "- Do not use asterisks (*) or any markdown formatting in your responses\n"
                    "- Do not use ** for bold text - bold formatting will be handled by the display system\n"
                    "- Write in plain text with proper punctuation and paragraph breaks\n"
                    "- Use numbers for lists (1., 2., 3.) instead of bullets or asterisks\n"
                    "- Keep your responses clean and readable without special formatting characters\n\n"

                    "Remember: Your role is to provide supportive information and guidance while empowering women to make informed "
                    "decisions about their health in consultation with qualified healthcare professionals."
                )

                response = groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=900,
                    temperature=0.7,
                    top_p=0.9
                )

                reply = response.choices[0].message.content.strip()

                # Remove any remaining asterisks and markdown formatting
                reply = reply.replace('**', '').replace('*', '').replace('##', '').replace('#', '')

                # Display response with styled container
                st.markdown("""
                    <div style='background-color: #f8f0ff; padding: 25px; border-radius: 12px; border: 1px solid #e0b3ff; margin: 20px 0;'>
                        <h5 style='color:#6f42c1; margin-bottom: 15px;'>🌸 FemCare Assistant says:</h5>
                        <div style='font-size:16px; color:#2d3748; line-height: 1.6;'>""" + reply.replace('\n',
                                                                                                          '<br>') + """</div>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error("🚨 Sorry, I encountered an error. Please try again.")
            st.code(str(e))


# ----------------------------
# Emergency Notice
# ----------------------------
st.markdown("""
<div style='background-color: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7; margin: 15px 0;'>
    <h6 style='color: #856404; margin-bottom: 10px;'>⚠️ Emergency Notice</h6>
    <p style='color: #856404; margin: 0; font-size: 14px;'>
    If you're experiencing severe bleeding, intense pain, signs of miscarriage, or any emergency symptoms, 
    please contact your healthcare provider immediately or call emergency services.
    </p>
</div>
""", unsafe_allow_html=True)
# ----------------------------
# Resources Section
# ----------------------------
st.markdown("### 📚 Helpful Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background-color: #f0f8ff; padding: 15px; border-radius: 8px; border: 1px solid #b6d7ff;'>
        <h6 style='color: #0d6efd;'>🩺 When to See a Doctor</h6>
        <ul style='font-size: 14px; color: #495057;'>
            <li>Unusual bleeding or discharge</li>
            <li>Severe menstrual pain</li>
            <li>Missed periods (if sexually active)</li>
            <li>Pregnancy confirmation</li>
            <li>Any concerning symptoms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #fff0f6; padding: 15px; border-radius: 8px; border: 1px solid #f8d7da;'>
        <h6 style='color: #d63384;'>🆘 Emergency Signs</h6>
        <ul style='font-size: 14px; color: #495057;'>
            <li>Severe abdominal pain</li>
            <li>Heavy bleeding with clots</li>
            <li>Signs of miscarriage</li>
            <li>High fever during pregnancy</li>
            <li>Difficulty breathing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
<div style='text-align: center; padding: 20px 0; color: #6c757d; border-top: 1px solid #e9ecef; margin-top: 30px;'>
    <p style='margin: 0; font-size: 14px;'>
    💝 Remember: This assistant provides general information only. Always consult with healthcare professionals for personalized medical advice.
    </p>
    <p style='margin: 5px 0 0 0; font-size: 12px; color: #adb5bd;'>
    Your health and well-being matter. Take care of yourself! 🌸
    </p>
</div>
""", unsafe_allow_html=True)
