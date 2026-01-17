import pandas as pd

df = pd.read_excel("Datasets/raw/EV_CS.xlsx")

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

df["charging_start_time"] = pd.to_datetime(
    df["charging_start_time"], errors="coerce"
)
df["charging_end_time"] = pd.to_datetime(
    df["charging_end_time"], errors="coerce"
)

# Removing rows with missing start or end time
df = df.dropna(
    subset=["charging_start_time", "charging_end_time"]
)

# Removing invalid sessions means those where end time is before start time
df = df[
    df["charging_end_time"] > df["charging_start_time"]
]

# Creating derived time features
df["charging_duration_minutes"] = (
    df["charging_end_time"] - df["charging_start_time"]
).dt.total_seconds() / 60

df["hour_of_day"] = df["charging_start_time"].dt.hour
df["day_of_week"] = df["charging_start_time"].dt.day_name()

# Remove fully empty rows
df = df.dropna(how="all")


df.to_csv(
    "Datasets/preprocessed/EV_preprocessed.csv",
    index=False
)

print("Cleaned dataset saved for Power BI.")
