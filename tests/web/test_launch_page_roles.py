import os

import pytest

from pages.web.launch_page import LaunchPage


ROLE_CREDENTIALS = [
    ("Admin", "ADMIN", "LMS_ADMIN_EMAIL", "LMS_ADMIN_PASSWORD"),
    ("College Admin", "COLLEGE", "LMS_COLLEGE_ADMIN_EMAIL", "LMS_COLLEGE_ADMIN_PASSWORD"),
    ("Student Primary", "STUDENT", "LMS_STUDENT_EMAIL", "LMS_STUDENT_PASSWORD"),
    ("Student Secondary", "STUDENT", "LMS_STUDENT_SECONDARY_EMAIL", "LMS_STUDENT_SECONDARY_PASSWORD"),
    ("TPO", "TPO", "LMS_TPO_EMAIL", "LMS_TPO_PASSWORD"),
    ("HOD", "HOD", "LMS_HOD_EMAIL", "LMS_HOD_PASSWORD"),
    ("Mentor", "MENTOR", "LMS_MENTOR_EMAIL", "LMS_MENTOR_PASSWORD"),
]


def _credential_from_env(email_var: str, password_var: str) -> tuple[str, str]:
    email = os.getenv(email_var, "").strip()
    password = os.getenv(password_var, "").strip()
    if not email or not password:
        pytest.skip(f"Missing role credentials: {email_var}/{password_var}")
    return email, password


@pytest.mark.web
def test_gp_launch_001_launch_page_displays_role_cards(web_page):
    launch = LaunchPage(web_page)

    launch.load()

    assert launch.has_role_cards()
    assert "Welcome" in launch.body_text()


@pytest.mark.web
@pytest.mark.parametrize("role_name,role_label,email_var,password_var", ROLE_CREDENTIALS)
def test_gp_launch_002_each_role_can_login(role_name, role_label, email_var, password_var, web_page):
    launch = LaunchPage(web_page)
    email, password = _credential_from_env(email_var, password_var)

    launch.load()
    launch.login_as_role(role_label, email, password)
    web_page.wait_for_load_state("networkidle")
    launch.present("body")

    body_text = launch.body_text()
    assert "LOGGING IN AS" not in body_text, f"{role_name} stayed on login form"
    assert email.split("@")[0].lower() in body_text.lower() or "/login" not in web_page.url
    assert body_text.strip(), f"{role_name} landed on an empty page"
