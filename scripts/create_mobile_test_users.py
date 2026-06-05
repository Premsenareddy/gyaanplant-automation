import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_web_page
from pages.web.dashboard_page import DashboardPage


def main():
    email = os.environ["LMS_EMAIL"]
    password = os.environ["LMS_PASSWORD"]
    timestamp = int(time.time())
    users = [
        (f"AUTO_MOBILE_TEST_BITS_{timestamp}", f"auto.mobile.bits.{timestamp}@mailinator.com", "BITS"),
        (f"AUTO_MOBILE_TEST_CMR_{timestamp}", f"auto.mobile.cmr.{timestamp}@mailinator.com", "CMR"),
        (f"AUTO_MOBILE_TEST_SAGAR_{timestamp}", f"auto.mobile.sagar.{timestamp}@mailinator.com", "sagar"),
    ]

    playwright, browser, context, page = create_web_page()
    try:
        dashboard = DashboardPage(page)
        dashboard.load()
        dashboard.login(email, password)
        dashboard.wait_for_dashboard()

        page.goto("https://lms.gyaanplant.co.in/users/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        created = []
        for name, user_email, college in users:
            page.get_by_text("Invite User", exact=True).click()
            page.wait_for_timeout(800)

            inputs = page.locator("input")
            inputs.nth(1).fill(name)
            inputs.nth(2).fill(user_email)

            selects = page.locator("select")
            selects.nth(0).select_option("student")
            selects.nth(1).select_option(label=college)

            page.get_by_text("Send Invitation", exact=True).click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            created.append((name, user_email, college))
            print(f"CREATED_OR_INVITED|{name}|{user_email}|{college}", flush=True)

        print("CREATED_LIST_START")
        for row in created:
            print("|".join(row))
        print("CREATED_LIST_END")
        page.screenshot(path="screenshots/mobile_test_users_created.png", full_page=True)
    finally:
        context.close()
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()
