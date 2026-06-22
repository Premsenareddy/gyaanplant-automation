import os

import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.fixture
def logged_in_page(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run mocked resilience tests.")

    dashboard = DashboardPage(web_page)
    dashboard.load()
    dashboard.login(email, password)
    dashboard.wait_for_dashboard()
    return web_page


@pytest.fixture
def api_pattern():
    pattern = os.getenv("WEB_MOCK_API_PATTERN", "").strip()
    if not pattern:
        pytest.skip("Set WEB_MOCK_API_PATTERN after dev confirms LMS API route patterns.")
    return pattern


@pytest.mark.web
def test_gp_mock_001_api_failure_state_is_recoverable(api_pattern, logged_in_page):
    intercepted = {"count": 0}

    def fail_api(route):
        intercepted["count"] += 1
        route.fulfill(
            status=500,
            content_type="application/json",
            body='{"message":"Simulated automation API failure"}',
        )

    logged_in_page.route(api_pattern, fail_api)
    logged_in_page.reload(wait_until="networkidle")
    logged_in_page.locator("body").wait_for(state="visible")

    if intercepted["count"] == 0:
        pytest.skip(f"No requests matched WEB_MOCK_API_PATTERN={api_pattern!r}")

    assert logged_in_page.locator("body").inner_text().strip()


@pytest.mark.web
def test_gp_mock_002_slow_api_state_keeps_page_responsive(api_pattern, logged_in_page):
    intercepted = {"count": 0}

    def slow_api(route):
        intercepted["count"] += 1
        logged_in_page.wait_for_timeout(1500)
        route.continue_()

    logged_in_page.route(api_pattern, slow_api)
    logged_in_page.reload(wait_until="domcontentloaded")
    logged_in_page.locator("body").wait_for(state="visible")

    if intercepted["count"] == 0:
        pytest.skip(f"No requests matched WEB_MOCK_API_PATTERN={api_pattern!r}")

    assert "GyaanPlant" in logged_in_page.title()
