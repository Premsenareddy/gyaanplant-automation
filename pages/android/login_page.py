# pages/android/login_page.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.android.base_page import BasePage


class MobileAuthenticationBlocked(Exception):
    """Raised when the APK needs auth data the automation run cannot provide."""


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
    OTP_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Enter OTP")'
    )
    OTP_FIELDS = (AppiumBy.XPATH, "//android.widget.EditText")
    OTP_CONTINUE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    def _tap_control(self, locator, timeout=10):
        element = self.click(locator, timeout=timeout)
        time.sleep(0.5)
        return element

    def _tap_control_center(self, locator, timeout=10):
        element = self.get_element(locator)
        rect = element.rect
        center_x = rect["x"] + rect["width"] // 2
        center_y = rect["y"] + rect["height"] // 2
        self.log.info("[LOGIN] Center tap fallback at (%s, %s)", center_x, center_y)
        self.driver.tap([(center_x, center_y)])
        time.sleep(0.5)

    # ----------------------------
    # Email Screen
    # ----------------------------

    def is_email_screen_displayed(self):
        return self.visible(self.EMAIL_FIELD) is not None

    def enter_email(self, email: str):
        self.log.info("[LOGIN] Tapping email field")
        field = self.get_element(self.EMAIL_FIELD)
        field.click()
        field.clear()

        self.log.info("[LOGIN] Typing email: %s", email)
        field.send_keys(email)

        time.sleep(0.5)

    def submit_email(self):
        self.log.info("[LOGIN] Closing keyboard before clicking Submit")
        self.hide_keyboard()
        time.sleep(0.3)

        self._tap_control(self.EMAIL_SUBMIT_BTN)

        if not self.is_password_screen_displayed(timeout=3):
            if self.is_otp_screen_displayed(timeout=3):
                return
            self.log.info("[LOGIN] Password screen not visible yet; retrying Submit with center tap")
            self._tap_control_center(self.EMAIL_SUBMIT_BTN)

    # ----------------------------
    # Password Screen
    # ----------------------------

    def is_password_screen_displayed(self, timeout=12):
        try:
            self.visible(self.PASSWORD_FIELD, timeout=timeout)
            return True
        except:
            return False

    def is_otp_screen_displayed(self, timeout=5):
        try:
            self.visible(self.OTP_TITLE, timeout=timeout)
            return True
        except:
            return False

    def enter_password(self, password: str):
        self.log.info("[LOGIN] Tapping password field")
        field = self.get_element(self.PASSWORD_FIELD)
        field.click()
        field.clear()

        self.log.info("[LOGIN] Typing password: %s", password)
        field.send_keys(password)

    def submit_password(self):
        self.hide_keyboard()
        time.sleep(0.3)
        self._tap_control(self.PASSWORD_CONTINUE_BTN)

        if self.is_password_screen_displayed(timeout=3):
            self.log.info("[LOGIN] Password screen still visible; retrying Continue with center tap")
            self._tap_control_center(self.PASSWORD_CONTINUE_BTN)

    # ----------------------------
    # OTP Screen
    # ----------------------------

    def enter_otp(self, otp: str):
        fields = self.driver.find_elements(*self.OTP_FIELDS)
        if len(fields) < len(otp):
            raise MobileAuthenticationBlocked(
                f"OTP screen displayed, but only {len(fields)} OTP fields were found"
            )

        for index, digit in enumerate(otp):
            fields[index].click()
            fields[index].send_keys(digit)

    def submit_otp(self):
        self.hide_keyboard()
        time.sleep(0.3)
        self._tap_control(self.OTP_CONTINUE_BTN)

    # ----------------------------
    # High-level test flow
    # ----------------------------

    def login(self, email: str, password: str, otp: str | None = None):
        # Email
        self.enter_email(email)
        self.submit_email()

        if self.is_password_screen_displayed():
            self.enter_password(password)
            self.submit_password()
            return

        if self.is_otp_screen_displayed():
            if not otp:
                raise MobileAuthenticationBlocked(
                    "Mobile app displayed an OTP screen. Set ANDROID_LMS_OTP for this run."
                )
            self.enter_otp(otp)
            self.submit_otp()
            return

        self.log.error("[LOGIN] Neither password nor OTP screen displayed after email submit")
        raise MobileAuthenticationBlocked(
            "Mobile app did not show a supported auth screen after email submit."
        )
