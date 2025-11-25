# pages/android/login_page.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.android.base_page import BasePage


class LoginPage(BasePage):

    # ----------------------------
    # Locators
    # ----------------------------

    # Email screen
    EMAIL_FIELD = (
        AppiumBy.XPATH,
        "//android.view.View[@content-desc='Enter your email and proceed']/following-sibling::android.widget.EditText"
    )
    EMAIL_SUBMIT_BTN = (AppiumBy.ACCESSIBILITY_ID, "Submit")

    # Password screen
    PASSWORD_FIELD = (
        AppiumBy.XPATH,
        "//android.view.View[@content-desc='Enter Password']/following-sibling::android.widget.EditText"
    )
    PASSWORD_CONTINUE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    # ----------------------------
    # Email Screen
    # ----------------------------

    def is_email_screen_displayed(self):
        return self.visible(self.EMAIL_FIELD) is not None

    def enter_email(self, email: str):
        self.log.info("[LOGIN] Tapping email field")
        field = self.get_element(self.EMAIL_FIELD)
        field.click()

        self.log.info("[LOGIN] Typing email: %s", email)
        field.send_keys(email)

        time.sleep(0.5)

    def submit_email(self):
        self.log.info("[LOGIN] Closing keyboard before clicking Submit")
        self.hide_keyboard()
        time.sleep(0.3)

        self.click(self.EMAIL_SUBMIT_BTN)

    # ----------------------------
    # Password Screen
    # ----------------------------

    def is_password_screen_displayed(self):
        try:
            self.visible(self.PASSWORD_FIELD, timeout=5)
            return True
        except:
            return False

    def enter_password(self, password: str):
        self.log.info("[LOGIN] Tapping password field")
        field = self.get_element(self.PASSWORD_FIELD)
        field.click()

        self.log.info("[LOGIN] Typing password: %s", password)
        field.send_keys(password)

    def submit_password(self):
        self.hide_keyboard()
        time.sleep(0.3)
        self.click(self.PASSWORD_CONTINUE_BTN)

    # ----------------------------
    # High-level test flow
    # ----------------------------

    def login(self, email: str, password: str):
        # Email
        self.enter_email(email)
        self.submit_email()

        # Password
        if self.is_password_screen_displayed():
            self.enter_password(password)
            self.submit_password()
        else:
            self.log.error("[LOGIN] Password screen not displayed!")
            raise Exception("Password screen did not appear")

