# Train Schedule Analysis and Interactive Route Enquiry System

Python project built against the provided `Dataset1.csv` and the supplied Data Analysis Task List.

## Included work
- Level 1: dataset dimensions, train endpoints, stop counts, maximum/minimum stop routes.
- Level 2: normalized/sorted schedule, endpoint journey duration estimate, Short/Medium/Long route categories, station frequency.
- Level 3: missing-value review, exact duplicate removal, station sequence checks, verified output CSV.
- Level 4: route-duration summaries and charts.
- Level 5: station/route pivot table and cross-tabulation.
- Level 6: interactive command-line route enquiry.

## Setup
Use Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

To rerun the reusable summary pipeline:
```bash
python src/analysis.py
```

## Important interpretation notes
- `Stop_Count` includes both endpoints; `Intermediate_Stops` excludes endpoints.
- Endpoint `00:00:00` values may be placeholders. Duration is estimated from first departure to last arrival, with midnight rollover handling; unknown/ambiguous times are not invented.
- Route categories are defined for this project only: Short <4 hours, Medium 4–12 hours, Long >12 hours.
- The dataset has one observed `Route_Number` value. Pivot/cross-tab outputs preserve that fact rather than inventing route groups.
- The system uses the schedule in the provided CSV; it is not a live railway API and does not guarantee real-time running status or availability.
