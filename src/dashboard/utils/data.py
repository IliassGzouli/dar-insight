from pathlib import Path

import pandas as pd


LOCAL_DATA_PATH = Path("data/processed/clean_data.csv")
PUBLIC_SAMPLE_PATH = Path("data/sample/sample_data.csv")


def load_market_data() -> pd.DataFrame:
    """Load local full data when available, otherwise use the public sample."""
    data_path = LOCAL_DATA_PATH if LOCAL_DATA_PATH.exists() else PUBLIC_SAMPLE_PATH
    df = pd.read_csv(data_path)
    df["ville"] = df["localisation"].str.split(",").str[0].str.strip()
    return df
