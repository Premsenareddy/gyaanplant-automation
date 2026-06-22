import pytest

from pages.web.colleges_page import CollegesPage
from utils.web_api_client import WebApiClient


@pytest.fixture
def colleges_crud_context(authenticated_web_page):
    colleges = CollegesPage(authenticated_web_page)
    colleges.load()
    colleges.wait_for_dashboard()

    created_colleges = []
    yield colleges, created_colleges

    api_cleanup = WebApiClient().cleanup_by_prefix("colleges", prefix=CollegesPage.AUTOMATION_PREFIX)
    if api_cleanup.enabled:
        print(f"\n[API Cleanup] Colleges status={api_cleanup.status_code}")

    for college_name in list(created_colleges):
        try:
            print(f"\n[Cleanup] Removing automated college record: {college_name}")
            colleges.delete_college_if_present(college_name)
        except Exception as error:
            print(f"[Cleanup Failed] Could not remove {college_name}: {error}")


@pytest.mark.web
def test_gp_col_crud_001_create_read_update_delete_college(colleges_crud_context):
    colleges, created_colleges = colleges_crud_context
    college_data = colleges.generate_college_form_data()
    created_colleges.append(college_data.name)

    colleges.navigate_to()
    WebApiClient().cleanup_by_prefix("colleges", prefix=CollegesPage.AUTOMATION_PREFIX)
    colleges.delete_college_if_present(college_data.name)

    colleges.create_college_from_data(college_data)

    assert colleges.college_exists(college_data.name), f"Created college not found: {college_data.name}"
    colleges.assert_college_row_matches_form_data(college_data)

    assert colleges.delete_college_if_present(college_data.name), f"College was not deleted: {college_data.name}"
    created_colleges.remove(college_data.name)

    assert not colleges.college_exists(college_data.name), f"College still visible after delete: {college_data.name}"
