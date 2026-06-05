import os
import re
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.driver import create_web_page
from pages.web.dashboard_page import DashboardPage


def invite_user(page, name, email, college):
    page.goto("https://lms.gyaanplant.co.in/users/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.get_by_text("Invite User", exact=True).click()
    page.wait_for_timeout(800)

    page.locator("input").nth(1).fill(name)
    page.locator("input").nth(2).fill(email)
    page.locator("select").nth(0).select_option("student")
    page.locator("select").nth(1).select_option(label=college)
    page.locator("button").filter(has_text="Send Invitation").click(force=True)
    page.wait_for_timeout(4000)

    body = page.locator("body").inner_text(timeout=10000)
    if f"Invitation sent to {email}" not in body:
        raise RuntimeError(f"Invitation was not confirmed for {email}")


def invitation_link_from_mailinator(page, inbox):
    page.goto(f"https://www.mailinator.com/v4/public/inboxes.jsp?to={inbox}", wait_until="domcontentloaded")
    page.wait_for_timeout(6000)
    page.get_by_text("Invitation to join", exact=False).first.click()
    page.wait_for_timeout(4000)

    links = page.locator("a").evaluate_all("(els) => els.map(a => a.href)")
    for href in links:
        if "lms.gyaanplant.co.in/invitation" in href:
            return href
    raise RuntimeError(f"No GyaanPlant invitation link found for {inbox}")


def accept_invite(page, invite_url, name, password):
    page.goto(invite_url, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.locator("input").nth(0).fill(name)
    page.locator("input").nth(1).fill(password)
    page.locator("input").nth(2).fill(password)
    page.locator("button").last.click(force=True)
    page.wait_for_timeout(5000)

    body = page.locator("body").inner_text(timeout=10000)
    if "Account activated" not in body and "/login" not in page.url:
        raise RuntimeError(f"Invite activation did not complete. URL={page.url} BODY={body[:500]}")


def main():
    admin_email = os.environ["LMS_EMAIL"]
    admin_password = os.environ["LMS_PASSWORD"]
    college = os.environ.get("MOBILE_ACTIVATE_COLLEGE", "BITS")
    user_password = os.environ.get("MOBILE_ACTIVATE_PASSWORD", "12345678")
    timestamp = int(time.time())

    name = f"AUTO_MOBILE_ACTIVE_{college.upper()}_{timestamp}"
    inbox = f"auto.mobile.active.{college.lower()}.{timestamp}"
    email = f"{inbox}@mailinator.com"

    playwright, browser, context, page = create_web_page()
    try:
        dashboard = DashboardPage(page)
        dashboard.load()
        dashboard.login(admin_email, admin_password)
        dashboard.wait_for_dashboard()
        invite_user(page, name, email, college)

        invite_url = invitation_link_from_mailinator(page, inbox)
        accept_invite(page, invite_url, name, user_password)

        print(f"ACTIVATED_USER|{name}|{email}|{user_password}|{college}|{invite_url}")
    finally:
        context.close()
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()
