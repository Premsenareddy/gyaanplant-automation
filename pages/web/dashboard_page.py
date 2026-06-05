from urllib.parse import urljoin
from typing import Optional

from config.settings import WebConfig
from pages.web.base_page import BaseWebPage


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
    METRIC_EXPECTATIONS = {
        "TOTAL PARTNERS": ["4", "Colleges: 4"],
        "TOTAL STUDENTS": ["25", "Global Student Reach"],
        "ACTIVE AGREEMENTS": ["1", "Total Orgs: 0"],
        "TOTAL EMPLOYEES": ["0", "Company Network"],
        "ACTIVITY TODAY": ["29", "785 Points earned", "Platform Activity"],
    }
    ACTIVITY_SUMMARIES = [
        ["28", "MAY 28, 2026", "ACTIVITY SUMMARY", "POINTS", "+785", "ACTIONS", "29"],
        ["29", "MAY 29, 2026", "ACTIVITY SUMMARY", "POINTS", "+105", "ACTIONS", "12"],
        ["30", "MAY 30, 2026", "ACTIVITY SUMMARY", "POINTS", "+50", "ACTIONS", "10"],
    ]
    TOP_PARTNER_ROW = ["Microsoft", "IT", "ACTIVE"]
    LEADERBOARD_ENTRIES = [
        ["01", "GYAANPLANT", "LVL 1", "65", "POINTS"],
        ["02", "ADA", "LVL 1", "65", "POINTS"],
        ["03", "RISHIK", "LVL 1", "60", "POINTS"],
        ["04", "PERSON1", "LVL 1", "55", "POINTS"],
        ["05", "SAGAR", "LVL 1", "55", "POINTS"],
    ]

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
        self.type(self.EMAIL_FIELD, email)
        self.type(self.PASSWORD_FIELD, password)
        submit_button = self.visible(self.SUBMIT_BUTTON)
        try:
            submit_button.click(timeout=10000, force=True)
        except Exception:
            submit_button.dispatch_event("click")
        self.page.wait_for_timeout(500)
        if "/login" in self.page.url and self.page.locator(self.SUBMIT_BUTTON).count():
            self.page.locator(self.SUBMIT_BUTTON).first.click(force=True)
            self.page.keyboard.press("Enter")

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

    def leaderboard_filter(self, label: str):
        return self.page.locator("button").filter(has_text=label).first

    def visible_texts(self, labels):
        for label in labels:
            self.wait_for_body_text(label, timeout=60)

    def assert_text_group_visible(self, labels):
        body_text = self.body_text()
        for label in labels:
            assert label in body_text, f"Expected dashboard text not found: {label}"

    def assert_metrics_match_dashboard_values(self):
        for metric, values in self.METRIC_EXPECTATIONS.items():
            self.assert_text_group_visible([metric, *values])

    def assert_activity_summaries_match_dashboard_values(self):
        for summary in self.ACTIVITY_SUMMARIES:
            self.assert_text_group_visible(summary)

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
