# pages/android/my_certificates_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MyCertificatesPage(BasePage):

    EMPTY_STATE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("No certificate available")'
    )

    DOWNLOAD_CERTIFICATE_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Download Certificate")'
    )

    def is_empty_state_visible(self):
        return self.is_text_visible("No certificate available")

    def download_certificate(self):
        self.wait_and_click(self.DOWNLOAD_CERTIFICATE_BTN)

