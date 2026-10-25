"""Interactive train enquiry CLI based on the supplied schedule dataset."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "Dataset1.csv"

def fmt_duration(hours):
    if pd.isna(hours):
        return "Duration unavailable (endpoint time missing or ambiguous)"
    minutes = round(hours * 60)
    return f"{minutes // 60} h {minutes % 60} min"

def main():
    data = pd.read_csv(DATA_PATH)
    data = data.drop_duplicates().sort_values(["Train_No", "Route_Number", "SN"])
    print("\\nTRAIN SCHEDULE ENQUIRY")
    print("Search by source and destination station name (partial matches accepted).")
    print("Type 'q' at either prompt to quit.\\n")
    while True:
        source = input("Source station: ").strip()
        if source.lower() == "q": break
        destination = input("Destination station: ").strip()
        if destination.lower() == "q": break
        if not source or not destination:
            print("Please enter both source and destination.\\n")
            continue
        matches = []
        for (train, route_no), group in data.groupby(["Train_No", "Route_Number"], sort=False):
            group = group.sort_values("SN").reset_index(drop=True)
            names = group["Station_Name"].astype(str)
            src = names.str.contains(source, case=False, regex=False)
            dst = names.str.contains(destination, case=False, regex=False)
            src_idx = list(src[src].index)
            dst_idx = list(dst[dst].index)
            valid = [(i, j) for i in src_idx for j in dst_idx if i < j]
            if not valid: continue
            i, j = valid[0]
            start = group.loc[i, "Departure_Time"]
            end = group.loc[j, "Arrival_time"]
            def mins(t):
                try:
                    parts = str(t).split(":")
                    return int(parts[0])*60 + int(parts[1])
                except Exception: return None
            a, b = mins(start), mins(end)
            duration = None
            if a is not None and b is not None and not (a == 0 and b == 0):
                duration = b-a
                if duration < 0: duration += 1440
            duration_hours = duration/60 if duration is not None else float("nan")
            matches.append({
                "Train_No": train, "Source": group.loc[i, "Station_Name"],
                "Destination": group.loc[j, "Station_Name"], "Departure": start,
                "Arrival": end, "Duration": fmt_duration(duration_hours),
                "Stations_In_Segment": j-i+1
            })
        if not matches:
            print("No direct scheduled train segment found for that source/destination pair. Check spelling or try a shorter station name.\\n")
        else:
            result = pd.DataFrame(matches).drop_duplicates(subset=["Train_No","Source","Destination"])
            print(f"\\nFound {len(result)} matching train(s):")
            print(result.to_string(index=False))
            print()
    print("Goodbye.")

if __name__ == "__main__":
    main()
