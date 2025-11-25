# pages/android/profile_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class ProfilePage(BasePage):

    SETTINGS_ICON = (
        # if there is no id, you may need a content-desc or XPath here
        # placeholder, adjust using inspector
        # Example: (AppiumBy.ACCESSIBILITY_ID, "Settings")
        # For now, let’s use gear via text if any:
        # (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Settings")')
        # Replace once known.
        None
    )

    def open_settings(self):
        # You’ll replace locator above; for now, you can manually plug value
        self.wait_and_click(self.SETTINGS_ICON)

