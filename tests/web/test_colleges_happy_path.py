import os

import pytest

from pages.web.colleges_page import CollegesPage


@pytest.fixture
def colleges_page(web_page):
    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to run Colleges tests.")

    colleges = CollegesPage(web_page)
    colleges.load()
    colleges.login(email, password)
    colleges.wait_for_dashboard()
    colleges.open_colleges()
    return colleges


@pytest.mark.web
def test_gp_col_001_colleges_page_loads_with_table_and_filters(colleges_page):
    colleges_page.assert_colleges_page_loaded()
    colleges_page.visible_texts(["All", "Active", "Pending", "Renewal", "Expired"])
    colleges_page.visible_texts(["All Types", "Engineering", "Management", "Science"])


@pytest.mark.web
def test_gp_col_002_colleges_table_displays_expected_institutions(colleges_page):
    colleges_page.assert_expected_college_rows_visible()


@pytest.mark.web
def test_gp_col_003_search_finds_bits_college(colleges_page):
    colleges_page.search_college("BITS")

    row_text = colleges_page.college_row("BITS").inner_text()
    assert "BITS" in row_text
    assert "bits@mailinator.com" in row_text


@pytest.mark.web
def test_gp_col_004_city_filter_keeps_hyderabad_colleges_visible(colleges_page):
    colleges_page.filter_city("Hyderabad")

    colleges_page.visible_texts(["CMR", "MVSR", "Hyderabad"])


@pytest.mark.web
def test_gp_col_005_add_college_modal_opens_with_required_fields(colleges_page):
    colleges_page.open_add_college_modal()
    colleges_page.assert_add_college_form_ready()
    colleges_page.close_add_college_modal()
    colleges_page.assert_colleges_page_loaded()
