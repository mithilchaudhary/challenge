# Intuit Build Challenge

Two independent exercises from Intuit's build challenge that showcase concurrency patterns and functional data analytics:

| Folder | Summary |
| --- | --- |
| `producer_consumer/` | In-memory producer/consumer queue with tests (Assignment 1). |
| `sales_streams/` | Functional pandas analytics on `sales_data_sample.csv` with pretty tables and unit tests (Assignment 2). |

## Prerequisites
- Python 3.11+ (tested locally)
- `pip` for dependency management
- The existing CSV dataset `sales_data_sample.csv` at the repository root

## Environment Setup
Install the dependencies required for the analytics project (the producer/consumer example only uses the standard library):

```bash
python -m pip install -r sales_streams/requirements.txt
```

For run/test instructions, see `producer_consumer/README.md` and `sales_streams/README.md`.

## Notes
- Each sub-project has its own README that dives into design choices and usage details.
