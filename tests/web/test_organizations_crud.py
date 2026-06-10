import os

import pytest

from pages.web.organizations_page import OrganizationsPage


@pytest.fixture
def organizations_crud_context(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run Organizations CRUD tests.")

    organizations = OrganizationsPage(web_page)
    organizations.load()
    organizations.login(email, password)
    organizations.wait_until_url_contains("/dashboard", timeout=60)

    created_companies = []
    yield organizations, created_companies

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
    organizations.delete_company_if_present(company_data.name)

    organizations.create_company_from_data(company_data)
    assert organizations.company_exists(company_data.name), f"Created company not found: {company_data.name}"
    organizations.assert_company_row_matches_form_data(company_data)

    assert organizations.delete_company_if_present(company_data.name), f"Company was not deleted: {company_data.name}"
    created_companies.remove(company_data.name)
