import os

import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.fixture
def admin_dashboard(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run admin dashboard tests.")

    dashboard = DashboardPage(web_page)
    dashboard.load()
    dashboard.login(email, password)
    dashboard.wait_for_dashboard()
    return dashboard


@pytest.mark.web
def test_gp_adm_dash_001_sidebar_navigation_modules_are_available(admin_dashboard):
    admin_dashboard.visible_texts(DashboardPage.NAVIGATION_ITEMS)


@pytest.mark.web
def test_gp_adm_dash_002_top_metric_cards_show_expected_values(admin_dashboard):
    admin_dashboard.assert_metrics_match_dashboard_values()


@pytest.mark.web
def test_gp_adm_dash_003_platform_activity_cards_show_expected_values(admin_dashboard):
    admin_dashboard.assert_activity_summaries_match_dashboard_values()


@pytest.mark.web
def test_gp_adm_dash_004_top_partner_table_shows_microsoft_active(admin_dashboard):
    admin_dashboard.assert_top_partner_company_matches_dashboard_values()


@pytest.mark.web
def test_gp_adm_dash_005_leaderboard_shows_top_five_students(admin_dashboard):
    admin_dashboard.assert_leaderboard_matches_dashboard_values()
