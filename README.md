# Medical Insurance Cost Explorer

An interactive, dark-themed healthcare analytics dashboard for exploring numerical medical charges across age, body mass index, smoking status and U.S. regions.

**Stack:** Python · Pandas · Plotly · Streamlit

## What it does

- Filter records by age, BMI, smoking status and region.
- Compare age-versus-charges and BMI-versus-charges scatter plots using consistent encodings.
- Compare mean or median charges by region, calculated on the currently filtered records.
- Inspect metrics and original source fields; export **only the filtered records** to CSV.
- Reuse the validated dataset via `st.cache_data`, keeping widget interactions responsive.

## Data

The bundled file is `data/insurance.csv`, supplied with the project. It contains 1,338 rows and seven fields: `age`, `sex`, `bmi`, `children`, `smoker`, `region` and `charges`. The provided file has no missing values and one exact duplicate row; the application retains it rather than silently changing the source sample.

**Interpretation boundary:** The CSV itself does not specify the source's data-collection period, insurance carrier, currency or detailed billing methodology. The dashboard therefore labels charges as *dataset units*, avoids claims about premiums or prices today, and presents associations rather than causal claims.

## Run locally

Python 3.10+ recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

For Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Run tests

```bash
python3 -m pip install pytest
python3 -m pytest -q
```

## Deploy to Streamlit Community Cloud

1. Push the complete project, including `data/insurance.csv`, to your GitHub repository.
2. Visit https://share.streamlit.io and create an app from that repository's `main` branch.
3. Set the main file path to `app.py`. Streamlit detects `requirements.txt` and `.streamlit/config.toml`.
4. Open the deployed app and verify that filters, charts and CSV export work.

## Project layout

```text
medical-insurance-cost-analytics/
├── app.py
├── analytics.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── insurance.csv
└── tests/
    └── test_analytics.py
```

## Development transparency

AI assistance was used for application scaffolding, visual-design suggestions, and documentation drafting. The repository owner should review, test, adapt and take responsibility for the analysis and final implementation.
