# pages/android/base_page.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from core.logger import get_logger
from utils.wait_utils import (
    wait_visible,
    wait_clickable,
    wait_present,
    wait_and_click,
    wait_and_send_keys,
    wait_text,
    scroll_until_visible,
    WaitUtils,
)

DEFAULT_TIMEOUT = 20


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.log = get_logger()
        self.wait = WaitUtils(driver)

    # ---------------------------
    # Generic Wait Helpers
    # ---------------------------

    def visible(self, locator, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Waiting for visible: {locator}")
        return wait_visible(self.driver, locator, timeout)

    def clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Waiting for clickable: {locator}")
        return wait_clickable(self.driver, locator, timeout)

    def present(self, locator, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Waiting for presence: {locator}")
        return wait_present(self.driver, locator, timeout)

    def is_text_visible(self, text, timeout=DEFAULT_TIMEOUT):
        try:
            wait_text(self.driver, text, timeout)
            return True
        except Exception:
            return False

    # ---------------------------
    # Keyboard Handling
    # ---------------------------

    def wait_for_keyboard(self, timeout=3):
        """
        Wait until Android soft keyboard is shown.
        Useful for slow emulators where keyboard opens slowly.
        """
        for _ in range(timeout * 10):
            try:
                if self.driver.is_keyboard_shown():
                    return True
            except:
                pass
            time.sleep(0.1)
        return False

    def hide_keyboard(self):
        """Force-hide the Android soft keyboard safely."""
        try:
            self.driver.hide_keyboard()
            self.log.info("[PAGE] Keyboard hidden using hide_keyboard()")
        except Exception:
            # Fallback: tap outside textbox
            self.log.info("[PAGE] hide_keyboard() failed → tapping blank area")
            try:
                self.driver.tap([(10, 10)])   # Tap top-left corner
            except:
                pass

    # ---------------------------
    # Common User Actions
    # ---------------------------

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Click: {locator}")
        return wait_and_click(self.driver, locator, timeout)

    def tap(self, locator):
        self.log.info(f"[PAGE] Tap (WaitUtils): {locator}")
        element = self.wait.wait_for_element(locator)
        element.click()
        return element

    def type(self, locator, text, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Type '{text}' into {locator}")
        return wait_and_send_keys(self.driver, locator, text, timeout)

    def send_keys(self, locator, text):
        self.log.info(f"[PAGE] send_keys (WaitUtils): '{text}' into {locator}")
        element = self.wait.wait_for_element(locator)
        element.send_keys(text)
        return element

    def get_element(self, locator):
        self.log.info(f"[PAGE] Get element: {locator}")
        return self.wait.wait_for_element(locator)

    def tap_text(self, text, timeout=DEFAULT_TIMEOUT):
        self.log.info(f"[PAGE] Tap text: {text}")
        return wait_text(self.driver, text, timeout)

    # ---------------------------
    # Scrolling
    # ---------------------------

    def scroll_to(self, locator):
        self.log.info(f"[PAGE] Scroll until visible: {locator}")
        return scroll_until_visible(self.driver, locator)

