import os

import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.fixture
def logged_in_dashboard(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run authenticated dashboard checks.")

    dashboard = DashboardPage(web_page)
    dashboard.load()
    dashboard.login(email, password)
    dashboard.wait_for_dashboard()
    return dashboard


@pytest.mark.web
def test_dashboard_navigation_menu_displays_admin_modules(logged_in_dashboard):
    logged_in_dashboard.visible_texts(DashboardPage.NAVIGATION_ITEMS)


@pytest.mark.web
def test_dashboard_summary_cards_display_platform_metrics(logged_in_dashboard):
    logged_in_dashboard.visible_texts(DashboardPage.SUMMARY_CARDS)


@pytest.mark.web
def test_dashboard_displays_activity_and_partner_company_widgets(logged_in_dashboard):
    logged_in_dashboard.visible_texts(
        [
            "ACTIVITY SUMMARY",
            "POINTS",
            "ACTIONS",
            "Top Partner Companies",
            "COMPANY NAME",
            "INDUSTRY",
            "STATUS",
        ]
    )


@pytest.mark.web
def test_dashboard_displays_leaderboard_widget(logged_in_dashboard):
    logged_in_dashboard.visible_texts(
        [
            "Leaderboard",
            "Top students across all colleges",
            "ALL TIME",
            "MONTHLY",
            "WEEKLY",
            "VIEW FULL LEADERBOARD",
        ]
    )
