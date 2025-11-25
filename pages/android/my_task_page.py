# pages/android/my_task_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MyTaskPage(BasePage):

    EMPTY_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("No courses available")'
    )

    def is_empty(self):
        return self.is_text_visible("No courses available")

