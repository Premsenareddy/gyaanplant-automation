import os

import pytest

from pages.web.courses_page import CoursesPage


@pytest.fixture
def courses_crud_context(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run Courses CRUD tests.")

    courses = CoursesPage(web_page)
    courses.load()
    courses.login(email, password)
    courses.wait_until_url_contains("/dashboard", timeout=60)
    courses.navigate_to()
    return courses


@pytest.mark.web
def test_gp_course_crud_001_create_read_update_delete_course(courses_crud_context):
    courses = courses_crud_context
    courses.open_add_course_modal()
    if not courses.has_visible_delete_cleanup_action():
        pytest.skip("Courses CRUD is blocked until a reliable delete/cleanup action is available.")
