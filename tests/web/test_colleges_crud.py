import os

import pytest

from pages.web.colleges_page import CollegesPage


@pytest.fixture
def colleges_crud_context(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run Colleges CRUD tests.")

    colleges = CollegesPage(web_page)
    colleges.load()
    colleges.login(email, password)
    colleges.wait_for_dashboard()

    created_colleges = []
    yield colleges, created_colleges

    for college_name in list(created_colleges):
        try:
            print(f"\n[Cleanup] Removing automated college record: {college_name}")
            colleges.delete_college_if_present(college_name)
        except Exception as error:
            print(f"[Cleanup Failed] Could not remove {college_name}: {error}")


@pytest.mark.web
@pytest.mark.skip(reason="College delete removes the college but leaves the generated college_admin user visible as inactive; CRUD creation disabled to avoid live user-list pollution.")
def test_gp_col_crud_001_create_read_update_delete_college(colleges_crud_context):
    colleges, created_colleges = colleges_crud_context
    target_college = colleges.generate_unique_college_name()
    created_colleges.append(target_college)

    colleges.navigate_to()
    colleges.delete_college_if_present(target_college)

    colleges.create_college(target_college, city="Hyderabad")

    assert colleges.college_exists(target_college), f"Created college not found: {target_college}"

    colleges.edit_college_city(target_college, "Automation City Updated")
    assert "Automation City Updated" in colleges.college_row(target_college).inner_text()

    assert colleges.delete_college_if_present(target_college), f"College was not deleted: {target_college}"
    created_colleges.remove(target_college)

    assert not colleges.college_exists(target_college), f"College still visible after delete: {target_college}"
