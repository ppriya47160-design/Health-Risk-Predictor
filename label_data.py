import pandas as pd

# Load cleaned data
df = pd.read_csv("data/clean_lifestyle_data.csv")

def label_risk(row):
    # HIGH RISK
    if (
        row["bmi"] >= 30 or
        row["sleep_hours"] < 5 or
        row["stress_level"] >= 8 or
        row["food_habit"] == 2
    ):
        return "High"

    # MEDIUM RISK
    elif (
        25 <= row["bmi"] < 30 or
        row["stress_level"] >= 5
    ):
        return "Medium"

    # LOW RISK
    else:
        return "Low"

# Apply risk labeling
df["health_risk"] = df.apply(label_risk, axis=1)

# Save final dataset
df.to_csv("data/final_dataset.csv", index=False)

print("✅ Health risk labels added successfully!")
