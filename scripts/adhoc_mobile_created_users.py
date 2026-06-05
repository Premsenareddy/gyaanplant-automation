import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_android_driver
from pages.android.login_page import LoginPage, MobileAuthenticationBlocked
from pages.android.onboarding_page import OnboardingPage
from pages.android.splash_page import SplashPage


APP_PACKAGE = "com.example.gyaanplant_learning_app"


@dataclass
class CreatedUser:
    label: str
    email: str
    password: str
    otp: str = "1234"


CREATED_USERS = [
    CreatedUser("active_bits_numeric", "auto.mobile.active.bits.1780551494@mailinator.com", "12345678"),
    CreatedUser("active_mvsr_text", "auto.mobile.active.mvsr.1780551869@mailinator.com", "Password123"),
    CreatedUser("verify_bits_symbol", "auto.mobile.verify.1780550953@mailinator.com", "Auto@12345"),
]


def adb(*args):
    subprocess.run(["adb", "-s", "emulator-5554", *args], check=False)


def clear_app_data(reason):
    print(f"CLEAR_CACHE|{reason}|{APP_PACKAGE}")
    adb("shell", "pm", "clear", APP_PACKAGE)
    time.sleep(1)


def matching(driver, text):
    locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'),
    ]
    elements = []
    for locator in locators:
        elements.extend(driver.find_elements(*locator))
    return elements


def visible(driver, text):
    return bool(matching(driver, text))


def tap(driver, text):
    elements = matching(driver, text)
    if not elements:
        return False
    elements[0].click()
    time.sleep(2)
    return True


def snapshot(driver, label):
    path = f"screenshots/adhoc_mobile_{label}.png"
    driver.save_screenshot(path)
    print(f"SCREENSHOT|{label}|{path}")


def page_markers(driver):
    names = [
        "Incorrect password",
        "Enter Password",
        "Enter OTP",
        "Roles Selection",
        "Student",
        "Employee",
        "Learning Goals",
        "Advance my Career",
        "Improve Communication",
        "Improve my efficiency",
        "Home",
        "Library",
        "Assessment",
        "Profile",
        "Courses",
        "Daily Attendance",
        "Continue",
        "Login",
        "Enter your email",
    ]
    return {name: len(matching(driver, name)) for name in names}


def wait_until_any(driver, texts, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        markers = page_markers(driver)
        if any(markers.get(text, 0) for text in texts):
            return markers
        time.sleep(1)
    return page_markers(driver)


def complete_intro_if_needed(driver):
    splash = SplashPage(driver)
    onboarding = OnboardingPage(driver)

    if splash.is_displayed():
        splash.tap_start()

    if (
        onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3)
        or onboarding.is_element_present(onboarding.LOGIN_BUTTON, timeout=3)
    ):
        onboarding.complete_onboarding_and_go_to_login()


def attempt_login(user):
    driver = create_android_driver()
    try:
        complete_intro_if_needed(driver)
        login = LoginPage(driver)
        if not login.is_email_screen_displayed():
            snapshot(driver, f"{user.label}_no_email_screen")
            return False, page_markers(driver)

        try:
            login.login(user.email, user.password, otp=user.otp)
        except MobileAuthenticationBlocked as exc:
            print(f"AUTH_BLOCKED|{user.label}|{exc}")

        markers = wait_until_any(
            driver,
            ["Incorrect password", "Roles Selection", "Learning Goals", "Home", "Profile", "Enter OTP", "Enter Password"],
            timeout=15,
        )
        snapshot(driver, f"{user.label}_after_login")
        print(f"LOGIN_RESULT|{user.label}|{markers}")

        success = bool(
            markers["Roles Selection"]
            or markers["Learning Goals"]
            or markers["Home"]
            or markers["Profile"]
        )
        if success:
            crawl_happy_paths(driver, user.label)
        return success, markers
    finally:
        driver.quit()


def complete_post_login(driver, label):
    for index in range(8):
        markers = page_markers(driver)
        print(f"POST_LOGIN_MARKERS|{label}|{index}|{markers}")
        snapshot(driver, f"{label}_post_login_{index}")

        if markers["Home"] or markers["Library"] or markers["Assessment"] or markers["Profile"]:
            return True

        if markers["Roles Selection"] and markers["Student"]:
            print(f"ACTION|{label}|select_student")
            tap(driver, "Student")
            continue

        if markers["Learning Goals"]:
            for goal in ["Advance my Career", "Improve Communication", "Improve my efficiency"]:
                if visible(driver, goal):
                    print(f"ACTION|{label}|select_goal|{goal}")
                    tap(driver, goal)
                    break
            if visible(driver, "Continue"):
                print(f"ACTION|{label}|continue_learning_goals")
                tap(driver, "Continue")
            continue

        if visible(driver, "Continue"):
            print(f"ACTION|{label}|continue")
            tap(driver, "Continue")
            continue

        return False
    return False


def crawl_happy_paths(driver, label):
    reached_main = complete_post_login(driver, label)
    print(f"CRAWL_MAIN_REACHED|{label}|{reached_main}")

    for tab in ["Home", "Library", "Assessment", "Profile"]:
        if tap(driver, tab):
            snapshot(driver, f"{label}_tab_{tab.lower()}")
            print(f"TAB_RESULT|{label}|{tab}|{page_markers(driver)}")

    if tap(driver, "Profile"):
        for item in ["Settings", "Leaderboard", "My Certificates", "My Task"]:
            if tap(driver, item):
                snapshot(driver, f"{label}_profile_{item.lower().replace(' ', '_')}")
                print(f"PROFILE_ITEM_RESULT|{label}|{item}|{page_markers(driver)}")
                driver.back()
                time.sleep(2)


def main():
    results = []
    for user in CREATED_USERS:
        clear_app_data(f"before_{user.label}")
        print(f"ATTEMPT_USER|{user.label}|{user.email}")
        success, markers = attempt_login(user)
        results.append((user.label, success, markers))
        if not success:
            clear_app_data(f"failed_{user.label}")

    print("SUMMARY_START")
    for label, success, markers in results:
        print(f"SUMMARY|{label}|success={success}|markers={markers}")
    print("SUMMARY_END")


if __name__ == "__main__":
    main()
