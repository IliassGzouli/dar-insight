# Dar Insight - Moroccan Real Estate Market Analysis

Dar Insight is an end-to-end Data Science project for exploring Moroccan real estate listings, cleaning scraped marketplace data, training a baseline price prediction model, and presenting insights through a Streamlit dashboard.

> Public release note: this repository is prepared for GitHub and LinkedIn publication with an anonymized sample dataset only. Raw scraped data, seller details, phone numbers, original listing URLs, trained pickle files, archives, and local environments are intentionally excluded from Git.

## Project Overview

| Stage | Tooling | Output |
|---|---|---|
| Scraping | Requests + Next.js JSON extraction | Local raw marketplace exports |
| Cleaning | Pandas | Local cleaned dataset |
| Feature engineering | Pandas / NumPy | ML-ready tabular features |
| Modeling | Scikit-learn | Baseline price prediction model |
| Dashboard | Streamlit + Plotly | Interactive market exploration |

## Public Dataset

The public repository includes:

```text
data/sample/sample_data.csv
```

This file is capped at 500 rows and keeps only ML-relevant fields:

- `prix`
- `surface`
- `chambres`
- `salles_de_bain`
- `etage`
- `localisation`
- `prix_par_m2`
- `categorie_prix`
- `categorie_surface`
- `type_etage`

The public sample excludes listing IDs, titles, seller names, dates, original listing URLs, phone numbers, and raw scraped page content.

## Architecture

```text
dar-insight/
├── data/
│   └── sample/
│       └── sample_data.csv
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── cleaning/
│   │   └── clean_avito.ipynb
│   ├── dashboard/
│   │   ├── Home.py
│   │   ├── pages/
│   │   └── utils/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── scraping/
├── models/
│   └── *.ipynb
├── requirements.txt
└── README.md
```

Local-only assets are ignored by Git:

- `data/raw/`
- `data/processed/`
- model binaries such as `models/*.pkl`
- virtual environments
- notebook checkpoints
- archives
- HTML/JSON dumps
- OS and cache files

## Pipeline

```text
Marketplace pages -> Scraping -> Cleaning -> Feature engineering -> EDA -> ML model -> Streamlit dashboard
```

### Scraping

The scraper extracts listing data from the Next.js `__NEXT_DATA__` JSON block. Raw scraped files are kept locally only because they may contain seller names, phone numbers, listing URLs, image links, and third-party page content.

### Cleaning

The cleaning workflow standardizes numeric columns, removes unusable records, derives price-per-square-meter, and creates categorical features for price, surface, and floor level.

### Modeling

The modeling workflow trains a baseline regression model using property characteristics such as surface, rooms, bathrooms, floor, city-derived features, and engineered ratios.

### Dashboard

The Streamlit app provides market analysis, Avito/Mubawab comparison views, insight pages, and a price prediction interface. The full dashboard expects the local cleaned dataset and trained model artifacts. The public sample is included for review and reproducibility of the project structure without exposing private scraped records.

## Installation

```bash
git clone https://github.com/your-username/dar-insight.git
cd dar-insight

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the Streamlit dashboard locally:

```bash
streamlit run src/dashboard/Home.py
```

Optional local-only workflow:

```bash
python3 src/scraping/avito_scraper.py
python3 src/models/train.py
```

The optional workflow regenerates private local data/model artifacts that are ignored by Git.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python 3.12 |
| Data | Pandas, NumPy |
| Machine Learning | Scikit-learn, Joblib |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Scraping | Requests |

## Privacy And Legal Notes

This project is intended for educational and portfolio purposes. The public repository avoids publishing raw scraped marketplace content, seller contact details, listing URLs, phone numbers, and original page dumps. If you reproduce the scraping pipeline, review the source website terms of service and applicable privacy rules before collecting or sharing data.

## Limitations

- The public sample is anonymized and capped, so it is not intended to reproduce the full model performance.
- Real estate prices depend on many features not fully represented here, such as building age, exact neighborhood, amenities, property condition, and proximity to transport.
- The model is a baseline and can be improved with broader data coverage and stronger feature engineering.

## Author

Project created as part of a Data Science learning portfolio.
