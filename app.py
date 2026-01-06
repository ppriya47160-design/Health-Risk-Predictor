import streamlit as st
import pandas as pd
import joblib
import base64
from pathlib import Path

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Health Risk Predictor",
    layout="centered"
)

# ================================
# BACKGROUND IMAGE
# ================================
def set_bg():
    img_path = Path("assets/bg.jpg")
    if not img_path.exists():
        st.warning("Background image not found")
        return

    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp {{
            background: rgba(255,255,255,0.7);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# ================================
# BASIC UI STYLE
# ================================
st.markdown("""
<style>
label, .stMarkdown {
    color: #020617 !important;
    font-size: 16px;
}

h1, h2, h3 {
    color: #020617;
    font-weight: 700;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox select {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    font-weight: 600;
}

.result-box {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-top: 20px;
    border-left: 6px solid #2563eb;
}
</style>
""", unsafe_allow_html=True)

# ================================
# TITLE
# ================================
st.title("🩺 Health Risk Predictor")
st.write("Predict health risk using **dataset records** or **manual lifestyle input**.")

# ================================
# LOAD MODEL & FEATURES
# ================================
model = joblib.load("health_risk_model.pkl")
train_df = pd.read_csv("data/final_dataset.csv")
feature_cols = train_df.drop(columns=["health_risk"]).columns.tolist()

# ================================
# LOAD DATASET
# ================================
df = pd.read_csv("data/real_lifestyle_data.csv")
df.columns = df.columns.str.strip()

df.rename(columns={
    "Sleep hours per day": "sleep_hours",
    "Screen time per day": "screen_time",
    "Water intake per day": "water_intake",
    "Steps walked per day": "steps",
    "Junk food  variety": "food_habit",
    "Work hours per day": "work_hours",
    "Weight (in kg)": "weight",
    "Height (in cm)": "height",
    "Stress level": "stress_level"
}, inplace=True)

food_map = {"Mostly healthy": 0, "Balanced": 1, "Mostly junk": 2}
df["food_habit"] = df["food_habit"].map(food_map)

df["height_m"] = df["height"] / 100
df["bmi"] = (df["weight"] / (df["height_m"] ** 2)).round(2)

df.drop(columns=["Timestamp", "height", "weight", "height_m"], inplace=True, errors="ignore")

# ================================
# MODE SELECTION
# ================================
mode = st.radio(
    "Select Prediction Type",
    ["Predict using Dataset Name", "Predict using Manual Entry"]
)

# ================================
# OPTION 1: DATASET NAME
# ================================
if mode == "Predict using Dataset Name":

    name = st.selectbox("Select Name from Dataset", sorted(df["Name"].unique()))

    if st.button("Predict Health Risk"):
        person = df[df["Name"] == name]
        X = person[feature_cols]
        row = person.iloc[0]

        prediction = model.predict(X)[0]

        st.markdown(f"""
        <div class="result-box">
            <h3>👤 {name}</h3>
            <h2>Health Risk Level: <b>{prediction}</b></h2>
        </div>
        """, unsafe_allow_html=True)

        # -------- Reasons --------
        st.subheader("🔍 Reasons")
        if row["bmi"] >= 25: st.write("• BMI is above normal range")
        if row["sleep_hours"] < 7: st.write("• Insufficient sleep duration")
        if row["stress_level"] >= 5: st.write("• Moderate to high stress level")
        if row["food_habit"] == 2: st.write("• Frequent junk food intake")
        if row["steps"] < 7000: st.write("• Low physical activity")
        if row["screen_time"] > 6: st.write("• High screen time")
        if row["water_intake"] < 2.5: st.write("• Low water intake")

        # -------- Suggestions --------
        st.subheader("💡 Health Suggestions")
        st.write("✅ Maintain balanced diet")
        st.write("✅ Sleep 7–8 hours daily")
        st.write("✅ Exercise regularly")
        st.write("✅ Reduce screen time")
        st.write("✅ Drink enough water")

# ================================
# OPTION 2: MANUAL ENTRY
# ================================
else:
    st.subheader("Enter Lifestyle Details")

    age = st.number_input("Age", 10, 80)
    sleep = st.number_input("Sleep hours per day", 0.0, 24.0)
    screen = st.number_input("Screen time per day (hours)", 0.0)
    water = st.number_input("Water intake per day (liters)", 0.0)
    steps = st.number_input("Steps walked per day", 0)
    work = st.number_input("Work hours per day", 0.0)
    stress = st.number_input("Stress level (1–10)", 1, 10)

    food = st.selectbox(
        "Daily food habit",
        ["Mostly healthy", "Balanced", "Mostly junk"]
    )

    bmi = st.number_input("BMI", 10.0, 50.0)

    if st.button("Predict Health Risk"):
        input_data = {
            "Age": age,
            "sleep_hours": sleep,
            "screen_time": screen,
            "water_intake": water,
            "steps": steps,
            "work_hours": work,
            "stress_level": stress,
            "food_habit": food_map[food],
            "bmi": bmi
        }

        X = pd.DataFrame([[input_data[c] for c in feature_cols]], columns=feature_cols)
        prediction = model.predict(X)[0]

        st.markdown(f"""
        <div class="result-box">
            <h2>Health Risk Level: <b>{prediction}</b></h2>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🔍 Reasons")
        if bmi >= 25: st.write("• BMI is above normal range")
        if sleep < 7: st.write("• Insufficient sleep")
        if stress >= 5: st.write("• High stress level")
        if food_map[food] == 2: st.write("• Junk food consumption")
        if steps < 7000: st.write("• Low physical activity")

        st.subheader("💡 Health Suggestions")
        st.write("✅ Follow healthy diet")
        st.write("✅ Improve sleep schedule")
        st.write("✅ Exercise daily")
        st.write("✅ Manage stress effectively")
