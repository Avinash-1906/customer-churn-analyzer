# Customer Churn Analyzer

A data analysis project built with Python and MySQL that identifies customer churn patterns from subscription data.

## What it does
- Calculates churn rate by plan type (Basic, Standard, Premium)
- Analyzes average customer lifetime per plan
- Shows monthly churn trends over time
- Identifies high-risk active customers who have been inactive for 180+ days

## Tech Stack
- Python 3
- MySQL
- mysql-connector-python

## Project Structure
| File | Purpose |
|------|---------|
| `generate_data.py` | Generates 100 fake customer records and saves to CSV |
| `load_data.py` | Reads CSV and loads data into MySQL |
| `analyze.py` | Contains all SQL query functions |
| `report.py` | Prints formatted analysis report to terminal |

## How to Run
1. Install dependency: `pip install mysql-connector-python`
2. Set up MySQL and update credentials in `load_data.py` and `analyze.py`
3. Run in order:
   - `python generate_data.py`
   - `python load_data.py`
   - `python report.py`
