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

Run mocked resilience tests after dev confirms API route patterns:

```bash
WEB_MOCK_API_PATTERN="**/api/**" pytest -m "web and mocked"
```

Run guarded CRUD tests:

```bash
pytest -m "web and crud" --run-live-crud
```

## Reports

Pytest writes the HTML report to:

```text
reports/web/pytest_report.html
```

Failed web tests save:

- screenshots under `reports/web/screenshots`
- Playwright traces under `reports/web/traces`

## GitHub Actions CI

The workflow at `.github/workflows/web-automation.yml` runs web automation remotely.

- Pull requests to `main`: runs smoke tests.
- Pushes to `main`: runs smoke tests.
- Nightly schedule: runs non-CRUD regression.
- Manual `workflow_dispatch`: choose `smoke`, `regression`, `rbac`, `mocked`, `crud`, or `release-candidate`.

Configure these GitHub repository secrets before expecting authenticated suites to run:

```bash
LMS_BASE_URL
LMS_EMAIL
LMS_PASSWORD
LMS_API_BASE_URL
LMS_API_TOKEN
```

Optional RBAC secrets:

```bash
LMS_ADMIN_EMAIL
LMS_ADMIN_PASSWORD
LMS_COLLEGE_ADMIN_EMAIL
LMS_COLLEGE_ADMIN_PASSWORD
LMS_STUDENT_EMAIL
LMS_STUDENT_PASSWORD
LMS_STUDENT_SECONDARY_EMAIL
LMS_STUDENT_SECONDARY_PASSWORD
LMS_TPO_EMAIL
LMS_TPO_PASSWORD
LMS_HOD_EMAIL
LMS_HOD_PASSWORD
LMS_MENTOR_EMAIL
LMS_MENTOR_PASSWORD
```

CI uploads the HTML report, screenshots, and Playwright traces as workflow artifacts.
It also uploads a machine-readable `test_summary.json` and a human-readable `test_summary.md`.

For dev-team requirements around RBAC users, API cleanup, selectors, and mocked API patterns, see:

```text
docs/dev_team_enterprise_test_contract.md
```

Run CRUD manually only after confirming live test data cleanup is acceptable:

```bash
pytest -m "web and crud" --run-live-crud
```

## Useful Environment Variables

```bash
LMS_BASE_URL=https://lms.gyaanplant.co.in
LMS_EMAIL=<admin email>
LMS_PASSWORD=<admin password>
WEB_HEADLESS=true
WEB_TRACE_MODE=retain-on-failure
WEB_TEST_ID_ATTRIBUTE=data-testid
WEB_REUSE_AUTH_STATE=false
WEB_AUTH_STATE_PATH=reports/web/auth/admin_state.json
WEB_MOCK_API_PATTERN=**/api/**
LMS_API_BASE_URL=<api url for automation cleanup>
LMS_API_TOKEN=<api token for automation cleanup>
```

## Test Design Standards

- Prefer stable `data-testid` selectors when the application exposes them.
- Keep page actions in page objects.
- Keep test assertions business-readable.
- Avoid live-data pollution unless setup and cleanup are safe.
- Use markers to separate smoke, regression, CRUD, and role-based access coverage.
