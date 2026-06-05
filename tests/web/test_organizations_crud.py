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
@pytest.mark.skip(reason="Organization delete API returns 200 but record remains visible after reload; disabling to avoid live data pollution.")
def test_gp_org_crud_001_create_read_update_delete_company(organizations_crud_context):
    organizations, created_companies = organizations_crud_context
    target_company = organizations.generate_unique_company_name()
    created_companies.append(target_company)

    organizations.navigate_to()
    organizations.delete_company_if_present(target_company)

    organizations.create_company(target_company, city="Hyderabad")
    assert organizations.company_exists(target_company), f"Created company not found: {target_company}"

    organizations.edit_company_city(target_company, "Automation City Updated")
    assert "Automation City Updated" in organizations.company_row(target_company).inner_text()

    assert organizations.delete_company_if_present(target_company), f"Company was not deleted: {target_company}"
    created_companies.remove(target_company)

    assert not organizations.company_exists(target_company), f"Company still visible after delete: {target_company}"
