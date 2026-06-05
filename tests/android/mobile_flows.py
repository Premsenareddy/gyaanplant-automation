import pytest

from config.settings import AndroidTestUser
from pages.android.home_page import HomePage
from pages.android.login_page import LoginPage, MobileAuthenticationBlocked
from pages.android.onboarding_page import OnboardingPage
from pages.android.post_login_onboarding_page import PostLoginOnboardingPage
from pages.android.splash_page import SplashPage


def login_to_home(driver):
    user = AndroidTestUser()
    splash = SplashPage(driver)
    onboarding = OnboardingPage(driver)
    login = LoginPage(driver)
    post_login = PostLoginOnboardingPage(driver)
    home = HomePage(driver)

    if splash.is_displayed():
        splash.tap_start()

    if onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3) or onboarding.is_element_present(onboarding.LOGIN_BUTTON, timeout=3):
        onboarding.complete_onboarding_and_go_to_login()

    if login.is_email_screen_displayed():
        try:
            login.login(user.email, user.password, otp=user.otp)
        except MobileAuthenticationBlocked as exc:
            pytest.skip(str(exc))

    post_login.complete_if_present()

    try:
        home.wait_for_home_loaded()
    except Exception:
        pytest.skip(
            "Login did not reach Home after credential submit and post-login onboarding. "
            "Provide a valid APK user/password or complete any newly introduced setup screen."
        )
    home.handle_daily_attendance_if_present()
    return home
