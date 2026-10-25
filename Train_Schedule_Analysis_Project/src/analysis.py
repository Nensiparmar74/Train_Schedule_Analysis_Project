"""Reusable data preparation and analysis for the Train Schedule Analysis project."""
from pathlib import Path
import pandas as pd
import numpy as np

def time_to_minutes(value):
    if pd.isna(value): return np.nan
    parsed = pd.to_datetime(str(value), format="%H:%M:%S", errors="coerce")
    if pd.isna(parsed): return np.nan
    return parsed.hour * 60 + parsed.minute + parsed.second / 60

def build_summary(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.drop_duplicates().sort_values(["Train_No", "Route_Number", "SN"], kind="stable")
    df["arrival_min"] = df["Arrival_time"].map(time_to_minutes)
    df["departure_min"] = df["Departure_Time"].map(time_to_minutes)
    rows = []
    for (train, route), group in df.groupby(["Train_No", "Route_Number"], sort=False):
        group = group.sort_values("SN")
        first, last = group.iloc[0], group.iloc[-1]
        start, end = first["departure_min"], last["arrival_min"]
        duration = np.nan
        if pd.notna(start) and pd.notna(end) and not (start == 0 and end == 0):
            duration = end - start
            if duration < 0: duration += 1440
        hours = duration / 60 if pd.notna(duration) else np.nan
        route_type = "Unknown" if pd.isna(hours) else ("Short" if hours < 4 else ("Medium" if hours <= 12 else "Long"))
        names = group["Station_Name"].astype(str).tolist()
        rows.append({
            "Train_No": train, "Route_Number": route, "Starting_Station": names[0],
            "Ending_Station": names[-1], "Stop_Count": len(group),
            "Intermediate_Stops": max(len(group)-2, 0),
            "Start_Departure": first["Departure_Time"], "End_Arrival": last["Arrival_time"],
            "Journey_Duration_Minutes": duration, "Journey_Duration_Hours": hours,
            "Route_Type": route_type, "Distance_Monotonic_NonDecreasing": group["Distance"].is_monotonic_increasing,
            "Route": " -> ".join(names)
        })
    return pd.DataFrame(rows)

def main():
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / "data" / "Dataset1.csv")
    summary = build_summary(data)
    (root / "outputs").mkdir(exist_ok=True)
    summary.to_csv(root / "outputs" / "train_summary.csv", index=False)
    station = (data.groupby(["Station_Code", "Station_Name"])
               .agg(Train_Station_Records=("Train_No", "size"), Unique_Trains=("Train_No", "nunique"))
               .reset_index().sort_values("Unique_Trains", ascending=False))
    station.to_csv(root / "outputs" / "station_frequency.csv", index=False)
    print(f"Processed {len(data):,} rows into {len(summary):,} train summaries.")
if __name__ == "__main__":
    main()
