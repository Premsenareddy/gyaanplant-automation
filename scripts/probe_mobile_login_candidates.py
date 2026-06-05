import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_android_driver
from pages.android.home_page import HomePage
from pages.android.login_page import LoginPage, MobileAuthenticationBlocked
from pages.android.onboarding_page import OnboardingPage
from pages.android.splash_page import SplashPage


def reach_login(driver):
    splash = SplashPage(driver)
    onboarding = OnboardingPage(driver)

    if splash.is_displayed():
        splash.tap_start()

    if onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3) or onboarding.is_element_present(
        onboarding.LOGIN_BUTTON, timeout=3
    ):
        onboarding.complete_onboarding_and_go_to_login()


def probe(email, password, otp):
    driver = create_android_driver()
    try:
        reach_login(driver)
        login = LoginPage(driver)
        home = HomePage(driver)

        if not login.is_email_screen_displayed():
            print(f"RESULT|{email}|{password}|{otp}|NO_EMAIL_SCREEN|{driver.current_activity}")
            return

        try:
            login.login(email, password, otp=otp)
        except MobileAuthenticationBlocked as exc:
            driver.save_screenshot(f"screenshots/mobile_probe_{email.replace('@', '_at_')}_{password}.png")
            print(f"RESULT|{email}|{password}|{otp}|AUTH_BLOCKED|{exc}")
            return

        if home.is_any_text_visible(["Home", "Daily Attendance", "MY COURSES", "Profile"], timeout=20):
            driver.save_screenshot(f"screenshots/mobile_probe_success_{email.replace('@', '_at_')}_{password}.png")
            print(f"RESULT|{email}|{password}|{otp}|HOME_REACHED|{driver.current_activity}")
        else:
            driver.save_screenshot(f"screenshots/mobile_probe_no_home_{email.replace('@', '_at_')}_{password}.png")
            print(f"RESULT|{email}|{password}|{otp}|NO_HOME|{driver.current_activity}")
    finally:
        driver.quit()


def main():
    users = [value for value in os.environ["MOBILE_PROBE_EMAILS"].split(",") if value]
    passwords = [value for value in os.environ.get("MOBILE_PROBE_PASSWORDS", "1234,123456,12345678,Auto@12345").split(",") if value]
    otp = os.environ.get("MOBILE_PROBE_OTP", "1234")

    for email in users:
        for password in passwords:
            probe(email.strip(), password.strip(), otp)


if __name__ == "__main__":
    main()
