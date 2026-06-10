from pathlib import Path
from playwright.sync_api import sync_playwright

from config.settings import WebConfig


def create_web_page():
    config = WebConfig()
    playwright = sync_playwright().start()

    try:
        playwright.selectors.set_test_id_attribute(config.test_id_attribute)
        browser_name = config.browser.lower()
        browser_type = getattr(playwright, browser_name, playwright.chromium)

        launch_options = {"headless": config.headless, "slow_mo": config.slow_mo_ms}
        if config.browser_executable_path:
            launch_options["executable_path"] = config.browser_executable_path
        elif browser_name == "chromium" and Path("/opt/homebrew/bin/chromium").exists():
            launch_options["executable_path"] = "/opt/homebrew/bin/chromium"

        browser = browser_type.launch(**launch_options)
        context_options = {
            "viewport": {
                "width": config.viewport_width,
                "height": config.viewport_height,
            },
        }
        if config.record_video:
            context_options["record_video_dir"] = str(
                Path(config.artifacts_dir) / "videos"
            )

        context = browser.new_context(**context_options)
        context.set_default_timeout(config.timeout_ms)
        context.set_default_navigation_timeout(config.timeout_ms)
        page = context.new_page()

        return playwright, browser, context, page
    except Exception:
        playwright.stop()
        raise
