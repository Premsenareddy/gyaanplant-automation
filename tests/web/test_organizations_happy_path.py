import pytest

from pages.web.organizations_page import OrganizationsPage


@pytest.fixture
def organizations_page(authenticated_web_page):
    organizations = OrganizationsPage(authenticated_web_page)
    organizations.load()
    organizations.wait_for_dashboard()
    organizations.navigate_to()
    return organizations


@pytest.mark.web
def test_gp_org_001_organizations_page_loads_with_table_and_filters(organizations_page):
    organizations_page.assert_organizations_page_loaded()
    organizations_page.assert_filter_controls_ready()
    organizations_page.assert_table_structure_ready()


@pytest.mark.web
def test_gp_org_002_organizations_table_displays_expected_partner(organizations_page):
    organizations_page.assert_expected_company_rows_visible()


@pytest.mark.web
def test_gp_org_003_search_finds_microsoft_partner(organizations_page):
    organizations_page.assert_search_result_contains(
        "Microsoft",
        ["Microsoft", "microsoft@mailinator.com", "IT", "MNC"],
    )


@pytest.mark.web
def test_gp_org_004_add_company_modal_opens_with_required_fields(organizations_page):
    organizations_page.assert_add_company_form_ready()
    organizations_page.assert_organizations_page_loaded()


@pytest.mark.web
def test_gp_org_005_existing_organization_row_has_action_controls(organizations_page):
    organizations_page.assert_row_actions_available("Microsoft")
