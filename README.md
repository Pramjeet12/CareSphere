# CareSphere - Where care, connection, and innovation meet.

**Demo Link:** [https://caresphere-pkumar12.streamlit.app/](https://caresphere-pkumar12.streamlit.app/)

## Project Overview 🏥

-----

CareSphere is an AI & ML-based healthcare web application designed to provide:

  - **Medicine Detection from Image**: Identify medicines by taking a picture of them.
  - **Find Nearby Hospitals**: Locate and get directions to hospitals in your vicinity.
  - **Asthma Detection**: Use advanced models to detect asthma.
  - **Heartbeat Condition Detection**: Analyze heart sounds to detect anomalies.
  - **Multiple Disease Prediction**: Predict the likelihood of various diseases based on user input.
  - **Personalized Health Plans**: Generate tailored diet plans.
  - **AI Bots**: Get information on general medical topics and specific women's health issues.
  - **Blood Donation & Request System**: A platform for users to donate and request blood.

The platform is accessible via a web-based interface, making healthcare services more accessible and efficient. 🌍

-----

## Features ✨

-----

1.  **Medicine Detection & Medical Assistance** 💊

      - **Medicine Detection**: Upload an image to identify a medicine.
      - **Find Hospitals**: Locate nearby hospitals and clinics. 🏥

2.  **AI & ML-Based Services** 💡

      - **Asthma Detection**: AI model for asthma diagnosis. 🌬️
      - **Heartbeat Condition Detection**: AI model for heart condition diagnosis. ❤️
      - **Multiple Disease Prediction**: Predict the likelihood of diabetes, heart attack, and lung cancer. 🤒
      - **Diet Plans**: AI-driven diet recommendations. 🍎
      - **General Medical Bot**: Ask questions about various health topics. 🤖
      - **Women’s Health Bot**: Specialized bot for women-related health queries. 👩‍⚕️

3.  **Blood Management System** ❤️

      - **Blood Donation**: Find nearby blood donation camps and centers.🩸
      - **Blood Request**: Request blood in case of an emergency.💉

-----

## Project Setup ⚙️

-----

1.  Prerequisites 🧑‍💻

      - Ensure you have the following installed:
          - Python 3.8+ 🐍
          - pip 📦
          - Virtual Environment (optional) 🌱

2.  Clone the Repository 🔁
    `git clone [https://github.com/yourusername/CareSphere.git](https://www.google.com/search?q=https://github.com/yourusername/CareSphere.git)`
    `cd CareSphere`

3.  Create Virtual Environment (Optional but Recommended) 🛠️
    `python -m venv venv`
    `source venv/bin/activate` \# On macOS/Linux
    `venv\\Scripts activate` \# On Windows

4.  Install Dependencies ⚡
    `pip install -r requirements.txt`

-----

## Datasets Used 📊

-----

  - **Medicine Image Dataset**: Used for training the medicine detection model. 🖼️
  - **Asthma Sound Data**: Used for breath sound analysis. 🎧
  - **Heartbeat Sound Data**: Used for heartbeat sound analysis. ❤️‍🩹
  - **Disease Prediction Data**: Used for training models for diabetes, heart attack, and lung cancer prediction. 📋
  - **Health & Nutrition Data**: Used for generating diet plans. 🍽️
  - **Blood Bank & Hospital Data**: Integrated with Google Maps API for location-based search. 🌍

-----

## Tools & Technologies Implemented 🛠️

-----

**Backend 🔌**

  - Python 🐍
  - Flask 🖥️
  - Firebase (Database for user data & medical records) 🔒
  - PostgreSQL (User data storage) 🗃️

**Machine Learning & AI Models 🤖**

  - Deep Learning: CNN, LSTM for image and sound-based analysis 🧠
  - Data Processing: Pandas, NumPy, Scikit-Learn, TensorFlow, Keras 📊

**Frontend & Deployment 🌐**

  - Streamlit (Web App UI/UX) 🌟
  - HTML/CSS (For additional UI customization) 🎨
  - APIs: Google Maps API, OpenAI API 📍
  - Deployment Platforms: Streamlit Cloud, GCP ☁️

-----

## Code Structure 🗂️

-----

The response has been limited to 50k tokens of the smallest files in the repo. You can remove this limitation by removing the max tokens filter.

```
├── Asthma_audioclassification.keras
├── Audio
│   ├── Asthma Detection
│   │   ├── .ipynb_checkpoints
│   │   │   └── Asthma Detection-checkpoint.ipynb
│   │   ├── Asthma Detection.ipynb
│   │   ├── Asthma Detection.pdf
│   │   └── Asthma_audioclassification.keras
│   └── Heartbeat Classifier
│       ├── .ipynb_checkpoints
│       │   └── Heartbeat Classifier-checkpoint.ipynb
│       ├── Heartbeat Classifier.ipynb
│       ├── Heartbeat Classifier.pdf
│       └── Heartbeat_audioclassification.keras
├── Diabetes_model_pickle
├── Heart_model_pickle
├── Heartbeat_audioclassification.keras
├── Homepage.py
├── Lung_cancer_model_pickle
├── Text
│   ├── Diabetes
│   │   ├── .ipynb_checkpoints
│   │   │   └── Diabetes_text-checkpoint.ipynb
│   │   ├── Diabetes_model_pickle
│   │   ├── Diabetes_text.ipynb
│   │   └── Diabetes_text.pdf
│   ├── Heart attack
│   │   ├── .ipynb_checkpoints
│   │   │   └── Heart_attack_predictor_text-checkpoint.ipynb
│   │   ├── Heart_attack_predictor_text.ipynb
│   │   ├── Heart_attack_predictor_text.pdf
│   │   └── Heart_model_pickle
│   └── Lung Cancer
│       ├── .ipynb_checkpoints
│       │   └── Lung_Cancer_text-checkpoint.ipynb
│       ├── Lung_Cancer_text.ipynb
│       ├── Lung_Cancer_text.pdf
│       └── Lung_cancer_model_pickle
├── Webapp Testing Data
│   ├── CareSphere.png
│   ├── P1AsthmaIE_5.wav
│   ├── Paracetamol-Tablets.jpg
│   └── artifact__201106021541.wav
├── pages
│   ├── BloodWarriors.py
│   ├── CardioEcho.py
│   ├── FitFuel.py
│   ├── HerAssist.py
│   ├── HospNearby.py
│   ├── MedAssist.py
│   ├── MediRxScan.py
│   ├── MultiDxPred.py
│   ├── RespEcho.py
│   └── src
│       └── components
│           └── HeartbeatResults.tsx
└── requirements.txt
```

-----

## Execution Instructions 🏃‍♂️

-----

1.  Run the Web App Locally 💻
    `streamlit run Homepage.py`

2.  Run on Google Cloud / Streamlit Cloud ☁️
    Deploy the app on Streamlit Cloud following the official documentation. Configure Google Cloud App Engine for large-scale deployment.

-----

## Future Scope 🔮

-----

  - Integration with Wearable Devices (Smartwatches for real-time health tracking) ⌚
  - Blockchain-based Medical Data Security (For secure patient records) 🔐
  - AI Voice Assistant for Health Queries 🎙️
  - More Disease Predictions (Kidney Disease, Mental Health Analysis) 🧠

-----

## Inspiration 💖

-----

The inspiration behind CareSphere stems from the need to bridge the gap between people and essential healthcare services. We wanted to create a comprehensive platform that not only provides personalized health guidance but also acts as a vital link in times of need, from locating a nearby hospital to connecting blood donors with recipients. The aim is to leverage **care, connection, and innovation** to create a seamless, efficient, and compassionate healthcare experience for everyone.

-----

## Contributing 🤝

-----

1.  Fork the repository 🍴
2.  Create a new branch (`git checkout -b feature-branch`) 🌱
3.  Commit changes (`git commit -m 'Added new feature'`) 📝
4.  Push the branch (`git push origin feature-branch`) 🚀
5.  Submit a Pull Request 🔄

-----

### Usage Guide 📖

How to use the CareSphere web app:

* From the home page, navigate to the desired feature using the sidebar.
* Each page provides a specific tool, from medical bots to blood donation services.
* Follow the on-screen instructions for each feature. For example, some pages require an image upload, while others need audio input or text queries.

### **HospNearby Demo**

[![HospNearby](https://img.youtube.com/vi/QvmzaoTJB7g/0.jpg)](https://www.youtube.com/watch?v=QvmzaoTJB7g)

### **MediRxScan Demo**

[![MediRxScan](https://img.youtube.com/vi/sRDwdajwXQA/0.jpg)](https://www.youtube.com/watch?v=sRDwdajwXQA)

### **BloodWarriors Demo**

[![BloodWarriors](https://img.youtube.com/vi/NfrY5B6yeWQ/0.jpg)](https://www.youtube.com/watch?v=NfrY5B6yeWQ)

### **RespEcho Demo**

[![RespEcho](https://img.youtube.com/vi/l14nh42kK80/0.jpg)](https://www.youtube.com/watch?v=l14nh42kK80)

### **CardioEcho Demo**

[![CardioEcho](https://img.youtube.com/vi/_Zy_bGQlJYc/0.jpg)](https://www.youtube.com/watch?v=_Zy_bGQlJYc)

### **MultiDxPred Demo**

[![MultiDxPred](https://img.youtube.com/vi/OZIIl7NQ2bI/0.jpg)](https://www.youtube.com/watch?v=OZIIl7NQ2bI)

### **FitFuel Demo**

[![FitFuel](https://img.youtube.com/vi/9vfroLDTQyk/0.jpg)](https://www.youtube.com/watch?v=9vfroLDTQyk)

### **HerAssist Demo**

[![HerAssist](https://img.youtube.com/vi/IGLn1btIQfw/0.jpg)](https://www.youtube.com/watch?v=IGLn1btIQfw)

### **MedAssist Demo**

[![MedAssist](https://img.youtube.com/vi/1CM8aF1y-ZU/0.jpg)](https://www.youtube.com/watch?v=1CM8aF1y-ZU)


