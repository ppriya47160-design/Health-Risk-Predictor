🩺 Health Risk Predictor

A machine learning–based web application that predicts an individual’s health risk level using lifestyle and daily habit data.
The system helps in identifying silent health risks early and provides personalized health suggestions.

🚀   Live Application

🔗  Deployed App:
https://health-risk-predictor-pkvaz5exrgb5jkj7ws5dkc.streamlit.app

📌 Project Overview

The Silent Health Risk Predictor analyzes lifestyle factors such as sleep, stress, physical activity, food habits, and BMI to classify health risk into:

🟢 Low Risk

🟡 Medium Risk

🔴 High Risk

This project demonstrates the use of machine learning, data preprocessing, and cloud deployment using Streamlit.

🎯  Key Features

🔍  Dataset-based Prediction

Select a name from the dataset

Predict health risk instantly

✍️   Manual Entry Prediction

Enter lifestyle details manually

Real-time health risk prediction

🧠   Machine Learning Model

Random Forest Classifier

Trained on real lifestyle survey data

💡  Explainable Results

Shows reasons for predicted risk

Provides health improvement suggestions

🌐  Cloud Deployed

Hosted using Streamlit Cloud

GitHub integrated CI/CD

🛠️  Technologies Used
Programming Language : Python
Machine Learning :	Scikit-learn
Data Processing	: Pandas, NumPy
Model Persistence :	Joblib
Web Framework :	Streamlit
Deployment : Streamlit Cloud
Version Control :	Git & GitHub

📂   Project Structure
 ## Health-Risk-Predictor/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies
├── health_risk_model.pkl       # Trained ML model
│
├── data/
│   ├── real_lifestyle_data.csv
│   ├── clean_lifestyle_data.csv
│   └── final_dataset.csv
│
├── assets/
│   └── bg.jpg                  # Background image
│
├── preprocess.py               # Data preprocessing
├── label_data.py               # Risk labeling logic
├── train_model.py              # Model training
├── predict_by_name.py          # Dataset name-based prediction
└── README.md

🧪  Machine Learning Workflow

Data Collection

Lifestyle data collected via Google Forms

Data Preprocessing

Cleaning, encoding categorical values

BMI calculation

Label Generation

Health risk labeled as Low / Medium / High

Model Training

Random Forest Classifier

Feature selection and evaluation

Deployment

Model saved using Joblib

Streamlit app deployed via GitHub

📊   Input Features

Age

Sleep hours per day

Screen time per day

Water intake

Steps walked per day

Work hours

Stress level

Food habit

BMI

🧾  Output

Health Risk Level

Risk Reasons

Personalized Health Suggestions

▶️  How to Run Locally
# Clone repository
git clone https://github.com/ppriya47160-design/Health-Risk-Predictor.git

# Navigate to project
cd Health-Risk-Predictor

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
