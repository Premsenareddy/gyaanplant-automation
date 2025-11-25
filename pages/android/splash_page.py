# pages/android/splash_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class SplashPage(BasePage):

    START_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "🚀 Let's Start Your Learning Journey"
    )

    def is_displayed(self):
        """Splash screen is considered displayed when the Start button is visible."""
        try:
            return self.visible(self.START_BUTTON) is not None
        except:
            return False

    def tap_start(self):
        """Tap on the green Start Your Learning Journey button."""
        self.click(self.START_BUTTON)

