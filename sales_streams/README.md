# Sales Streams

Functional-style analytics pipelines for the `sales_data_sample.csv` dataset using straight pandas chaining. Each analysis is a pure function that accepts a DataFrame, applies a pipeline of `groupby`, `assign`, and `sort_values`, and returns a new DataFrame ready for console printing.

Dataset courtesy of Kaggle: [Sample Sales Data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data?resource=download).

## Highlights
- Pure functions: every helper keeps I/O at the edges and returns fresh DataFrames.
- No custom stream abstraction, just method chaining, lambdas, and aggregation maps.

## Analyses and Tests
- Queries: revenue share by product line, top customer revenue, and quarterly revenue trends with quarter-on-quarter growth calculations.
- Tests: pytest suite covers each query plus edge cases for empty or single-row DataFrames to ensure predictable behavior.

## Project Layout
```
sales_streams/
├── aggregations.py      # Functional analytics queries built with pandas
├── data_loader.py       # CSV ingestion and normalization helpers
├── formatters.py        # Pretty table utilities
├── runner.py            # Entry point that prints all analyses
├── tests/               # Pytest coverage for the analytics helpers
└── requirements.txt     # pandas + tabulate + pytest
```

## Setup
1. Create/activate a virtual environment (recommended).
2. Install dependencies:
   ```bash
   python -m pip install -r sales_streams/requirements.txt
   ```

## Run the Analyses
```bash
python sales_streams/runner.py
```
The script reads `sales_data_sample.csv`, executes every functional query, and prints tables for each result set.

## Run the Tests
```bash
python -m pytest sales_streams/tests
```
Pytest is configured (see repo-level `pytest.ini`) with `-v -ra`, so each test prints its name as it runs with a concise summary of all outcomes.

## Sample Output
```
Revenue by product line
| PRODUCTLINE      |   total_sales |   units_sold |   avg_unit_price |
|------------------|---------------|--------------|------------------|
| Classic Cars     |    3919615.66 |        33992 |           115.31 |
| Vintage Cars     |    1903150.84 |        21069 |            90.33 |
| Motorcycles      |    1166388.34 |        11663 |           100.01 |
| Trucks and Buses |    1127789.84 |        10777 |           104.65 |
| Planes           |     975003.57 |        10727 |            90.89 |
| Ships            |     714437.13 |         8127 |            87.91 |
| Trains           |     226243.47 |         2712 |            83.42 |

Top customers
| CUSTOMERNAME                 | COUNTRY   |   total_sales |
|------------------------------|-----------|---------------|
| Euro Shopping Channel        | Spain     |     912294.11 |
| Mini Gifts Distributors Ltd. | USA       |     654858.06 |
| Australian Collectors, Co.   | Australia |     200995.41 |
| Muscle Machine Inc           | USA       |     197736.94 |
| La Rochelle Gifts            | France    |     180124.90 |

Quarterly revenue
|   YEAR_ID |   QTR_ID | quarter   |   total_sales |   qoq_growth |
|-----------|----------|-----------|---------------|--------------|
|      2003 |        1 | 2003-Q1   |     445094.69 |         0.00 |
|      2003 |        2 | 2003-Q2   |     562365.22 |         0.26 |
|      2003 |        3 | 2003-Q3   |     649514.54 |         0.15 |
|      2003 |        4 | 2003-Q4   |    1860005.09 |         1.86 |
|      2004 |        1 | 2004-Q1   |     833730.68 |        -0.55 |
|      2004 |        2 | 2004-Q2   |     766260.73 |        -0.08 |
|      2004 |        3 | 2004-Q3   |    1109396.27 |         0.45 |
|      2004 |        4 | 2004-Q4   |    2014774.92 |         0.82 |
|      2005 |        1 | 2005-Q1   |    1071992.36 |        -0.47 |
|      2005 |        2 | 2005-Q2   |     719494.35 |        -0.33 |

```

## Dataset Notes
- Source: Kaggle’s [Sample Sales Data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data?resource=download), downloaded as `sales_data_sample.csv` and stored at the repository root per the challenge instructions.
- Type coercion: `data_loader.py` converts the numeric measure columns (quantity, sales, MSRP, etc.) with `pd.to_numeric` and parses `ORDERDATE` into pandas timestamps so groupings stay numeric-safe.
- Missing values: `TERRITORY` falls back to `"Unknown"`, while `STATE`/`POSTALCODE` default to empty strings so joins/grouping aren’t affected by NaNs. This assumption is captured directly in `data_loader.py`.
