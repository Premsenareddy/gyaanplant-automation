import sys
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.driver import create_android_driver


@pytest.fixture
def android_driver():
    driver = create_android_driver()
    yield driver
    driver.quit()


# ----------------------------------------------------
# 📸 AUTOMATIC SCREENSHOT ON TEST FAILURE
# ----------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    # Only capture screenshot on FAILURE & if android_driver is used
    if result.failed and "android_driver" in item.fixturenames:

        driver = item.funcargs.get("android_driver")
        if driver:

            # Create folder if missing
            os.makedirs("screenshots", exist_ok=True)

            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

            print(f"\n📸 Screenshot saved: {screenshot_path}")

