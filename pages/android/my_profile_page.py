# pages/android/my_profile_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MyProfilePage(BasePage):

    FULLNAME_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Full Name")'
    )

    MOBILE_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Mobile Number")'
    )

    EMAIL_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Enter Email")'
    )

    SAVE_CHANGES_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Save Changes")'
    )

    def update_fullname(self, value):
        self.wait_and_send_keys(self.FULLNAME_INPUT, value)

    def update_mobile(self, value):
        self.wait_and_send_keys(self.MOBILE_INPUT, value)

    def update_email(self, value):
        self.wait_and_send_keys(self.EMAIL_INPUT, value)

    def save(self):
        self.wait_and_click(self.SAVE_CHANGES_BTN)

