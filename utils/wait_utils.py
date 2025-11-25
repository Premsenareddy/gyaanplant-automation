# utils/wait_utils.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from core.logger import get_logger

log = get_logger()

DEFAULT_TIMEOUT = 20


# ------------------------------
# BASIC WAITS
# ------------------------------

def wait_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    log.info(f"[WAIT] Waiting for visibility: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    log.info(f"[WAIT] Waiting for clickable: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_present(driver, locator, timeout=DEFAULT_TIMEOUT):
    log.info(f"[WAIT] Waiting for presence: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


# ------------------------------
# ACTION HELPERS
# ------------------------------

def wait_and_click(driver, locator, timeout=DEFAULT_TIMEOUT):
    el = wait_clickable(driver, locator, timeout)
    log.info(f"[ACTION] Click → {locator}")
    el.click()
    return el


def wait_and_send_keys(driver, locator, value, timeout=DEFAULT_TIMEOUT):
    el = wait_visible(driver, locator, timeout)
    log.info(f"[ACTION] Type '{value}' → {locator}")
    el.clear()
    el.send_keys(value)
    return el


# ------------------------------
# TEXT WAITS (for Splash/Login/Profile screens)
# ------------------------------

def wait_text(driver, text, timeout=DEFAULT_TIMEOUT):
    locator = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().text("{text}")'
    )
    log.info(f"[WAIT] Waiting for text: {text}")
    return wait_visible(driver, locator, timeout)


# ------------------------------
# SMART SCROLL (for long pages)
# ------------------------------

def scroll_until_visible(driver, locator, max_swipes=10):
    """
    Scrolls until the element is found or until max_swipes reached.
    Great for: Profile Page, Resume Page, Settings Page.
    """
    log.info(f"[SCROLL] Scrolling to find element: {locator}")

    from appium.webdriver.common.touch_action import TouchAction
    action = TouchAction(driver)

    for i in range(max_swipes):
        try:
            log.info(f"[SCROLL] Attempt {i+1}/{max_swipes}")
            el = driver.find_element(*locator)
            return el
        except Exception:
            size = driver.get_window_size()
            start_y = size["height"] * 0.7
            end_y = size["height"] * 0.3
            x = size["width"] * 0.5

            action.press(x=x, y=start_y)\
                  .wait(200)\
                  .move_to(x=x, y=end_y)\
                  .release()\
                  .perform()

    raise Exception(f"[ERROR] Element not found after {max_swipes} scrolls → {locator}")


# ------------------------------
# OO-style Wait Wrapper (used by BasePage)
# ------------------------------

class WaitUtils:
    def __init__(self, driver, default_timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.default_timeout = default_timeout

    def wait_for_element(self, locator, timeout: int | None = None):
        """
        Simple wrapper used by BasePage.get_element/send_keys/tap.
        Currently uses visibility wait by default.
        """
        t = timeout or self.default_timeout
        return wait_visible(self.driver, locator, t)


