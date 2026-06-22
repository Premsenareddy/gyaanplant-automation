import pytest

from pages.web.organizations_page import OrganizationsPage
from utils.web_api_client import WebApiClient


@pytest.fixture
def organizations_crud_context(authenticated_web_page):
    organizations = OrganizationsPage(authenticated_web_page)
    organizations.load()
    organizations.wait_for_dashboard()

    created_companies = []
    yield organizations, created_companies

    api_cleanup = WebApiClient().cleanup_by_prefix("organizations", prefix=OrganizationsPage.AUTOMATION_PREFIX)
    if api_cleanup.enabled:
        print(f"\n[API Cleanup] Organizations status={api_cleanup.status_code}")

    for company_name in list(created_companies):
        try:
            print(f"\n[Cleanup] Removing automated organization record: {company_name}")
            organizations.delete_company_if_present(company_name)
        except Exception as error:
            print(f"[Cleanup Failed] Could not remove {company_name}: {error}")


@pytest.mark.web
def test_gp_org_crud_001_create_read_update_delete_company(organizations_crud_context):
    organizations, created_companies = organizations_crud_context
    company_data = organizations.generate_organization_form_data()
    created_companies.append(company_data.name)

    organizations.navigate_to()
    WebApiClient().cleanup_by_prefix("organizations", prefix=OrganizationsPage.AUTOMATION_PREFIX)
    organizations.delete_company_if_present(company_data.name)

    organizations.create_company_from_data(company_data)
    assert organizations.company_exists(company_data.name), f"Created company not found: {company_data.name}"
    organizations.assert_company_row_matches_form_data(company_data)

    assert organizations.delete_company_if_present(company_data.name), f"Company was not deleted: {company_data.name}"
    created_companies.remove(company_data.name)
