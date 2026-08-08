# Contributing

Thanks for helping improve MetricSense AI.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[excel,app,test]"
```

## Checks

Run tests before opening a pull request:

```powershell
python -m unittest discover -s tests
```

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Add or update tests for behavior changes.
- Update README or docs when user-facing behavior changes.
- Do not commit credentials, personal data, generated reports, or local `.env` files.
