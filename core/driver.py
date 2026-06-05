from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from pathlib import Path
from playwright.sync_api import sync_playwright

from config.settings import AndroidConfig, WebConfig


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
    options.set_capability("appium:noReset", config.no_reset)
    options.set_capability("appium:fullReset", config.full_reset)

    driver = WebDriver(
        command_executor=config.appium_server_url,
        options=options
    )

    return driver


def create_web_page():
    config = WebConfig()
    playwright = sync_playwright().start()

    try:
        browser_name = config.browser.lower()
        browser_type = getattr(playwright, browser_name, playwright.chromium)

        launch_options = {"headless": config.headless, "slow_mo": config.slow_mo_ms}
        if config.browser_executable_path:
            launch_options["executable_path"] = config.browser_executable_path
        elif browser_name == "chromium" and Path("/opt/homebrew/bin/chromium").exists():
            launch_options["executable_path"] = "/opt/homebrew/bin/chromium"

        browser = browser_type.launch(**launch_options)
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        context.set_default_timeout(config.timeout_ms)
        page = context.new_page()

        return playwright, browser, context, page
    except Exception:
        playwright.stop()
        raise
