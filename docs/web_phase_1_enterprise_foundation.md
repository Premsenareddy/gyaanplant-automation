# Web Automation Phase 1: Enterprise Foundation

This phase improves web test reliability and diagnostics without requiring source-code changes in the LMS web application.

## What Changed

- Playwright now uses a configurable test-id attribute, defaulting to `data-testid`.
- Web browser viewport, tracing, video recording, and artifact folders are configurable through environment variables.
- Failed web tests save screenshots under `reports/web/screenshots`.
- Playwright traces are retained for failed web tests under `reports/web/traces`.
- Pytest generates a self-contained HTML report at `reports/web/pytest_report.html`.
- Base page objects now expose test-id helper methods:
  - `by_test_id`
  - `visible_by_test_id`
  - `click_by_test_id`
  - `type_by_test_id`
- Pytest markers now include `smoke`, `regression`, `crud`, and `rbac`.

## Recommended App-Side Test IDs

When the LMS frontend can be updated, add stable attributes to critical controls.

```html
<input data-testid="login-email-input" />
<input data-testid="login-password-input" />
<button data-testid="login-submit-button">Login to Dashboard</button>
<a data-testid="sidebar-colleges-link">Colleges</a>
<button data-testid="college-add-button">ADD COLLEGE</button>
```

Then page objects can use:

```python
self.click_by_test_id("college-add-button")
```

## Useful Environment Variables

```bash
WEB_TEST_ID_ATTRIBUTE=data-testid
WEB_TRACE_MODE=retain-on-failure
WEB_RECORD_VIDEO=false
WEB_ARTIFACTS_DIR=reports/web
WEB_VIEWPORT_WIDTH=1440
WEB_VIEWPORT_HEIGHT=1000
```

## Suggested Runs

```bash
pytest -m web
pytest -m "web and smoke"
pytest -m "web and regression"
```

Phase 1 does not solve test data isolation. That belongs to Phase 2: API-backed test data setup and cleanup.
