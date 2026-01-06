import streamlit as st
import pandas as pd
import joblib

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Silent Health Risk Predictor",
    layout="centered"
)

# =================================================
# SIMPLE CLEAN BACKGROUND (NO IMAGE – BEST READABILITY)
# =================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc, #eef2f7);
}

label, .stMarkdown {
    color: #0f172a !important;
    font-size: 16px;
    font-weight: 500;
}

h1, h2, h3 {
    color: #020617;
    font-weight: 700;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox select {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #cbd5e1;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
}

/* Glass result card */
.glass-card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    border: 1px solid rgba(0,0,0,0.08);
}

/* Risk dot */
.risk-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

.low { background-color: #22c55e; }
.medium { background-color: #facc15; }
.high { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# =================================================
# TITLE
# =================================================
st.title("🩺 Silent Health Risk Predictor")
st.write("Enter your lifestyle details to **predict health risk instantly**.")

# =================================================
# LOAD MODEL & FEATURE ORDER
# =================================================
model = joblib.load("health_risk_model.pkl")
train_df = pd.read_csv("data/final_dataset.csv")
feature_cols = train_df.drop(columns=["health_risk"]).columns.tolist()

# =================================================
# INPUT SECTION (SINGLE PAGE)
# =================================================
st.subheader("👤 Personal & Lifestyle Details")

name = st.text_input("Name")
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

food_map = {"Mostly healthy": 0, "Balanced": 1, "Mostly junk": 2}
food_encoded = food_map[food]

# =================================================
# PREDICT BUTTON
# =================================================
if st.button("🔍 Predict Health Risk"):

    input_data = {
        "Age": age,
        "sleep_hours": sleep,
        "screen_time": screen,
        "water_intake": water,
        "steps": steps,
        "work_hours": work,
        "stress_level": stress,
        "food_habit": food_encoded,
        "bmi": bmi
    }

    X = pd.DataFrame([[input_data[c] for c in feature_cols]],
                     columns=feature_cols)

    prediction = model.predict(X)[0]
    risk_class = prediction.lower()

    # =================================================
    # RESULT CARD
    # =================================================
    st.markdown(f"""
    <div class="glass-card">
        <h3>
            <span class="risk-dot {risk_class}"></span>
            Health Risk Level: <b>{prediction}</b>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # =================================================
    # REASONS
    # =================================================
    st.subheader("🔍 Reasons")

    if bmi >= 30:
        st.write("• BMI is in obese range")
    elif bmi >= 25:
        st.write("• BMI is above normal range")
    else:
        st.write("• BMI is within healthy range")

    if sleep < 5:
        st.write("• Very low sleep duration")
    elif sleep < 7:
        st.write("• Slightly insufficient sleep")

    if stress >= 8:
        st.write("• Very high stress level")
    elif stress >= 5:
        st.write("• Moderate stress level")

    if food_encoded == 2:
        st.write("• Frequent junk food consumption")

    if steps < 7000:
        st.write("• Low physical activity")

    if screen > 6:
        st.write("• High daily screen time")

    if water < 2.5:
        st.write("• Low daily water intake")

    # =================================================
    # SUGGESTIONS
    # =================================================
    st.subheader("💡 Health Suggestions")

    if bmi >= 25:
        st.write("✅ Maintain balanced diet and exercise regularly")

    if sleep < 7:
        st.write("✅ Aim for 7–8 hours of sleep daily")

    if stress >= 5:
        st.write("✅ Practice meditation or relaxation techniques")

    if food_encoded == 2:
        st.write("✅ Reduce junk food and eat more fruits & vegetables")

    if steps < 7000:
        st.write("✅ Increase daily walking or physical activity")

    if screen > 6:
        st.write("✅ Limit screen time and take regular breaks")

    if water < 2.5:
        st.write("✅ Drink at least 2.5–3 liters of water daily")
