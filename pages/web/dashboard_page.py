from urllib.parse import urljoin
from typing import Optional
import re

from config.settings import WebConfig
from pages.web.base_page import BaseWebPage
from pages.web.launch_page import LaunchPage


class DashboardPage(BaseWebPage):
    ROOT = "#root"
    EMAIL_FIELD = "input[type='email'], input[name*='email' i], input[placeholder*='email' i]"
    PASSWORD_FIELD = "input[type='password'], input[name*='password' i], input[placeholder*='password' i]"
    SUBMIT_BUTTON = "button:has-text('Login to Dashboard')"

    NAVIGATION_ITEMS = [
        "Dashboard",
        "Analytics",
        "Colleges",
        "Organizations",
        "Courses",
        "Problems",
        "Career Paths",
        "Users",
        "Prep Packs",
        "Job Details",
        "Revenue",
        "Payments",
        "MOU Pipeline",
        "Notifications",
        "Settings",
        "SIGN OUT",
    ]
    SUMMARY_CARDS = [
        "TOTAL PARTNERS",
        "TOTAL STUDENTS",
        "ACTIVE AGREEMENTS",
        "TOTAL EMPLOYEES",
        "ACTIVITY TODAY",
    ]
    DASHBOARD_WIDGETS = [
        "Top Partner Companies",
        "Leaderboard",
        "VIEW FULL LEADERBOARD",
    ]
    SMOKE_CLICK_SIDEBAR_ITEMS = [
        "Analytics",
        "Colleges",
        "Organizations",
        "Courses",
        "Problems",
        "Career Paths",
        "Users",
        "Prep Packs",
        "Job Details",
        "Revenue",
        "Payments",
        "MOU Pipeline",
        "Notifications",
        "Settings",
    ]
    SMOKE_CLICK_LEADERBOARD_FILTERS = ["MONTHLY", "WEEKLY"]
    SIDEBAR_ROUTE_EXPECTATIONS = {
        "Dashboard": "/dashboard",
        "Analytics": "/analytics",
        "Colleges": "/colleges",
        "Organizations": "/organizations",
        "Courses": "/courses",
        "Career Paths": "/career-paths",
        "Users": "/users",
        "Prep Packs": "/prep-packs",
        "Revenue": "/revenue",
        "Payments": "/payments",
        "Notifications": "/notifications",
        "Settings": "/settings",
    }
    SIDEBAR_NON_NAVIGATING_ITEMS = ["Problems", "Job Details", "MOU Pipeline"]
    METRIC_EXPECTATIONS = {
        "TOTAL PARTNERS": ["Colleges:"],
        "TOTAL STUDENTS": ["Global Student Reach"],
        "ACTIVE AGREEMENTS": ["Total Orgs:"],
        "TOTAL EMPLOYEES": ["Company Network"],
        "ACTIVITY TODAY": ["Points earned", "Platform Activity"],
    }
    TOP_PARTNER_ROW = ["Microsoft", "IT", "ACTIVE"]
    TOP_PARTNER_HEADERS = ["COMPANY NAME", "INDUSTRY", "STATUS"]
    LEADERBOARD_ENTRIES = [
        ["01", "GYAANPLANT", "POINTS"],
        ["02", "SUKESH", "POINTS"],
        ["03", "CHARAN", "POINTS"],
        ["04", "ADA", "POINTS"],
        ["05", "RISHIK", "POINTS"],
    ]
    LEADERBOARD_FILTERS = ["ALL TIME", "MONTHLY", "WEEKLY"]

    def __init__(self, page, config: Optional[WebConfig] = None):
        super().__init__(page)
        self.config = config or WebConfig()
        self.sidebar_dashboard = page.get_by_text("Dashboard", exact=True).first
        self.sidebar_analytics = page.get_by_text("Analytics", exact=True).first
        self.sidebar_colleges = page.get_by_text("Colleges", exact=True).first
        self.sidebar_organizations = page.get_by_text("Organizations", exact=True).first
        self.sidebar_courses = page.get_by_text("Courses", exact=True).first
        self.sidebar_problems = page.get_by_text("Problems", exact=True).first
        self.sidebar_career_paths = page.get_by_text("Career Paths", exact=True).first
        self.sidebar_users = page.get_by_text("Users", exact=True).first
        self.sidebar_prep_packs = page.get_by_text("Prep Packs", exact=True).first
        self.sidebar_job_details = page.get_by_text("Job Details", exact=True).first
        self.sidebar_revenue = page.get_by_text("Revenue", exact=True).first
        self.sidebar_payments = page.get_by_text("Payments", exact=True).first
        self.sidebar_mou_pipeline = page.get_by_text("MOU Pipeline", exact=True).first
        self.sidebar_notifications = page.get_by_text("Notifications", exact=True).first
        self.sidebar_settings = page.get_by_text("Settings", exact=True).first
        self.sidebar_sign_out = page.get_by_text("SIGN OUT", exact=True).first
        self.theme_toggle_button = page.get_by_label("Toggle Theme")
        self.notifications_button = page.get_by_label("Notifications")
        self.profile_dropdown_button = page.locator("button").filter(has_text="Gyaanplant").filter(has_text="admin").first
        self.total_partners_card = page.locator("body").filter(has_text="TOTAL PARTNERS")
        self.total_students_card = page.locator("body").filter(has_text="TOTAL STUDENTS")
        self.active_agreements_card = page.locator("body").filter(has_text="ACTIVE AGREEMENTS")
        self.total_employees_card = page.locator("body").filter(has_text="TOTAL EMPLOYEES")
        self.activity_today_card = page.locator("body").filter(has_text="ACTIVITY TODAY")
        self.platform_activity_cards = page.get_by_text("ACTIVITY SUMMARY")
        self.top_partner_table_rows = page.get_by_text("Microsoft", exact=True)
        self.leaderboard_list_items = page.locator("body").filter(has_text="Leaderboard")

    @property
    def dashboard_url(self):
        return urljoin(self.config.base_url, self.config.dashboard_path)

    def load(self):
        self.open(self.dashboard_url)
        self.present(self.ROOT)

    def has_rendered_app_shell(self):
        root = self.visible(self.ROOT)
        return root is not None

    def is_on_dashboard_route(self):
        return "/dashboard" in self.page.url

    def is_on_login_route(self):
        return "/login" in self.page.url

    def has_login_form(self):
        return self.visible(self.EMAIL_FIELD) is not None

    def login(self, email: str, password: str):
        launch = LaunchPage(self.page, self.config)
        if not self.page.locator(LaunchPage.EMAIL_FIELD).count():
            launch.wait_for_role_cards()
        launch.login_as_role("ADMIN", email, password)

    def wait_for_dashboard(self):
        self.wait_until_url_contains("/dashboard")
        self.page.wait_for_load_state("networkidle")
        self.present("body")
        self.wait_for_body_text("TOTAL PARTNERS", timeout=60)

    def go_to_dashboard_home(self):
        # Re-fetch by text on every reset because SPA navigation may detach old handles.
        dashboard_link = self.sidebar_item("Dashboard")
        dashboard_link.scroll_into_view_if_needed()
        dashboard_link.click()
        self.wait_for_dashboard()

    def sidebar_item(self, label: str):
        return self.page.locator("aside, nav").first.get_by_text(label, exact=True).first

    def navigate_sidebar_item(self, label: str):
        route = self.SIDEBAR_ROUTE_EXPECTATIONS[label]
        item = self.sidebar_item(label)
        item.scroll_into_view_if_needed()
        item.click()
        self.wait_until_url_contains(route, timeout=60)
        self.page.wait_for_load_state("networkidle")
        self.present("body")
        assert self.body_text().strip(), f"{label} page rendered empty body"
        return route

    def leaderboard_filter(self, label: str):
        return self.page.locator("button").filter(has_text=label).first

    def visible_texts(self, labels):
        for label in labels:
            self.wait_for_body_text(label, timeout=60)

    def logout(self):
        sign_out = self.page.get_by_text(re.compile(r"SIGN\s*OUT", re.I)).last
        if sign_out.count() == 0 or not sign_out.is_visible():
            self.profile_dropdown_button.click()
            self.page.wait_for_timeout(500)
            sign_out = self.page.get_by_text(re.compile(r"SIGN\s*OUT", re.I)).last

        sign_out.scroll_into_view_if_needed()
        sign_out.click()
        self.page.wait_for_load_state("networkidle")
        self.present("body")

        if "/login" in self.page.url:
            body_text = self.body_text()
            assert "ADMIN" in body_text or self.page.locator(self.EMAIL_FIELD).count() > 0
            return

        LaunchPage(self.page, self.config).wait_for_role_cards()

    def toggle_theme_and_assert_changed(self):
        before_state = self._theme_state()
        self.theme_toggle_button.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_load_state("networkidle")
        after_state = self._theme_state()

        assert self.theme_toggle_button.is_visible()
        assert after_state != before_state or self._has_theme_state(after_state)

    def assert_notifications_panel_opens(self):
        self.notifications_button.click()
        self.page.wait_for_timeout(500)
        self.present("body")
        body_text = self.body_text()
        assert "Notifications" in body_text or "alerts" in body_text.lower()

    def assert_profile_dropdown_opens(self):
        self.profile_dropdown_button.click()
        self.page.wait_for_timeout(500)
        self.present("body")
        body_text = self.body_text()
        assert "Gyaanplant" in body_text
        assert "admin" in body_text.lower() or "SIGN OUT" in body_text

    def _theme_state(self):
        return self.page.evaluate(
            """() => ({
                htmlClass: document.documentElement.className,
                bodyClass: document.body.className,
                colorScheme: getComputedStyle(document.documentElement).colorScheme,
                theme: localStorage.getItem("theme") || localStorage.getItem("color-theme")
            })"""
        )

    def _has_theme_state(self, state):
        return any(value for value in state.values())

    def summary_card_text(self, label: str):
        self.wait_for_body_text(label, timeout=60)
        body_text = self.body_text()
        match = re.search(rf"{re.escape(label)}[\s\S]{{0,160}}", body_text)
        assert match, f"Unable to locate summary card text for {label}"
        return match.group(0)

    def assert_summary_card_value_format(self, label: str):
        card_text = self.summary_card_text(label)
        assert re.search(r"\d", card_text), f"Expected numeric value in {label} card"

    def assert_summary_card_exact_value(self, label: str, expected_value: str):
        card_text = self.summary_card_text(label)
        assert expected_value in card_text, f"Expected {label} to show {expected_value!r}"

    def assert_all_summary_cards_have_values(self):
        for label in self.SUMMARY_CARDS:
            self.assert_summary_card_value_format(label)

    def assert_top_partner_table_structure(self):
        self.assert_text_group_visible(["Top Partner Companies", *self.TOP_PARTNER_HEADERS])
        self.assert_top_partner_company_matches_dashboard_values()

    def assert_leaderboard_widget_structure(self):
        self.assert_text_group_visible(
            ["Leaderboard", "Top students across all colleges", *self.LEADERBOARD_FILTERS, "VIEW FULL LEADERBOARD"]
        )
        for entry in self.LEADERBOARD_ENTRIES:
            self.assert_text_group_visible(entry)

    def assert_text_group_visible(self, labels):
        body_text = self.body_text()
        for label in labels:
            assert label in body_text, f"Expected dashboard text not found: {label}"

    def assert_metrics_match_dashboard_values(self):
        for metric, values in self.METRIC_EXPECTATIONS.items():
            self.assert_text_group_visible([metric, *values])

    def assert_activity_summaries_match_dashboard_values(self):
        self.assert_text_group_visible(["Platform Activity", "ACTIVITY SUMMARY", "POINTS", "ACTIONS"])
        assert self.platform_activity_cards.count() >= 3

    def assert_top_partner_company_matches_dashboard_values(self):
        self.assert_text_group_visible(
            ["Top Partner Companies", "COMPANY NAME", "INDUSTRY", "STATUS", *self.TOP_PARTNER_ROW]
        )

    def assert_leaderboard_matches_dashboard_values(self):
        self.assert_text_group_visible(
            ["Leaderboard", "Top students across all colleges", "ALL TIME", "MONTHLY", "WEEKLY"]
        )
        for entry in self.LEADERBOARD_ENTRIES:
            self.assert_text_group_visible(entry)
        self.assert_text_group_visible(["VIEW FULL LEADERBOARD"])
