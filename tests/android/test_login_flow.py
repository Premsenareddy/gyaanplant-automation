# tests/android/test_login_flow.py

import pytest
from pages.android.splash_page import SplashPage
from pages.android.onboarding_page import OnboardingPage
from pages.android.login_page import LoginPage


@pytest.mark.android
def test_login_navigation_flow(android_driver):
    splash = SplashPage(android_driver)
    onboarding = OnboardingPage(android_driver)
    login = LoginPage(android_driver)

    # 1. Splash → Start
    assert splash.is_displayed()
    splash.tap_start()

    # 2. Onboarding screens → Login
    onboarding.complete_onboarding_and_go_to_login()

    # 3. Email screen
    assert login.is_email_screen_displayed()
    login.enter_email("maxy1@gmail.com")
    login.submit_email()

    # --------------------------------
    # 4. OTP screen disabled for now
    # --------------------------------
    # if login.is_otp_screen_displayed():
    #     login.enter_otp("1234")
    #     login.submit_otp()

    # 5. Password screen
    assert login.is_password_screen_displayed()
    login.enter_password("1234")
    login.submit_password()

    # TODO: Add assertions for Home/Profile after login

