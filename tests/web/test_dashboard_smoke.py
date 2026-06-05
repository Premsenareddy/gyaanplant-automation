import os

import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.mark.web
def test_dashboard_route_requires_authentication(web_page):
    dashboard = DashboardPage(web_page)

    dashboard.load()

    assert dashboard.has_rendered_app_shell()
    assert "GyaanPlant" in web_page.title()
    assert dashboard.is_on_login_route() or dashboard.has_login_form()


@pytest.mark.web
def test_login_page_is_ready_for_credentials(web_page):
    dashboard = DashboardPage(web_page)

    dashboard.load()

    assert dashboard.has_login_form()


@pytest.mark.web
def test_dashboard_login_with_credentials(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run authenticated dashboard checks.")

    dashboard = DashboardPage(web_page)
    dashboard.load()
    dashboard.login(email, password)

    dashboard.wait_until_url_contains("/dashboard")
    assert dashboard.has_rendered_app_shell()
