import os
import sys
import time
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_android_driver
from pages.android.login_page import LoginPage
from pages.android.onboarding_page import OnboardingPage
from pages.android.splash_page import SplashPage


EMAIL = os.getenv("ANDROID_LMS_EMAIL", "auto.mobile.active.bits.1780551494@mailinator.com")
PASSWORD = os.getenv("ANDROID_LMS_PASSWORD", "12345678")


def count_text(driver, text):
    locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    return sum(len(driver.find_elements(*locator)) for locator in locators)


def main():
    driver = create_android_driver()
    try:
        splash = SplashPage(driver)
        onboarding = OnboardingPage(driver)
        login = LoginPage(driver)

        if splash.is_displayed():
            splash.tap_start()

        if (
            onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3)
            or onboarding.is_element_present(onboarding.LOGIN_BUTTON, timeout=3)
        ):
            onboarding.complete_onboarding_and_go_to_login()

        login.enter_email(EMAIL)
        login.submit_email()

        if login.is_password_screen_displayed(timeout=15):
            login.enter_password(PASSWORD)
            login.hide_keyboard()
            time.sleep(0.5)
            driver.save_screenshot("screenshots/manual_continue_password_filled.png")
            print("READY_FOR_MANUAL_CONTINUE|password_filled", flush=True)
            print(
                f"MARKERS|Enter Password={count_text(driver, 'Enter Password')}|Continue={count_text(driver, 'Continue')}",
                flush=True,
            )
            while True:
                time.sleep(30)

        if login.is_otp_screen_displayed(timeout=3):
            driver.save_screenshot("screenshots/manual_continue_otp_screen.png")
            print("OTP_SCREEN_VISIBLE|password_not_filled", flush=True)
            while True:
                time.sleep(30)

        driver.save_screenshot("screenshots/manual_continue_unknown_state.png")
        print("UNKNOWN_STATE", flush=True)
        while True:
            time.sleep(30)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
