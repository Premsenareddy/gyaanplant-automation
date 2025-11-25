# pages/android/settings_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class SettingsPage(BasePage):

    MY_PROFILE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("My Profile")'
    )
    MY_RESUME = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("My Resume")'
    )
    MY_CERTIFICATES = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("My Certificates")'
    )
    LEADERBOARD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Leaderboard")'
    )
    MY_TASK = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("My Task")'
    )
    LOGOUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Logout")'
    )

    def open_my_profile(self):
        self.wait_and_click(self.MY_PROFILE)

    def open_my_resume(self):
        self.wait_and_click(self.MY_RESUME)

    def open_my_certificates(self):
        self.wait_and_click(self.MY_CERTIFICATES)

    def open_leaderboard(self):
        self.wait_and_click(self.LEADERBOARD)

    def open_my_task(self):
        self.wait_and_click(self.MY_TASK)

    def logout(self):
        self.wait_and_click(self.LOGOUT)

