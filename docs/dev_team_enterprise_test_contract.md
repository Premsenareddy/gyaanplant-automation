# Dev Team Contract for Enterprise Regression

This automation framework is ready for stronger enterprise coverage when the LMS app and backend expose stable test hooks and test-data APIs.

## Required GitHub Secrets

Base authenticated CI:

- `LMS_BASE_URL`
- `LMS_EMAIL`
- `LMS_PASSWORD`

RBAC:

- `LMS_ADMIN_EMAIL`
- `LMS_ADMIN_PASSWORD`
- `LMS_COLLEGE_ADMIN_EMAIL`
- `LMS_COLLEGE_ADMIN_PASSWORD`
- `LMS_STUDENT_EMAIL`
- `LMS_STUDENT_PASSWORD`
- `LMS_STUDENT_SECONDARY_EMAIL`
- `LMS_STUDENT_SECONDARY_PASSWORD`
- `LMS_TPO_EMAIL`
- `LMS_TPO_PASSWORD`
- `LMS_HOD_EMAIL`
- `LMS_HOD_PASSWORD`
- `LMS_MENTOR_EMAIL`
- `LMS_MENTOR_PASSWORD`

API-backed cleanup:

- `LMS_API_BASE_URL`
- `LMS_API_TOKEN`

## API Cleanup Contract

Preferred endpoints:

```text
DELETE /automation/cleanup/colleges?prefix=AUTO_TEST_COLLEGE_
DELETE /automation/cleanup/organizations?prefix=AUTO_TEST_COMPANY_
DELETE /automation/cleanup/courses?prefix=AUTO_TEST_COURSE_
DELETE /automation/cleanup/users?prefix=AUTO_TEST_USER_
DELETE /automation/cleanup/career-paths?prefix=AUTO_TEST_PATH_
DELETE /automation/cleanup/prep-packs?prefix=AUTO_TEST_PACK_
POST   /automation/seed
```

The current client is implemented in `utils/web_api_client.py` and is inert until `LMS_API_BASE_URL` and `LMS_API_TOKEN` are configured.

## Selector Contract

Add stable `data-testid` attributes for:

- login role cards
- email/password/login controls
- sidebar navigation links
- search inputs and filters
- table rows and cells
- card containers and action buttons
- modal fields
- save/update/delete/confirm buttons
- toast messages
- profile/logout controls

Examples:

```html
<input data-testid="login-email-input" />
<button data-testid="login-submit-button">Login to Dashboard</button>
<a data-testid="sidebar-colleges-link">Colleges</a>
<tr data-testid="college-row-BITS">...</tr>
<button data-testid="college-delete-button">Delete</button>
```

## Mocked Resilience Contract

Set `WEB_MOCK_API_PATTERN` once API routes are confirmed, for example:

```bash
WEB_MOCK_API_PATTERN="**/api/**"
```

Then run:

```bash
pytest -m "web and mocked"
```

## CRUD Readiness

Full CRUD can be enabled safely for Courses, Users, Career Paths, Prep Packs, Notifications, and Settings only after one of these exists:

- reliable UI delete/cleanup action
- API cleanup endpoint
- database cleanup job for automation-owned records

Automation-owned records should use the `AUTO_TEST_` or `AUTO_WEB_` prefix.
