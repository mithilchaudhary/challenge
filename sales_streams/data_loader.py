"""Utilities for loading and normalizing the sales CSV."""

from pathlib import Path
from typing import Iterable

import pandas as pd

# Columns that should be numeric in the typed DataFrame.
_NUMERIC_COLUMNS: tuple[str, ...] = (
    "ORDERNUMBER",
    "QUANTITYORDERED",
    "PRICEEACH",
    "ORDERLINENUMBER",
    "SALES",
    "QTR_ID",
    "MONTH_ID",
    "YEAR_ID",
    "MSRP",
)


def _coerce_numeric(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Returns a copy with the requested columns converted via pd.to_numeric."""
    frame = df.copy()
    for column in columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def load_sales_data(csv_path: str | Path) -> pd.DataFrame:
    """Load the classic CSV export and return a typed pandas DataFrame."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Missing sales CSV at {path!s}")

    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")
    df = _coerce_numeric(df, _NUMERIC_COLUMNS)
    df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")
    df["TERRITORY"] = df["TERRITORY"].fillna("Unknown")
    df["STATE"] = df["STATE"].fillna("")
    df["POSTALCODE"] = df["POSTALCODE"].fillna("").astype(str)
    return df
