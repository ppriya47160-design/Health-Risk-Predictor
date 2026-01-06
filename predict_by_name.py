import pandas as pd
import joblib

# -----------------------------
# Load trained ML model
# -----------------------------
model = joblib.load("health_risk_model.pkl")

# -----------------------------
# Load original dataset
# -----------------------------
df = pd.read_csv("data/real_lifestyle_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Rename columns
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

# Encode food habit
food_map = {
    "Mostly healthy": 0,
    "Balanced": 1,
    "Mostly junk": 2
}
df["food_habit"] = df["food_habit"].map(food_map)

# Calculate BMI
df["height_m"] = df["height"] / 100
df["bmi"] = df["weight"] / (df["height_m"] ** 2)
df["bmi"] = df["bmi"].round(2)

# Drop unused columns
df.drop(columns=[
    "Timestamp",
    "Breakfast time",
    "Lunch time",
    "Dinner time",
    "height_m",
    "height",
    "weight"
], inplace=True)

# -----------------------------
# User input (NAME ONLY)
# -----------------------------
name = input("Enter name: ").strip()

person = df[df["Name"].str.lower() == name.lower()]

if person.empty:
    print("\n❌ Name not found in dataset\n")
else:
    # -----------------------------
    # Load training feature order
    # -----------------------------
    train_df = pd.read_csv("data/final_dataset.csv")
    feature_cols = train_df.drop(columns=["health_risk"]).columns
    X = person[feature_cols]

    # -----------------------------
    # Predict health risk
    # -----------------------------
    prediction = model.predict(X)[0]

    # -----------------------------
    # Generate ALL reasons
    # -----------------------------
    row = person.iloc[0]
    reasons = []

    # BMI
    if row["bmi"] >= 30:
        reasons.append("BMI is in obese range")
    elif row["bmi"] >= 25:
        reasons.append("BMI is above normal range")
    else:
        reasons.append("BMI is within healthy range")

    # Sleep
    if row["sleep_hours"] < 5:
        reasons.append("Very low sleep duration")
    elif row["sleep_hours"] < 7:
        reasons.append("Sleep duration is slightly low")
    else:
        reasons.append("Adequate sleep duration")

    # Stress
    if row["stress_level"] >= 8:
        reasons.append("Very high stress level")
    elif row["stress_level"] >= 5:
        reasons.append("Moderate stress level")
    else:
        reasons.append("Low stress level")

    # Food habit
    if row["food_habit"] == 2:
        reasons.append("Mostly consumes junk food")
    elif row["food_habit"] == 1:
        reasons.append("Balanced food habit")
    else:
        reasons.append("Mostly healthy food habit")

    # Physical activity (steps)
    if row["steps"] < 3000:
        reasons.append("Very low physical activity")
    elif row["steps"] < 7000:
        reasons.append("Moderate physical activity")
    else:
        reasons.append("Good physical activity level")

    # Screen time
    if row["screen_time"] > 8:
        reasons.append("High daily screen time")
    elif row["screen_time"] > 5:
        reasons.append("Moderate screen time")
    else:
        reasons.append("Low screen time")

    # Water intake
    if row["water_intake"] < 1.5:
        reasons.append("Low daily water intake")
    elif row["water_intake"] < 2.5:
        reasons.append("Moderate water intake")
    else:
        reasons.append("Adequate water intake")

    # Work hours
    if row["work_hours"] > 10:
        reasons.append("Long working hours")
    elif row["work_hours"] < 4:
        reasons.append("Very low daily activity hours")
    else:
        reasons.append("Normal working hours")

    # -----------------------------
    # Final Output
    # -----------------------------
    print("\n==============================")
    print(f"👤 Name: {name}")
    print(f"⚠️ Health Risk Level: {prediction}")
    print("\nDetailed Reason(s):")
    for r in reasons:
        print(f"- {r}")
    print("==============================\n")
