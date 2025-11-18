"""Console formatting helpers for output."""

from typing import Optional

import pandas as pd
from tabulate import tabulate


def format_table(df: pd.DataFrame, title: Optional[str] = None, floatfmt: str = ".2f") -> str:
    table = tabulate(df, headers="keys", tablefmt="github", showindex=False, floatfmt=floatfmt)
    return f"{title}\n{table}" if title else table


def print_table(df: pd.DataFrame, title: Optional[str] = None, floatfmt: str = ".2f") -> None:
    print(format_table(df, title=title, floatfmt=floatfmt))
