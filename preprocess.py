import pandas as pd

# Load raw data
df = pd.read_csv("data/real_lifestyle_data.csv")

# 1️⃣ Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# 2️⃣ Rename columns to standard ML-friendly names
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

# 3️⃣ Drop columns not needed for ML
df.drop(columns=[
    "Name",
    "Timestamp",
    "Breakfast time",
    "Lunch time",
    "Dinner time"
], inplace=True)

# 4️⃣ Calculate BMI
df["height_m"] = df["height"] / 100
df["bmi"] = df["weight"] / (df["height_m"] ** 2)
df["bmi"] = df["bmi"].round(2)

df.drop(columns=["height_m", "height", "weight"], inplace=True)

# 5️⃣ Encode food habit
food_map = {
    "Mostly healthy": 0,
    "Balanced": 1,
    "Mostly junk": 2
}
df["food_habit"] = df["food_habit"].map(food_map)

# 6️⃣ Ensure numeric stress level
df["stress_level"] = df["stress_level"].astype(int)

# 7️⃣ Save cleaned dataset
df.to_csv("data/clean_lifestyle_data.csv", index=False)

print("✅ Preprocessing completed successfully!")
print("✅ Meal time removed & BMI calculated")
