import pytest

from pages.web.dashboard_page import DashboardPage


@pytest.fixture
def admin_dashboard(authenticated_web_page):
    dashboard = DashboardPage(authenticated_web_page)
    dashboard.load()
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


@pytest.mark.web
def test_gp_adm_dash_009_summary_cards_have_numeric_values(admin_dashboard):
    admin_dashboard.assert_all_summary_cards_have_values()


@pytest.mark.web
def test_gp_adm_dash_010_top_partner_table_has_expected_structure(admin_dashboard):
    admin_dashboard.assert_top_partner_table_structure()


@pytest.mark.web
def test_gp_adm_dash_011_leaderboard_widget_has_expected_structure(admin_dashboard):
    admin_dashboard.assert_leaderboard_widget_structure()


@pytest.mark.web
def test_gp_adm_dash_012_header_profile_notifications_and_theme_are_operable(admin_dashboard):
    admin_dashboard.assert_profile_dropdown_opens()
    admin_dashboard.go_to_dashboard_home()

    admin_dashboard.assert_notifications_panel_opens()
    admin_dashboard.go_to_dashboard_home()

    admin_dashboard.toggle_theme_and_assert_changed()


@pytest.mark.web
@pytest.mark.parametrize("label,expected_path", DashboardPage.SIDEBAR_ROUTE_EXPECTATIONS.items())
def test_gp_adm_dash_013_sidebar_items_route_to_expected_pages(admin_dashboard, label, expected_path):
    admin_dashboard.go_to_dashboard_home()
    actual_path = admin_dashboard.navigate_sidebar_item(label)
    assert actual_path == expected_path
    assert expected_path in admin_dashboard.page.url


@pytest.mark.web
def test_gp_adm_dash_014_non_navigating_sidebar_items_are_visible(admin_dashboard):
    admin_dashboard.go_to_dashboard_home()
    for label in DashboardPage.SIDEBAR_NON_NAVIGATING_ITEMS:
        assert admin_dashboard.sidebar_item(label).is_visible()


@pytest.mark.web
def test_gp_adm_dash_015_admin_can_logout_from_dashboard(admin_dashboard):
    admin_dashboard.logout()
    assert admin_dashboard.is_on_login_route() or "STUDENT" in admin_dashboard.body_text()
