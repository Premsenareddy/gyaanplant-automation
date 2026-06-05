import os

import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.fixture
def dashboard_for_smoke_click(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run dashboard smoke-click tests.")

    dashboard = DashboardPage(web_page)
    dashboard.load()
    dashboard.login(email, password)
    dashboard.wait_for_dashboard()
    return dashboard


def _settle_dashboard_app(page):
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.locator("body").wait_for(state="visible")


def _record_soft_failure(failures, target_name, error):
    failures.append(f"{target_name}: {error}")


@pytest.mark.web
def test_gp_adm_dash_006_sidebar_navigation_smoke_clicks(dashboard_for_smoke_click):
    dashboard = dashboard_for_smoke_click
    page = dashboard.page
    failures = []

    for item_text in DashboardPage.SMOKE_CLICK_SIDEBAR_ITEMS:
        try:
            dashboard.go_to_dashboard_home()
            before_url = page.url

            # Re-locate by text inside the loop. This avoids stale/detached handles after SPA rerenders.
            sidebar_item = dashboard.sidebar_item(item_text)
            sidebar_item.scroll_into_view_if_needed()
            sidebar_item.click()
            _settle_dashboard_app(page)

            assert page.url != before_url or item_text in dashboard.body_text()
            assert "GyaanPlant" in page.title()
            assert page.locator("body").inner_text().strip()
        except Exception as error:
            _record_soft_failure(failures, item_text, error)

    dashboard.go_to_dashboard_home()
    assert not failures, "Smoke-click sidebar failures:\n" + "\n".join(failures)


@pytest.mark.web
def test_gp_adm_dash_007_leaderboard_filter_smoke_clicks(dashboard_for_smoke_click):
    dashboard = dashboard_for_smoke_click
    page = dashboard.page
    failures = []

    for filter_text in DashboardPage.SMOKE_CLICK_LEADERBOARD_FILTERS:
        try:
            dashboard.go_to_dashboard_home()

            # Re-fetch the filter button each loop because leaderboard content may rerender after a click.
            dashboard.leaderboard_filter(filter_text).click()
            _settle_dashboard_app(page)

            assert dashboard.leaderboard_filter(filter_text).is_visible()
            assert "Leaderboard" in dashboard.body_text()
            assert page.url.endswith("/dashboard")
        except Exception as error:
            _record_soft_failure(failures, filter_text, error)

    dashboard.go_to_dashboard_home()
    assert not failures, "Smoke-click leaderboard filter failures:\n" + "\n".join(failures)


@pytest.mark.web
def test_gp_adm_dash_008_header_actions_smoke_click(dashboard_for_smoke_click):
    dashboard = dashboard_for_smoke_click
    page = dashboard.page
    failures = []

    header_actions = [
        ("Theme Toggle", lambda: dashboard.theme_toggle_button),
        ("Notifications", lambda: dashboard.notifications_button),
        ("Profile dropdown", lambda: dashboard.profile_dropdown_button),
    ]

    for action_name, locator_factory in header_actions:
        try:
            dashboard.go_to_dashboard_home()

            # Create a fresh locator for every click. Header actions can update global app state.
            locator_factory().click()
            _settle_dashboard_app(page)

            assert page.locator("body").inner_text().strip()
            assert "GyaanPlant" in page.title()
        except Exception as error:
            _record_soft_failure(failures, action_name, error)

    dashboard.go_to_dashboard_home()
    assert not failures, "Smoke-click header action failures:\n" + "\n".join(failures)
