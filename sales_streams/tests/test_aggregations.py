"""Tests for high-level analytical queries."""

from pathlib import Path
import sys

import pandas as pd
import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import aggregations


@pytest.fixture()
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PRODUCTLINE": [
                "Motorcycles",
                "Motorcycles",
                "Classic Cars",
                "Classic Cars",
                "Planes",
                "Planes",
            ],
            "CUSTOMERNAME": [
                "Land of Toys Inc.",
                "Signal Gift Stores",
                "Dragon Souvenirs",
                "Dragon Souvenirs",
                "Euro Shopping",
                "Euro Shopping",
            ],
            "COUNTRY": ["USA", "USA", "Spain", "Spain", "Spain", "Spain"],
            "SALES": [2000.0, 1500.0, 3000.0, 1000.0, 500.0, 700.0],
            "QUANTITYORDERED": [20, 15, 30, 10, 5, 7],
            "PRICEEACH": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
            "MSRP": [120.0, 120.0, 130.0, 130.0, 150.0, 150.0],
            "YEAR_ID": [2004, 2004, 2004, 2005, 2005, 2005],
            "QTR_ID": [1, 2, 1, 2, 3, 4],
            "DEALSIZE": ["Medium", "Small", "Large", "Medium", "Small", "Medium"],
            "STATUS": ["Shipped", "Shipped", "Resolved", "Resolved", "Disputed", "Shipped"],
            "TERRITORY": ["NA", "NA", "EMEA", "EMEA", "EMEA", "APAC"],
        }
    )


@pytest.fixture()
def empty_frame(sample_frame: pd.DataFrame) -> pd.DataFrame:
    return sample_frame.head(0).copy()


@pytest.fixture()
def single_row_frame(sample_frame: pd.DataFrame) -> pd.DataFrame:
    return sample_frame.head(1).copy()


def test_sales_by_product_line(sample_frame: pd.DataFrame) -> None:
    """Summarizes product-line revenue/units correctly."""
    df = aggregations.sales_by_product_line(sample_frame)
    assert df.iloc[0]["PRODUCTLINE"] == "Classic Cars"
    assert df.iloc[0]["total_sales"] == pytest.approx(4000.0)


def test_top_customers(sample_frame: pd.DataFrame) -> None:
    """Ranks customers by total sales."""
    df = aggregations.top_customers(sample_frame, top_n=2)
    assert len(df) == 2
    assert df.iloc[0]["CUSTOMERNAME"] == "Dragon Souvenirs"


def test_quarterly_performance(sample_frame: pd.DataFrame) -> None:
    """Computes per-quarter totals and QoQ growth."""
    df = aggregations.quarterly_performance(sample_frame)
    assert list(df["quarter"])[:2] == ["2004-Q1", "2004-Q2"]
    assert df.iloc[0]["qoq_growth"] == pytest.approx(0.0)
    assert df.iloc[1]["qoq_growth"] != 0.0


def test_empty_frame_returns_empty_results(empty_frame: pd.DataFrame) -> None:
    """All analytics should handle an empty DataFrame gracefully."""
    assert aggregations.sales_by_product_line(empty_frame).empty
    assert aggregations.top_customers(empty_frame).empty
    assert aggregations.quarterly_performance(empty_frame).empty


def test_single_row_frame_preserves_values(single_row_frame: pd.DataFrame) -> None:
    """A single order should flow through every aggregation unchanged."""
    row = single_row_frame.iloc[0]

    product = aggregations.sales_by_product_line(single_row_frame)
    assert len(product) == 1
    assert product.iloc[0]["total_sales"] == pytest.approx(row["SALES"])
    assert product.iloc[0]["units_sold"] == pytest.approx(row["QUANTITYORDERED"])

    customer = aggregations.top_customers(single_row_frame, top_n=5)
    assert len(customer) == 1
    assert customer.iloc[0]["CUSTOMERNAME"] == row["CUSTOMERNAME"]

    quarter = aggregations.quarterly_performance(single_row_frame)
    assert len(quarter) == 1
    assert quarter.iloc[0]["total_sales"] == pytest.approx(row["SALES"])
    assert quarter.iloc[0]["qoq_growth"] == pytest.approx(0.0)


