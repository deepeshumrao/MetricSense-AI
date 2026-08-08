# MetricSense AI

MetricSense AI is a small Python toolkit for finding unusual values in business metric files. It can read CSV files out of the box and Excel workbooks when `openpyxl` is installed. The project includes a reusable package, a command-line interface, a Streamlit app, an email helper, tests, and GitHub Actions CI.

## Features

- Detect metric anomalies with robust median absolute deviation scoring.
- Fall back to z-score detection when requested.
- Analyze CSV, TSV, XLSX, and XLSM files.
- Export anomaly reports to CSV.
- Run from a terminal with the `metricsense` command.
- Explore uploaded files with the Streamlit app.
- Email generated reports through SMTP.
- Testable package structure with no required runtime dependencies for CSV analysis.

## Project Structure

```text
.
|-- .github/workflows/ci.yml
|-- apps/streamlit_app.py
|-- docs/PR_BODY.md
|-- docs/USAGE.md
|-- examples/sample_metrics.csv
|-- metricsense_ai/
|   |-- __init__.py
|   |-- cli.py
|   |-- detector.py
|   |-- emailer.py
|   `-- io.py
|-- tests/
|   |-- test_detector.py
|   `-- test_io.py
|-- .gitignore
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- pyproject.toml
`-- SECURITY.md
```

## Quick Start

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/deepeshumrao/MetricSense-AI.git
cd MetricSense-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[excel,app,test]"
```

Analyze the sample file:

```powershell
metricsense analyze examples/sample_metrics.csv --column revenue --output reports/anomalies.csv
```

Or run the Streamlit app:

```powershell
streamlit run apps/streamlit_app.py
```

## CLI Usage

```powershell
metricsense analyze path\to\metrics.xlsx --sheet Sheet1 --column revenue --threshold 3 --output reports\anomalies.csv
```

Useful options:

- `--column`: numeric column to analyze. If omitted, MetricSense AI chooses the first numeric column.
- `--threshold`: anomaly score threshold. Default is `3.0`.
- `--method`: choose `robust` or `zscore`.
- `--sheet`: Excel sheet name. Defaults to the active sheet.
- `--email-to`: send the generated report by email after analysis.

Email sending uses these environment variables:

```powershell
$env:METRICSENSE_SMTP_HOST="smtp.example.com"
$env:METRICSENSE_SMTP_PORT="587"
$env:METRICSENSE_SMTP_USERNAME="your-user"
$env:METRICSENSE_SMTP_PASSWORD="your-password"
$env:METRICSENSE_EMAIL_FROM="metricsense@example.com"
```

## Python API

```python
from metricsense_ai.detector import detect_anomalies
from metricsense_ai.io import load_table

rows = load_table("examples/sample_metrics.csv")
results = detect_anomalies(rows, value_column="revenue")

for item in results:
    if item.is_anomaly:
        print(item.index, item.value, item.score)
```

## Testing

```powershell
python -m unittest discover -s tests
```

## Notes

This project is designed as a practical starter package for metric anomaly detection. It is not a replacement for domain-specific monitoring, forecasting, or financial controls. Always review anomalies before acting on them.

## License

MIT License. See [LICENSE](LICENSE).
