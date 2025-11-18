"""Composable analytical queries expressed with plain pandas pipelines."""

import pandas as pd


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / denominator.replace({0: pd.NA})


def sales_by_product_line(frame: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        frame.groupby("PRODUCTLINE", dropna=False)
        .agg(total_sales=("SALES", "sum"), units_sold=("QUANTITYORDERED", "sum"))
        .reset_index()
    )
    grouped["avg_unit_price"] = _safe_divide(grouped["total_sales"], grouped["units_sold"])
    return grouped.sort_values("total_sales", ascending=False).reset_index(drop=True)


def top_customers(frame: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    ranked = (
        frame.groupby(["CUSTOMERNAME", "COUNTRY"], dropna=False)
        .agg(total_sales=("SALES", "sum"))
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )
    return ranked.head(top_n).reset_index(drop=True)


def quarterly_performance(frame: pd.DataFrame) -> pd.DataFrame:
    ordered = (
        frame.groupby(["YEAR_ID", "QTR_ID"], dropna=False)
        .agg(total_sales=("SALES", "sum"))
        .reset_index()
        .sort_values(["YEAR_ID", "QTR_ID"], ascending=[True, True])
    )
    if ordered.empty:
        ordered = ordered.assign(
            quarter=pd.Series(dtype="object"), qoq_growth=pd.Series(dtype="float64")
        )
        return ordered[["YEAR_ID", "QTR_ID", "quarter", "total_sales", "qoq_growth"]]
    ordered["quarter"] = (
        ordered["YEAR_ID"].astype(int).astype(str)
        + "-Q"
        + ordered["QTR_ID"].astype(int).astype(str)
    )
    ordered["qoq_growth"] = ordered["total_sales"].pct_change().fillna(0.0)
    return ordered[["YEAR_ID", "QTR_ID", "quarter", "total_sales", "qoq_growth"]]


ANALYSES = {
    "Revenue by product line": sales_by_product_line,
    "Top customers": top_customers,
    "Quarterly revenue": quarterly_performance,
}
