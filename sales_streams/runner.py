from pathlib import Path

from aggregations import ANALYSES
from data_loader import load_sales_data
from formatters import print_table


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "sales_data_sample.csv"
    frame = load_sales_data(csv_path)

    for title, func in ANALYSES.items():
        result = func(frame.copy())
        print_table(result, title=title)
        print()


if __name__ == "__main__":
    main()
