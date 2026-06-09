import sys
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.driver import create_android_driver, create_web_page


@pytest.fixture
def android_driver():
    driver = create_android_driver()
    yield driver
    driver.quit()


@pytest.fixture
def web_page():
    playwright, browser, context, page = create_web_page()
    yield page
    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------
# 📸 AUTOMATIC SCREENSHOT ON TEST FAILURE
# ----------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.failed:
        driver = None
        if "android_driver" in item.fixturenames:
            driver = item.funcargs.get("android_driver")
        elif "web_page" in item.fixturenames:
            page = item.funcargs.get("web_page")
            if page:
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = f"screenshots/{item.name}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n📸 Screenshot saved: {screenshot_path}")
            return

        if driver:
            os.makedirs("screenshots", exist_ok=True)

            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

            print(f"\n📸 Screenshot saved: {screenshot_path}")
