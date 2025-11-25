# pages/android/home_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class HomePage(BasePage):

    DAILY_ATTENDANCE_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Daily Attendance")'
    )
    DAILY_ATTENDANCE_MARK_PRESENT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Mark Present")'
    )
    MY_COURSES_LINK = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("MY COURSES")'
    )
    NEW_ADDITIONS_SEE_MORE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("SEE MORE")'
    )

    HOME_TAB = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Home")'
    )
    LIBRARY_TAB = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Library")'
    )
    ASSESSMENT_TAB = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Assessment")'
    )
    PROFILE_TAB = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Profile")'
    )

    def wait_for_home_loaded(self):
        self.wait_for_visibility(self.HOME_TAB)

    def handle_daily_attendance_if_present(self):
        try:
            self.wait_for_visibility(self.DAILY_ATTENDANCE_TITLE, timeout=5)
            self.wait_and_click(self.DAILY_ATTENDANCE_MARK_PRESENT, timeout=5)
        except Exception:
            # Popup not shown – fine
            pass

    def open_my_courses(self):
        self.wait_and_click(self.MY_COURSES_LINK)

    def open_course_from_new_additions(self, course_name: str):
        # scroll if needed, but first try by visible text
        self.tap_by_text(course_name)

    def go_to_library(self):
        self.wait_and_click(self.LIBRARY_TAB)

    def go_to_assessment_tab(self):
        self.wait_and_click(self.ASSESSMENT_TAB)

    def go_to_profile(self):
        self.wait_and_click(self.PROFILE_TAB)

