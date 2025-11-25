# pages/android/assessment_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class AssessmentPage(BasePage):

    IMPORTANT_POINTS_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Important Points to Remember")'
    )
    START_QUIZ_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Start Quiz")'
    )

    def wait_for_assessment_intro(self):
        self.wait_for_visibility(self.IMPORTANT_POINTS_TITLE)

    def start_quiz(self):
        self.wait_and_click(self.START_QUIZ_BTN)

