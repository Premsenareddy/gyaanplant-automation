from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class OnboardingPage(BasePage):

    NEXT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Next")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Login")

    def tap_next_if_present(self):
        """Tap Next if available, else skip."""
        if self.is_element_present(self.NEXT_BUTTON):
            self.click(self.NEXT_BUTTON)
            return True
        return False

    def tap_login(self):
        self.click(self.LOGIN_BUTTON)

    def complete_onboarding_and_go_to_login(self):
        # Try tapping Next until it's gone
        for _ in range(4):  # upper bound to avoid infinite loops
            if not self.tap_next_if_present():
                break

        # Now Login button should be visible
        self.tap_login()

    # Keep the historical page-level helper while using BasePage's timeout-aware wait.
    def is_element_present(self, locator, timeout=3):
        return super().is_element_present(locator, timeout=timeout)
