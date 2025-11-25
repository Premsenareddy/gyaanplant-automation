from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from config.settings import AndroidConfig


def create_android_driver():
    config = AndroidConfig()

    options = UiAutomator2Options()
    options.set_capability("platformName", config.platformName)
    options.set_capability("appium:automationName", config.automationName)
    options.set_capability("appium:deviceName", config.deviceName)
    options.set_capability("appium:platformVersion", config.platformVersion)
    options.set_capability("appium:app", config.app)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:appWaitActivity", config.appWaitActivity)

    driver = WebDriver(
        command_executor="http://127.0.0.1:4723",
        options=options
    )

    return driver

