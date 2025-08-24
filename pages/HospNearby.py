import requests
import streamlit as st
from groq import Groq
import urllib.parse
import pandas as pd
from dotenv import load_dotenv
import os


# Use st.secrets instead of dotenv
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Initialize Groq client
from groq import Groq
groq_client = Groq(api_key=GROQ_API_KEY)


# Expanded list of medical specialties and health conditions
health_conditions = [
    "Nephrology",
    "Endocrinology",
    "Cardiology",
    "Dermatology",
    "Gastroenterology",
    "Pediatrics",
    "Pulmonology",
    "General Physician",
    "Oncology",
    "Neurology",
    "Orthopedics",
    "Urology",
    "Ophthalmology",
    "Gynecology",
    "ENT (Ear, Nose, Throat)",
    "Rheumatology",
    "Psychiatry",
    "Dentistry",
    "Hematology",
    "Allergy and Immunology",
    "Emergency Medicine",
    "Anesthesiology",
    "Radiology",
    "Pathology",
    "Physical Medicine & Rehabilitation",
    "Plastic Surgery",
    "General Surgery",
    "Obstetrics",
    "Infectious Diseases",
    "Geriatrics",
    "Sports Medicine",
    "Pain Management",
    "Critical Care",
    "Neonatology",
    "Interventional Cardiology"
]


# Function to get user's approximate location using Google Geolocation API
def get_location_from_google_api():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    payload = {}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to get location: {e}")
        return None


# Function to get nearby hospitals using Google Places API
def get_nearby_hospitals(lat, lng, hospital_type, radius_km):
    radius = int(radius_km * 1000)  # Convert km to meters
    if hospital_type == "Government":
        keyword = "government hospital"
    elif hospital_type == "Private":
        keyword = "private hospital"
    else:  # Both
        keyword = "hospital"

    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius={radius}&type=hospital&keyword={urllib.parse.quote(keyword)}&key={GOOGLE_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch hospitals: {e}")
        return []


# Function to get hospital details (contact and website) using Google Places API
def get_hospital_details(place_id):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={place_id}&fields=formatted_phone_number,website,formatted_address,rating,user_ratings_total&key={GOOGLE_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json().get("result", {})
        return {
            "phone": result.get("formatted_phone_number", "Not available"),
            "website": result.get("website", "Not available"),
            "address": result.get("formatted_address", "Not available"),
            "rating": result.get("rating", "N/A"),
            "total_ratings": result.get("user_ratings_total", 0)
        }
    except requests.RequestException as e:
        st.error(f"Failed to fetch details for place_id {place_id}: {e}")
        return {"phone": "Not available", "website": "Not available", "address": "Not available", "rating": "N/A",
                "total_ratings": 0}


# Function to estimate treatment prices using Groq API
def estimate_treatment_price(hospital_name, location, hospital_type, disease):
    prompt = f"""
    You are an expert in Indian healthcare pricing. Estimate the treatment cost (in INR) for the disease or department '{disease}' at a {hospital_type.lower()} hospital named '{hospital_name}' located in '{location}'.

    Consider the following:
    - Location: Urban vs. rural pricing differences (e.g., Delhi/Mumbai vs. small towns)
    - Hospital Type: Private hospitals are costlier; government hospitals are cheaper or subsidized
    - Disease/Department: Costs vary by condition, treatment type, and department
    - Include diagnostics, consultation, medication, hospital stay if relevant
    - Assume average facilities unless specified
    - Reflect affordability for middle-class Indian patients

    ⚠️ Output strictly in this format:  
    Rs X - Rs Y  
    or  
    N/A (reason)

    Do not provide any additional explanation or text.
    """

    try:
        response = groq_client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error estimating price: {e}"


# Function to generate Google Maps link
def get_google_maps_link(lat, lng, hospital_name):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&destination_place_id={urllib.parse.quote(hospital_name)}"


# Streamlit App
st.set_page_config(page_title="Hospital Finder", page_icon="🏥", layout="wide")

import streamlit as st

# Custom CSS for better styling
import streamlit as st

# Custom CSS for better styling
import streamlit as st

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    .section-header {
        color: #34495e;
        margin: 20px 0 15px 0;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
    }
    /* Equal-size feature boxes with centered text */
    .feature-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease-in-out;
        background: linear-gradient(135deg, #434343 0%, #000000 100%);
    }
    .feature-box h4 {
        margin-bottom: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    .feature-box p {
        font-size: 14px;
        margin: 0;
        opacity: 0.95;
    }
    /* Hover effect */
    .feature-box:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>🏥 Smart Hospital Finder & Cost Estimator</h1>", unsafe_allow_html=True)

# Feature boxes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Smart Search</h4>
        <p>Find nearby hospitals based on your location and medical needs with advanced filters.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>💰 Cost Estimation</h4>
        <p>Get AI-powered treatment cost estimates using advanced models for budget planning.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>🗺️ Navigation</h4>
        <p>Direct Google Maps integration for easy navigation with hospital details.</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h4>⭐ Hospital Ratings</h4>
        <p>View real user ratings and reviews to make informed decisions about hospital quality.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-box">
        <h4>📞 Contact Details</h4>
        <p>Get phone numbers, websites, and addresses with direct calling and website access.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-box">
        <h4>🏥 Hospital Types</h4>
        <p>Filter between government and private hospitals based on your budget and preferences.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)




# User inputs
st.subheader("Select Medical Condition 🔬")
disease = st.selectbox(
    "Select Medical Condition:",
    ["Select a Type"] + health_conditions,
    help="Select a medical specialty. Scroll for more options."
)

st.subheader("Select Hospital Type 🏥")
hospital_type = st.selectbox(
    "Select Hospital Type:",
    ["Government", "Private"],
    help="Choose your preferred hospital type"
)

st.subheader("Search Radius ??")
radius_km = st.number_input(
    "Search Radius (km):",
    min_value=0.5,
    max_value=50.0,
    value=5.0,
    step=0.5,
    format="%.1f",
    help="Distance to search for hospitals"
)

if st.button("🔍 Find Hospitals & Estimate Costs", type="primary", use_container_width=True):
    if disease == "Select a Type":
        st.error("❌ Please select a medical condition first!")
    else:
        with st.spinner("🌍 Getting your location..."):
            location_data = get_location_from_google_api()

        if location_data:
            lat = location_data['location']['lat']
            lng = location_data['location']['lng']
            accuracy = location_data['accuracy']
            location_name = f"Lat: {lat:.4f}, Lng: {lng:.4f}"

            # Add reverse geocoding to get place name
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}"
            try:
                geocode_response = requests.get(geocode_url)
                geocode_response.raise_for_status()
                geocode_data = geocode_response.json()

                if geocode_data['results']:
                    place_name = geocode_data['results'][0]['formatted_address']
                    st.success(
                        f"📍 Location found: {place_name} | Lat: {lat:.4f}, Lng: {lng:.4f} (±{accuracy} meters accuracy)")
                else:
                    st.success(f"📍 Location found: Lat: {lat:.4f}, Lng: {lng:.4f} (±{accuracy} meters accuracy)")
            except:
                st.success(f"📍 Location found: Lat: {lat:.4f}, Lng: {lng:.4f} (±{accuracy} meters accuracy)")

            # Search for hospitals
            with st.spinner("🏥 Searching for nearby hospitals..."):
                hospitals = get_nearby_hospitals(lat, lng, hospital_type, radius_km)

        if hospitals:
            st.markdown(f"<h3 class='section-header'>🏥 Found {len(hospitals[:10])} Nearby Hospitals</h3>",
                        unsafe_allow_html=True)

            for idx, hospital in enumerate(hospitals[:10], 1):
                name = hospital.get("name", "Unknown Hospital")
                place_id = hospital.get("place_id")
                hospital_lat = hospital.get("geometry", {}).get("location", {}).get("lat", lat)
                hospital_lng = hospital.get("geometry", {}).get("location", {}).get("lng", lng)

                # Get detailed hospital information
                with st.spinner(f"Getting details for {name}..."):
                    details = get_hospital_details(place_id) if place_id else {
                        "phone": "Not available",
                        "website": "Not available",
                        "address": hospital.get("vicinity", "Not available"),
                        "rating": "N/A",
                        "total_ratings": 0
                    }

                    # Estimate treatment price
                    price = estimate_treatment_price(name, details["address"], hospital_type, disease)

                # Create hospital card
                with st.container():
                    st.markdown(f"""
                    <div class="hospital-card">
                        <h4>🏥 {idx}. {name}</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    # Hospital details in columns
                    info_col1, info_col2, info_col3 = st.columns(3)

                    with info_col1:
                        st.markdown(f"**Address:** {details['address']}")
                        if details['rating'] != "N/A":
                            st.markdown(f"**Rating:** {details['rating']}/5 ({details['total_ratings']} reviews)")
                        else:
                            st.markdown("**Rating:** Not rated")

                    with info_col2:
                        st.markdown(f"**Estimated Cost:** {price}")
                        if details['phone'] != "Not available":
                            st.markdown(f"**Phone:** [{details['phone']}](tel:{details['phone']})")
                        else:
                            st.markdown("**Phone:** Not available")

                    with info_col3:
                        if details['website'] != "Not available":
                            st.markdown(f"**Website:** [Visit Website]({details['website']})")
                        else:
                            st.markdown("**Website:** Not available")

                        # Google Maps link
                        maps_link = get_google_maps_link(hospital_lat, hospital_lng, name)
                        st.markdown(f"**Directions:** [Open in Google Maps]({maps_link})")

                    # Action buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)

                    with btn_col1:
                        if details['phone'] != "Not available":
                            st.link_button("📞 Call Now", f"tel:{details['phone']}", use_container_width=True)

                    with btn_col2:
                        if details['website'] != "Not available":
                            st.link_button("🌐 Visit Website", details['website'], use_container_width=True)

                    with btn_col3:
                        st.link_button("🗺️ Get Directions", maps_link, use_container_width=True)

                    st.markdown("---")
        else:
            st.error("❌ Unable to determine your location. Please check your internet connection and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 30px;'>
    <h4>⚠️ Important Disclaimer</h4>
    <p>This app provides information about hospitals and estimated costs for reference only. 
    Actual costs may vary significantly based on specific treatments, hospital facilities, and individual cases. 
    Please consult with healthcare providers directly for accurate pricing and medical advice. 
    This app does not endorse any particular hospital or healthcare provider.</p>
    <p><strong>🚨 In case of emergency, please call 108 (Emergency Services) or visit the nearest hospital immediately.</strong></p>
</div>
""", unsafe_allow_html=True)
