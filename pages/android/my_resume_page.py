# pages/android/my_resume_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MyResumePage(BasePage):

    EDIT_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Edit")'
    )

    EXPORT_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Export")'
    )

    # Fields on Edit screen
    DOB_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Date of Birth")'
    )

    ADDRESS_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Address")'
    )

    ADD_EXPERIENCE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Add Experience")'
    )

    ADD_PROJECT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Add Project")'
    )

    SAVE_UPDATE_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Save & Update Resume")'
    )

    def click_edit(self):
        self.wait_and_click(self.EDIT_BTN)

    def export_resume(self):
        self.wait_and_click(self.EXPORT_BTN)

    def update_address(self, address):
        self.wait_and_send_keys(self.ADDRESS_INPUT, address)

    def update_dob(self, dob):
        self.wait_and_send_keys(self.DOB_INPUT, dob)

    def save_resume(self):
        self.wait_and_click(self.SAVE_UPDATE_BTN)

