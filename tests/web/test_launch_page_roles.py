import pytest

from pages.web.launch_page import LaunchPage


ROLE_CREDENTIALS = [
    ("Admin", "ADMIN", "admin@gyaanplant.com", "12345678"),
    ("College Admin", "COLLEGE", "sagar@mailinator.com", "12345678"),
    ("Student Avinash", "STUDENT", "avinash@mailinator.com", "12345678"),
    ("Student Ishu", "STUDENT", "ishu@mailinator.com", "12345678"),
    ("TPO", "TPO", "sagartpo@mailinator.com", "12345678"),
    ("HOD", "HOD", "sagarhod@mailinator.com", "12345678"),
    ("Mentor", "MENTOR", "sagarmentor@mailinator.com", "12345678"),
]


@pytest.mark.web
def test_gp_launch_001_launch_page_displays_role_cards(web_page):
    launch = LaunchPage(web_page)

    launch.load()

    assert launch.has_role_cards()
    assert "Welcome" in launch.body_text()


@pytest.mark.web
@pytest.mark.parametrize("role_name,role_label,email,password", ROLE_CREDENTIALS)
def test_gp_launch_002_each_role_can_login(role_name, role_label, email, password, web_page):
    launch = LaunchPage(web_page)

    launch.load()
    launch.login_as_role(role_label, email, password)
    web_page.wait_for_load_state("networkidle")
    launch.present("body")

    body_text = launch.body_text()
    assert "LOGGING IN AS" not in body_text, f"{role_name} stayed on login form"
    assert email.split("@")[0].lower() in body_text.lower() or "/login" not in web_page.url
    assert body_text.strip(), f"{role_name} landed on an empty page"
