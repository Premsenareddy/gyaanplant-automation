# GyaanPlant Web Test Automation Framework

A Python web automation framework for the GyaanPlant LMS admin application.

The framework uses Pytest, Playwright, Page Object Model design, reusable fixtures, and HTML reporting for smoke and regression coverage.

## Key Features

- Web automation with Playwright
- Pytest-based test execution
- Page Object Model structure under `pages/web`
- Environment-driven configuration
- Screenshot capture on failure
- Playwright trace retention on failure
- Self-contained HTML report generation
- Marker-based suite selection for smoke, regression, CRUD, and RBAC tests

## Project Structure

```text
gyaanplant_automation
├── config/              # Environment and web runtime settings
├── core/                # Playwright driver factory
├── docs/                # Architecture and implementation notes
├── pages/web/           # Web page objects
├── reports/             # Generated test reports and artifacts
├── testdata/            # Test input data
├── tests/web/           # Web test cases
├── utils/               # Shared helpers
├── conftest.py          # Pytest fixtures and failure artifacts
├── pytest.ini           # Pytest configuration
├── requirement.txt      # Python dependencies
└── Makefile             # Quick run commands
```

## Install

```bash
pip install -r requirement.txt
playwright install chromium
```

## Run Tests

Run all tests:

```bash
pytest
```

Run all web tests:

```bash
pytest -m web
```

Run smoke tests:

```bash
pytest -m "web and smoke"
```

Run regression tests:

```bash
pytest -m "web and regression"
```

## Reports

Pytest writes the HTML report to:

```text
reports/web/pytest_report.html
```

Failed web tests save:

- screenshots under `reports/web/screenshots`
- Playwright traces under `reports/web/traces`

## Useful Environment Variables

```bash
LMS_BASE_URL=https://lms.gyaanplant.co.in
LMS_EMAIL=<admin email>
LMS_PASSWORD=<admin password>
WEB_HEADLESS=true
WEB_TRACE_MODE=retain-on-failure
WEB_TEST_ID_ATTRIBUTE=data-testid
```

## Test Design Standards

- Prefer stable `data-testid` selectors when the application exposes them.
- Keep page actions in page objects.
- Keep test assertions business-readable.
- Avoid live-data pollution unless setup and cleanup are safe.
- Use markers to separate smoke, regression, CRUD, and role-based access coverage.
