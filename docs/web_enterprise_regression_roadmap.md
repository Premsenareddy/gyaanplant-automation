# Web Enterprise Regression Roadmap

This repo is now focused on GyaanPlant web automation only.

## Current Foundation

- Python, Pytest, and Playwright.
- Page Object Model under `pages/web`.
- Failure screenshots and Playwright traces.
- HTML reporting.
- Strict marker registration.
- Automatic marker assignment for web, smoke, regression, CRUD, RBAC, and live tests.
- Live CRUD tests are guarded behind `--run-live-crud`.
- Shared web automation test data naming through `utils/web_test_data.py`.

## Suite Layers

| Layer | Purpose | Command |
| --- | --- | --- |
| Smoke | Fast critical UI checks | `pytest -m "web and smoke"` |
| Regression | Broader non-mutating release coverage | `pytest -m "web and regression"` |
| RBAC | Role login/access coverage | `pytest -m "web and rbac"` |
| CRUD | Mutating data lifecycle checks | `pytest -m "web and crud" --run-live-crud` |

## Remaining Enterprise Work

### Phase 1: Selector Stabilization

Status: framework-ready, app-source pending.

The framework supports `data-testid` through `WEB_TEST_ID_ATTRIBUTE`. The LMS frontend should expose stable test IDs for:

- login controls
- sidebar navigation
- tables and rows
- modal fields
- save/update/delete buttons
- toast messages
- role-specific landing pages

### Phase 2: Test Data Control

Status: started in the framework, backend/API work pending.

Needed:

- API client for setup and cleanup.
- Dedicated automation records.
- Cleanup by `AUTO_WEB` prefix.
- Test users per role.
- Data contracts for Colleges, Organizations, Courses, Users, Career Paths, and Prep Packs.

### Phase 3: Full CRUD Regression

Status: guarded.

CRUD tests should stay disabled by default until cleanup is reliable. Once backend cleanup exists, enable:

- Create
- Read/search/filter
- Update
- Delete
- Verify deletion after reload

### Phase 4: Role-Based Access

Status: basic role login coverage exists.

Needed:

- Expected landing page per role.
- Allowed modules per role.
- Forbidden module assertions.
- Session isolation between roles.

### Phase 5: CI/CD

Recommended GitHub Actions stages:

- Pull request: smoke only.
- Nightly: regression + RBAC.
- Release candidate: full regression + approved CRUD.

### Phase 6: Assertion Maturity

Replace broad body-text checks with component assertions:

- table cell values
- card metric values
- modal field state
- selected filters
- URLs and navigation state
- toast success/error messages
