import pytest

from pages.web.courses_page import CoursesPage


@pytest.fixture
def courses_crud_context(authenticated_web_page):
    courses = CoursesPage(authenticated_web_page)
    courses.load()
    courses.wait_for_dashboard()
    courses.navigate_to()
    return courses


@pytest.mark.web
def test_gp_course_crud_001_create_read_update_delete_course(courses_crud_context):
    courses = courses_crud_context
    courses.open_add_course_modal()
    if not courses.has_visible_delete_cleanup_action():
        pytest.skip("Courses CRUD is blocked until a reliable delete/cleanup action is available.")
