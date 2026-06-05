from urllib.parse import urljoin

from pages.web.dashboard_page import DashboardPage


class AdminModulesPage(DashboardPage):
    MODULE_ROUTES = {
        "Analytics": "/analytics/",
        "Organizations": "/organizations/",
        "Courses": "/courses/",
        "Problems": "/problems/",
        "Career Paths": "/career-paths/",
        "Users": "/users/",
        "Prep Packs": "/prep-packs/",
        "Job Details": "/job-details/",
        "Revenue": "/revenue/",
        "Payments": "/payments/",
        "MOU Pipeline": "/mou-pipeline/",
        "Notifications": "/notifications/",
        "Settings": "/settings/",
    }

    def open_module(self, module_name: str):
        route = self.MODULE_ROUTES[module_name]
        self.open(urljoin(self.config.base_url, route))
        self.wait_until_url_contains(route.rstrip("/"), timeout=60)
        self.page.wait_for_load_state("networkidle")
        self.present("body")

    def assert_current_module_url(self, module_name: str):
        route = self.MODULE_ROUTES[module_name].rstrip("/")
        assert route in self.page.url

    def assert_module_texts(self, module_name: str, expected_texts):
        self.assert_current_module_url(module_name)
        self.assert_text_group_visible(expected_texts)

    def assert_table_row_count_at_least(self, minimum: int):
        assert self.page.locator("table tbody tr").count() >= minimum

    def assert_404_module(self, module_name: str):
        self.assert_module_texts(
            module_name,
            ["404", "Lost in Space?", "Back to Dashboard", "Go Back to Safety"],
        )
