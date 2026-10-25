# Train Schedule Analysis — Project Report

## Project overview
This project follows the six levels in the supplied Sysslan IT Solutions Data Analysis Task List: basic data review, simple processing, data quality checks, basic analysis and visualization, advanced pivot/cross-tab analysis, and an interactive route enquiry system.

## Dataset overview
- Source file: `data/Dataset1.csv`
- Rows: **186,074**
- Columns: **12**
- Unique train numbers: **11,113**
- Unique station codes: **8,147**
- Exact duplicate rows detected before removal: **0**
- Missing values in original CSV: **0**

## Processing assumptions
- Rows are ordered by `Train_No`, `Route_Number`, and `SN`.
- The first row is treated as the starting station and the last row as the ending station for each train/route.
- `Stop_Count` counts all station records in a route, including endpoints; `Intermediate_Stops` excludes the first and last station.
- `00:00:00` can be a placeholder at route endpoints in this dataset. Duration is estimated using first-station departure and last-station arrival. Negative durations roll over midnight by adding 24 hours. Missing/ambiguous endpoint times remain unknown rather than being fabricated.
- Route categories are project-defined: Short < 4 hours, Medium 4–12 hours, Long > 12 hours. These are analysis thresholds, not official railway classifications.
- The provided data has a single observed `Route_Number` value (1); station-route cross-tabs therefore reflect only the supplied route-number coding.

## Key results
- Train/route summaries generated: **11,113**
- Routes with computable endpoint duration: **11,113**
- Longest station-record route: Train **53041**, HOWRAH JN. → JAYNAGAR, **118 station records**.
- Fewest station-record route: Train **557**, URKURA → PANJIPARA, **2 station records**.
- Most frequently represented station: **CST-MUMBAI** (1,027 unique trains).

## Deliverables
- `outputs/train_summary.csv` — start/end stations, stop counts, route, endpoint duration, category, and order checks.
- `outputs/cleaned_train_schedule.csv` — sorted, deduplicated schedule with parsed time-in-minutes helper columns.
- `outputs/station_frequency.csv` — station-wise train frequency.
- `outputs/route_type_duration.csv` — average and median duration by route category.
- `outputs/station_route_pivot.csv` and `outputs/station_route_crosstab.csv` — advanced analysis tables.
- `outputs/charts/` — generated visualizations.
- `src/analysis.py` — reusable analysis pipeline.
- `app.py` — interactive command-line train enquiry system.
