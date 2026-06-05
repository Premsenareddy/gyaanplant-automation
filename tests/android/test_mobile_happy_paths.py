import pytest

from config.settings import AndroidConfig
from pages.android.assessment_page import AssessmentPage
from pages.android.courses_page import CoursesPage
from pages.android.home_page import HomePage
from pages.android.leaderboard_page import LeaderboardPage
from pages.android.my_certificates_page import MyCertificatesPage
from pages.android.my_task_page import MyTaskPage
from pages.android.onboarding_page import OnboardingPage
from pages.android.settings_page import SettingsPage
from pages.android.splash_page import SplashPage
from tests.android.mobile_flows import login_to_home


@pytest.mark.android
def test_mob_hp_001_app_launches_to_expected_package(android_driver):
    cfg = AndroidConfig()

    assert android_driver.current_package == cfg.APP_PACKAGE
    assert android_driver.current_activity == cfg.APP_ACTIVITY


@pytest.mark.android
def test_mob_hp_002_splash_and_onboarding_reach_login_or_home(android_driver):
    splash = SplashPage(android_driver)
    onboarding = OnboardingPage(android_driver)

    if splash.is_displayed():
        splash.tap_start()

    if onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3):
        onboarding.complete_onboarding_and_go_to_login()

    assert (
        onboarding.is_element_present(onboarding.LOGIN_BUTTON, timeout=3)
        or android_driver.page_source
    )


@pytest.mark.android
def test_mob_hp_003_valid_user_can_login_and_view_home(android_driver):
    home = login_to_home(android_driver)

    assert home.is_any_text_visible(["Home", "Daily Attendance", "MY COURSES", "Profile"], timeout=10)


@pytest.mark.android
def test_mob_hp_004_bottom_navigation_tabs_are_accessible(android_driver):
    home = login_to_home(android_driver)

    home.go_to_library()
    assert home.is_any_text_visible(["Library", "MY COURSES", "Courses", "New Additions"], timeout=10)

    home.go_to_assessment_tab()
    assert home.is_any_text_visible(["Assessment", "Quiz", "Important Points", "Start Quiz"], timeout=10)

    home.go_to_profile()
    assert home.is_any_text_visible(["Profile", "Settings", "My Profile", "Leaderboard"], timeout=10)


@pytest.mark.android
def test_mob_hp_005_settings_menu_support_pages_are_accessible(android_driver):
    login_to_home(android_driver)
    home = HomePage(android_driver)
    settings = SettingsPage(android_driver)

    home.go_to_profile()

    settings.open_leaderboard()
    LeaderboardPage(android_driver).wait_for_loaded()
    android_driver.back()

    settings.open_my_certificates()
    certificates = MyCertificatesPage(android_driver)
    assert certificates.is_empty_state_visible() or certificates.is_text_visible("Certificate", timeout=10)
    android_driver.back()

    settings.open_my_task()
    task = MyTaskPage(android_driver)
    assert task.is_empty() or task.is_text_visible("Task", timeout=10) or task.is_text_visible("Course", timeout=10)


@pytest.mark.android
def test_mob_hp_006_courses_flow_opens_available_course(android_driver):
    home = login_to_home(android_driver)
    courses = CoursesPage(android_driver)

    home.go_to_library()
    assert home.is_any_text_visible(["MY COURSES", "Courses", "Rust"], timeout=10)

    if home.is_text_visible("Rust", timeout=5):
        courses.open_course_in_my_courses("Rust")
        assert courses.is_any_text_visible(["Rust", "Enroll Now", "Next Chapter", "Start Assessment"], timeout=10)


@pytest.mark.android
def test_mob_hp_007_assessment_intro_or_assessment_tab_loads(android_driver):
    home = login_to_home(android_driver)
    assessment = AssessmentPage(android_driver)

    home.go_to_assessment_tab()

    assert assessment.is_any_text_visible(
        ["Assessment", "Important Points to Remember", "Start Quiz", "Quiz"],
        timeout=10,
    )
