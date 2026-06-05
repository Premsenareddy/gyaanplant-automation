import sys
import time
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_android_driver
from config.settings import AndroidTestUser
from pages.android.login_page import LoginPage, MobileAuthenticationBlocked
from pages.android.onboarding_page import OnboardingPage
from pages.android.splash_page import SplashPage


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
    path = f"screenshots/mobile_happy_{label}.png"
    driver.save_screenshot(path)
    print(f"SCREENSHOT|{label}|{path}")
    print(f"SOURCE|{label}|{driver.page_source[:6000]}")


def markers(driver):
    names = [
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
        "Settings",
        "Leaderboard",
        "My Certificates",
        "My Task",
        "Courses",
        "Daily Attendance",
        "Continue",
    ]
    return {name: len(matching(driver, name)) for name in names}


def complete_post_login_setup(driver):
    for step in range(10):
        current = markers(driver)
        print(f"SETUP_MARKERS|{step}|{current}")
        snapshot(driver, f"setup_{step}")

        if current["Home"] or current["Library"] or current["Assessment"] or current["Profile"]:
            return True

        if current["Roles Selection"] and current["Student"]:
            print("ACTION|select_student")
            tap(driver, "Student")
            continue

        if current["Learning Goals"]:
            if visible(driver, "Advance my Career"):
                print("ACTION|select_goal_advance_my_career")
                tap(driver, "Advance my Career")
                if visible(driver, "Continue"):
                    print("ACTION|continue_after_learning_goal")
                    tap(driver, "Continue")
                continue
            if visible(driver, "Continue"):
                print("ACTION|continue_learning_goals")
                tap(driver, "Continue")
                continue

        if visible(driver, "Continue"):
            print("ACTION|generic_continue")
            tap(driver, "Continue")
            continue

        return False
    return False


def wait_for_launch_settle(driver, timeout=30):
    interesting = [
        "Let's Start Your Learning Journey",
        "Login",
        "Enter your email",
        "Enter Password",
        "Enter OTP",
        "Roles Selection",
        "Learning Goals",
        "Home",
        "Profile",
    ]
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = {name: len(matching(driver, name)) for name in interesting}
        if any(current.values()):
            print(f"LAUNCH_SETTLED|{current}")
            return
        time.sleep(1)
    print("LAUNCH_SETTLED|no_known_markers")


def login_if_needed(driver):
    user = AndroidTestUser()
    splash = SplashPage(driver)
    onboarding = OnboardingPage(driver)
    login = LoginPage(driver)

    if splash.is_displayed():
        print("ACTION|splash_start")
        splash.tap_start()

    if (
        onboarding.is_element_present(onboarding.NEXT_BUTTON, timeout=3)
        or onboarding.is_element_present(onboarding.LOGIN_BUTTON, timeout=3)
    ):
        print("ACTION|complete_intro_onboarding")
        onboarding.complete_onboarding_and_go_to_login()

    if login.is_email_screen_displayed():
        print(f"ACTION|login|{user.email}")
        try:
            login.login(user.email, user.password, otp=user.otp)
            time.sleep(5)
        except MobileAuthenticationBlocked as exc:
            print(f"BLOCKED|auth|{exc}")


def open_tab(driver, name):
    print(f"ACTION|open_tab|{name}")
    if tap(driver, name):
        time.sleep(3)
        snapshot(driver, f"tab_{name.lower().replace(' ', '_')}")
        print(f"TAB_MARKERS|{name}|{markers(driver)}")
        return True
    print(f"SKIP|tab_not_found|{name}")
    return False


def main():
    driver = create_android_driver()
    try:
        wait_for_launch_settle(driver)
        snapshot(driver, "initial")
        login_if_needed(driver)
        wait_for_launch_settle(driver, timeout=15)
        snapshot(driver, "after_login_if_needed")
        completed_setup = complete_post_login_setup(driver)
        print(f"RESULT|post_login_setup_completed_or_home_visible|{completed_setup}")

        for tab in ["Home", "Library", "Assessment", "Profile"]:
            open_tab(driver, tab)

        if visible(driver, "Profile"):
            open_tab(driver, "Profile")
            for item in ["Settings", "Leaderboard", "My Certificates", "My Task"]:
                if open_tab(driver, item):
                    driver.back()
                    time.sleep(2)
                    snapshot(driver, f"after_back_from_{item.lower().replace(' ', '_')}")

        snapshot(driver, "final")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
