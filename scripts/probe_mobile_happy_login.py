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


def count_text(driver, text):
    locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    return sum(len(driver.find_elements(*locator)) for locator in locators)


def tap_first_text(driver, text):
    locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    for locator in locators:
        elements = driver.find_elements(*locator)
        if elements:
            elements[0].click()
            return True
    return False


def tap_center(element, driver):
    rect = element.rect
    x = rect["x"] + rect["width"] // 2
    y = rect["y"] + rect["height"] // 2
    print(f"ACTION|center_tap|{x}|{y}")
    driver.tap([(x, y)])


def wait_for_any_marker(driver, markers, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        counts = {marker: count_text(driver, marker) for marker in markers}
        if any(counts.values()):
            return counts
        time.sleep(1)
    return {marker: count_text(driver, marker) for marker in markers}


def continue_post_login_onboarding(driver):
    decisions = [
        ("Roles Selection", "Student"),
        ("Learning Goals", "Advance my Career"),
        ("Learning Goals", "Continue"),
        ("Experience Level", "Beginner"),
        ("Experience Level", "Continue"),
        ("Interests", "Technology"),
        ("Interests", "Continue"),
        ("Skills", "Communication"),
        ("Skills", "Continue"),
    ]

    for step in range(10):
        markers = {
            "Home": count_text(driver, "Home"),
            "Profile": count_text(driver, "Profile"),
            "Roles Selection": count_text(driver, "Roles Selection"),
            "Learning Goals": count_text(driver, "Learning Goals"),
            "Experience Level": count_text(driver, "Experience Level"),
            "Interests": count_text(driver, "Interests"),
            "Skills": count_text(driver, "Skills"),
            "Continue": count_text(driver, "Continue"),
        }
        print(f"ONBOARDING_MARKERS|{step}|{markers}")
        if markers["Home"] or markers["Profile"]:
            return

        progressed = False
        for screen, choice in decisions:
            if count_text(driver, screen) and count_text(driver, choice):
                print(f"ACTION|post_login_choice|{screen}|{choice}")
                tap_first_text(driver, choice)
                time.sleep(2)
                if screen == "Learning Goals" and count_text(driver, "Continue"):
                    print("ACTION|post_login_continue_after_learning_goal")
                    tap_first_text(driver, "Continue")
                    time.sleep(3)
                progressed = True
                break

        if not progressed and count_text(driver, "Continue"):
            print("ACTION|post_login_continue")
            tap_first_text(driver, "Continue")
            time.sleep(3)
            progressed = True

        if not progressed:
            print("ACTION|post_login_no_known_step")
            return


def main():
    email = os.environ["ANDROID_LMS_EMAIL"]
    password = os.environ["ANDROID_LMS_PASSWORD"]
    output = os.environ.get("MOBILE_HAPPY_PROBE_SCREENSHOT", "screenshots/happy_probe_after_login.png")

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

        login.enter_email(email)
        login.submit_email()
        time.sleep(2)

        print("STATE_AFTER_EMAIL_MARKER")
        print(driver.page_source[:8000])

        if login.is_password_screen_displayed(timeout=5):
            login.enter_password(password)
            login.hide_keyboard()
            continue_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Continue")
            tap_center(continue_button, driver)
            markers = wait_for_any_marker(
                driver,
                ["Student", "Teacher", "Home", "Profile", "Enter OTP", "Incorrect password"],
                timeout=25,
            )
            print(f"POST_PASSWORD_MARKERS|{markers}")
        elif login.is_otp_screen_displayed(timeout=3):
            otp = os.environ.get("ANDROID_LMS_OTP")
            if otp:
                login.enter_otp(otp)
                login.submit_otp()
                time.sleep(12)

        print("STATE_AFTER_AUTH_MARKER")
        print(driver.page_source[:16000])
        driver.save_screenshot(output)

        for text in ["Student", "Teacher", "College", "Organization", "Continue", "Home", "Profile", "Incorrect password"]:
            print(f"TEXT_COUNT|{text}|{count_text(driver, text)}")

        if count_text(driver, "Student"):
            print("ACTION|tap_student")
            tap_first_text(driver, "Student")
            time.sleep(2)
            if count_text(driver, "Continue"):
                print("ACTION|tap_continue_after_student")
                tap_first_text(driver, "Continue")
                time.sleep(8)
            continue_post_login_onboarding(driver)
            driver.save_screenshot(output.replace(".png", "_after_student.png"))
            print("STATE_AFTER_STUDENT_MARKER")
            print(driver.page_source[:16000])
            for text in ["Home", "Profile", "Courses", "Assessment", "Daily Attendance"]:
                print(f"POST_STUDENT_TEXT_COUNT|{text}|{count_text(driver, text)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
