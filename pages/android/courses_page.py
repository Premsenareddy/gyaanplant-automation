# pages/android/courses_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class CoursesPage(BasePage):

    def open_course_in_my_courses(self, course_name: str):
        self.tap_by_text(course_name)

    ENROLL_NOW_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Enroll Now")'
    )

    NEXT_CHAPTER_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Next Chapter")'
    )

    ACHIEVEMENT_POPUP_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Achievement Accomplished")'
    )
    START_ASSESSMENT_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Start Assessment")'
    )

    def enroll_current_course(self):
        self.wait_and_click(self.ENROLL_NOW_BTN)

    def go_through_all_chapters(self, chapter_count=2):
        # rough approach – call Next Chapter N times
        for _ in range(chapter_count):
            self.wait_and_click(self.NEXT_CHAPTER_BTN)

    def wait_for_achievement_popup(self):
        self.wait_for_visibility(self.ACHIEVEMENT_POPUP_TITLE)

    def start_assessment_from_popup(self):
        self.wait_and_click(self.START_ASSESSMENT_BTN)

