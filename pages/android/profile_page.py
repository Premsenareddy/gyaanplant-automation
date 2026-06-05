# pages/android/profile_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class ProfilePage(BasePage):

    SETTINGS_ICON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Settings")'
    )
    PROFILE_TAB = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Profile")'
    )

    def open_settings(self):
        if self.is_element_present(self.PROFILE_TAB, timeout=3):
            self.wait_and_click(self.PROFILE_TAB)

        if self.is_element_present(self.SETTINGS_ICON, timeout=5):
            self.wait_and_click(self.SETTINGS_ICON)
        else:
            self.tap_by_text("Settings")
