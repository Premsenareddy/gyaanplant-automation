# pages/android/leaderboard_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class LeaderboardPage(BasePage):

    LEADERBOARD_HEADER = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Leaderboard")'
    )

    def wait_for_loaded(self):
        self.wait_for_visibility(self.LEADERBOARD_HEADER)

    def is_user_present(self, username):
        return self.is_text_visible(username)

