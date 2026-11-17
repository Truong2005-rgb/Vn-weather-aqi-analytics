# Instructions for coding agents

## Scope and project context

These instructions apply to this repository. Read `README.md` and `HUONG_DAN.md`
before changing setup, data processing, or dashboard behavior.

This individual Python course project collects and visualizes weather and air
pollution data for 14 locations in 4 Vietnamese regional groups. It uses Requests,
pandas, Plotly Express, and Streamlit. It is a snapshot analysis project; it does
not currently train a forecast/ML model or run a continuous streaming service.

## Data flow and important files

1. `01_thu_thap_du_lieu.py` calls the two OpenWeatherMap endpoints and writes
   `weather_raw.csv` and `air_raw.csv`.
2. `02_lam_sach_va_ket_hop.py` checks missing values, deduplicates by `City`, and
   performs an inner join on `City` to write `vietnam_weather_air_merged.csv`.
3. `03_kham_pha_va_tao_cot.py` explores the merged data and adds AQI/temperature
   categories, writing `vietnam_weather_air_final.csv`.
4. `04_dashboard_app.py` reads the final CSV and renders the Streamlit dashboard.

Run commands from the repository root: the current scripts use relative CSV
paths. Preserve this behavior unless the task explicitly changes path handling.

## Working conventions

- Make focused changes and follow the existing Python style.
- Preserve Vietnamese labels and CSV column names, including accents, spaces,
  punctuation, and units. Coordinate changes across producers and consumers.
- Retain UTF-8-compatible CSV handling; existing writers use `utf-8-sig`.
- Preserve the intended `City` join, regional mapping, and classification rules
  unless changing them is part of the task. Explain resulting data differences.
- OpenWeatherMap's AQI is a 1-5 scale. Do not label it as Vietnam's VN_AQI or
  another numeric AQI scale without implementing and explaining that conversion.
- Keep raw, merged, and final data consistent. Do not hand-edit only the final
  CSV to manufacture a result or silently change the sample for a code-only fix.
- Keep the four chart views, four KPI cards, region filter, and detail table
  working when changing dashboard code, unless the task changes that scope.
- Do not add a new framework, deployment service, or ML component for an
  unrelated maintenance task.

## Setup and local dashboard

Use Python 3.10+:

```bash
python -m venv .venv
```

Activate `.venv` using the command for the current shell (see `README.md`), then:

```bash
python -m pip install -r requirements.txt
python -m streamlit run 04_dashboard_app.py
```

The bundled sample works without an API key or fresh collection. Use the local
URL printed by Streamlit, usually `http://localhost:8501`.

## API keys and fresh collection

- The collector reads `OPENWEATHERMAP_API_KEY` from the environment/local `.env`.
  `.env.example` must remain a placeholder, never a real API key.
- Never commit `.env`, credentials, or a key embedded in code, documentation,
  screenshots, error output, or a full authenticated request URL.
- Keep request timeouts. Handle request failures without disclosing credentials.
- Do not call the paid/rate-limited external API merely to verify an unrelated
  local change. Use bundled CSVs or mocked HTTP responses where appropriate.
- Collection overwrites the raw files; processing overwrites merged/final files.
  Preserve the original snapshot and use a temporary copy for validation.

When refreshing data is the task, configure the key locally and run in order:

```bash
python 01_thu_thap_du_lieu.py
python 02_lam_sach_va_ket_hop.py
python 03_kham_pha_va_tao_cot.py
python -m streamlit run 04_dashboard_app.py
```

Restart the dashboard or clear its data cache after changing the CSV files.

## Validation and accurate reporting

There is no dedicated automated test suite in the supplied package. Choose
checks appropriate to the change; do not claim a test suite passed if none ran.

- For processing changes, run scripts 02 and 03 in a temporary project copy
  containing the bundled inputs. Check keys, row counts, missing values, column
  names/types, category outputs, and consistency with the final dashboard input.
- The current bundled final snapshot has 14 rows and 18 columns, no missing
  values, and no duplicate `City` values. These are baseline expectations for
  this snapshot, not values to hard-code into processing or future live data.
- For dashboard changes, check the all-regions view, each region filter, KPI
  values, charts, and detail table against the loaded data where runtime permits.
- A syntax check alone does not establish API or dashboard behavior. Clearly
  identify checks not run because dependencies, network, or UI access are absent.
- Report screenshots come from another collection run; do not require their
  measurements to match the bundled snapshot. Keep README image links valid for
  the actual image locations in the repository.

Update the README when changing dependencies, commands, output schema, or scope.
Keep claims precise: one observation per selected location, not a historical time
series, province-wide average, national estimate, or automatically live feed.
Do not invent dataset scale, accuracy scores, speedups, or completed deployments.
