import os

import pytest

from pages.web.courses_page import CoursesPage


@pytest.fixture
def courses_page(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run Courses tests.")

    courses = CoursesPage(web_page)
    courses.load()
    courses.login(email, password)
    courses.wait_until_url_contains("/dashboard", timeout=60)
    courses.navigate_to()
    return courses


@pytest.mark.web
def test_gp_course_001_courses_page_loads_existing_course_card(courses_page):
    courses_page.assert_courses_page_loaded()
    courses_page.assert_expected_courses_visible()
    courses_page.assert_search_controls_ready()
    courses_page.assert_course_actions_available()


@pytest.mark.web
def test_gp_course_002_search_finds_nodejs_course(courses_page):
    courses_page.assert_course_card_contains(
        "Node.js Backend Development",
        ["Node.js Backend Development", "BEGINNER", "VIEW CONTENT"],
    )


@pytest.mark.web
def test_gp_course_003_add_course_modal_opens_with_required_fields(courses_page):
    courses_page.assert_add_course_form_ready()
    courses_page.assert_courses_page_loaded()


@pytest.mark.web
def test_gp_course_004_course_page_keeps_actions_after_search(courses_page):
    courses_page.search_course("Node.js Backend Development")
    courses_page.assert_course_actions_available()
