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


EMAIL = os.getenv("ANDROID_LMS_EMAIL", "arjun@mailinator.com")
PASSWORD = os.getenv("ANDROID_LMS_PASSWORD", "12345678")
OTP = os.getenv("ANDROID_LMS_OTP", "1234")


def count_text(driver, text):
    locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    return sum(len(driver.find_elements(*locator)) for locator in locators)


def tap_first_text(driver, text):
    locators = [
        (AppiumBy.ACCESSIBILITY_ID, text),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    for locator in locators:
        elements = driver.find_elements(*locator)
        if elements:
            elements[0].click()
            time.sleep(2)
            return True
    return False


def wait_for_any(driver, texts, timeout=25):
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = {text: count_text(driver, text) for text in texts}
        if any(current.values()):
            return current
        time.sleep(1)
    return {text: count_text(driver, text) for text in texts}


def snapshot(driver, label):
    path = f"screenshots/{label}.png"
    driver.save_screenshot(path)
    print(f"SCREENSHOT|{label}|{path}", flush=True)
    print(f"MARKERS|{label}|{wait_for_any(driver, ['Enter OTP', 'Enter Password', 'Roles Selection', 'Student', 'Learning Goals', 'Home', 'Incorrect password'], timeout=1)}", flush=True)


def submit_email_until_auth_branch(driver, login, max_attempts=3):
    login.submit_email()
    for attempt in range(1, max_attempts + 1):
        branch = wait_for_any(driver, ["Enter OTP", "Enter Password"], timeout=10)
        print(f"AUTH_BRANCH_ATTEMPT|{attempt}|{branch}", flush=True)
        if branch["Enter OTP"] or branch["Enter Password"]:
            return branch

        if count_text(driver, "Enter your email and proceed") or count_text(driver, "Submit"):
            print(f"ACTION|retry_email_submit|{attempt}", flush=True)
            tap_first_text(driver, "Submit")

    return wait_for_any(driver, ["Enter OTP", "Enter Password"], timeout=2)


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
        branch = submit_email_until_auth_branch(driver, login)
        print(f"AUTH_BRANCH|{branch}", flush=True)

        if count_text(driver, "Enter OTP"):
            login.enter_otp(OTP)
            login.submit_otp()
        elif count_text(driver, "Enter Password"):
            login.enter_password(PASSWORD)
            login.submit_password()
        else:
            snapshot(driver, "arjun_unknown_auth_branch")
            print("PAUSED|Unknown auth branch. Keeping session open for inspection.", flush=True)
            while True:
                time.sleep(30)
            return

        auth_result = wait_for_any(
            driver,
            ["Roles Selection", "Student", "Learning Goals", "Home", "Incorrect password"],
            timeout=25,
        )
        print(f"AUTH_RESULT|{auth_result}", flush=True)

        if count_text(driver, "Incorrect password"):
            snapshot(driver, "arjun_password_failed_pause_probe")
            return

        if count_text(driver, "Roles Selection") or count_text(driver, "Student"):
            print("ACTION|select_student", flush=True)
            tap_first_text(driver, "Student")

        wait_for_any(driver, ["Learning Goals", "Advance my Career", "Home"], timeout=20)
        snapshot(driver, "arjun_paused_at_learning_goals")

        if count_text(driver, "Learning Goals"):
            print("PAUSED|Learning Goals is visible. Waiting for manual instructions.", flush=True)
            while True:
                time.sleep(30)
        else:
            print("DONE|Learning Goals was not visible after student selection.", flush=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
