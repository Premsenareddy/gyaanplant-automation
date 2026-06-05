import time

from appium.webdriver.common.appiumby import AppiumBy

from .base_page import BasePage


class PostLoginOnboardingPage(BasePage):
    ROLES_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Roles Selection")'
    )
    STUDENT_CARD = (AppiumBy.ACCESSIBILITY_ID, "Student")
    EMPLOYEE_CARD = (AppiumBy.ACCESSIBILITY_ID, "Employee")

    LEARNING_GOALS_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Learning Goals")'
    )
    ADVANCE_CAREER = (AppiumBy.ACCESSIBILITY_ID, "Advance my Career")
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    EXPERIENCE_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Experience")'
    )
    BEGINNER_OPTION = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Beginner")'
    )

    def is_roles_selection_displayed(self, timeout=3):
        return self.is_element_present(self.ROLES_TITLE, timeout=timeout)

    def is_learning_goals_displayed(self, timeout=3):
        return self.is_element_present(self.LEARNING_GOALS_TITLE, timeout=timeout)

    def is_continue_visible(self, timeout=2):
        return self.is_element_present(self.CONTINUE_BUTTON, timeout=timeout)

    def choose_student(self):
        self.wait_and_click(self.STUDENT_CARD, timeout=10)
        time.sleep(1)

    def choose_default_learning_goal(self):
        self.wait_and_click(self.ADVANCE_CAREER, timeout=10)
        time.sleep(1)
        if self.is_continue_visible(timeout=3):
            self.wait_and_click(self.CONTINUE_BUTTON, timeout=10)
            time.sleep(2)

    def complete_if_present(self, max_steps=6):
        for _ in range(max_steps):
            if self.is_roles_selection_displayed(timeout=2):
                self.choose_student()
                continue

            if self.is_learning_goals_displayed(timeout=2):
                self.choose_default_learning_goal()
                continue

            if self.is_element_present(self.EXPERIENCE_TITLE, timeout=2):
                if self.is_element_present(self.BEGINNER_OPTION, timeout=2):
                    self.wait_and_click(self.BEGINNER_OPTION, timeout=10)
                    time.sleep(1)
                if self.is_continue_visible(timeout=2):
                    self.wait_and_click(self.CONTINUE_BUTTON, timeout=10)
                    time.sleep(2)
                continue

            return
