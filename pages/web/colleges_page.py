import time
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.web.dashboard_page import DashboardPage


class CollegesPage(DashboardPage):
    PAGE_TITLE = "Colleges"
    ADD_COLLEGE_BUTTON = "button:has-text('ADD COLLEGE')"
    SEARCH_INPUT = "input[placeholder='Search colleges...']"
    CITY_FILTER_INPUT = "input[placeholder='Filter City...']"
    TYPE_FILTER_SELECT = "select"
    SEARCH_BUTTON = "button:has-text('SEARCH')"
    APPLY_BUTTON = "button:has-text('APPLY')"
    COLLEGES_TABLE = "table"
    ADD_COLLEGE_MODAL_TITLE = "ADD NEW COLLEGE"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    DEPLOY_INSTITUTION_BUTTON = "button:has-text('Deploy Institution')"
    UPDATE_INSTITUTION_BUTTON = "button:has-text('Update Institutional Record')"
    AUTOMATION_PREFIX = "AUTO_TEST_COLLEGE_"

    EXPECTED_COLLEGE_ROWS = {
        "BITS": ["bits@mailinator.com", "hyderabad", "Active", "200000", "A++", "90%"],
        "CMR": ["cmr@mailinator.com", "Hyderabad", "Active", "55000", "A++", "65%"],
        "sagar": ["sagar@mailinator.com", "Fugiat repudiandae v", "Active", "52", "Not Accredited", "60%"],
        "MVSR": ["mvsr@mailinator.com", "Hyderabad", "Active", "1000", "A++", "80%"],
    }
    ADD_COLLEGE_FORM_LABELS = [
        "COLLEGE NAME *",
        "CITY *",
        "STATE",
        "TYPE",
        "NAAC GRADE *",
        "TOTAL STUDENTS *",
        "PLACEMENT %",
        "EMAIL *",
        "PASSWORD *",
        "PHONE",
        "WEBSITE URL",
        "FULL ADDRESS",
        "SUBSCRIPTION *",
        "MOU STATUS *",
    ]

    def open_colleges(self):
        item = self.sidebar_item("Colleges")
        item.scroll_into_view_if_needed()
        item.click()
        self.wait_for_colleges()

    def navigate_to(self):
        self.open(urljoin(self.config.base_url, "/colleges/"))
        self.wait_for_colleges()

    def wait_for_colleges(self):
        self.wait_until_url_contains("/colleges")
        self.page.wait_for_load_state("networkidle")
        self.wait_for_body_text("ADD COLLEGE", timeout=60)
        self.wait_for_body_text("Showing", timeout=60)
        self.wait_for_body_text("institutions", timeout=60)

    def table_rows(self):
        return self.page.locator(f"{self.COLLEGES_TABLE} tbody tr")

    def college_row(self, college_name: str):
        return self.table_rows().filter(has_text=college_name).first

    def assert_colleges_page_loaded(self):
        self.assert_text_group_visible(
            [
                "Colleges",
                "4 colleges",
                "ADD COLLEGE",
                "COLLEGE",
                "LOCATION",
                "STATUS",
                "STUDENTS",
                "NAAC",
                "PLACEMENT",
                "ACTIONS",
            ]
        )
        assert self.table_rows().count() >= 4

    def assert_expected_college_rows_visible(self):
        for college_name, expected_values in self.EXPECTED_COLLEGE_ROWS.items():
            row_text = self.college_row(college_name).inner_text()
            for value in [college_name, *expected_values]:
                assert value in row_text, f"Expected {value} in {college_name} row"

    def search_college(self, search_text: str):
        self.type(self.SEARCH_INPUT, search_text)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def filter_city(self, city: str):
        self.type(self.CITY_FILTER_INPUT, city)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def select_type_filter(self, college_type: str):
        self.page.locator(self.TYPE_FILTER_SELECT).first.select_option(label=college_type)
        self.click(self.APPLY_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def open_add_college_modal(self):
        self.click(self.ADD_COLLEGE_BUTTON)
        self.wait_for_body_text(self.ADD_COLLEGE_MODAL_TITLE)

    def close_add_college_modal(self):
        self.click(self.CANCEL_BUTTON)
        self.page.get_by_text(self.ADD_COLLEGE_MODAL_TITLE, exact=True).wait_for(state="detached")

    def assert_add_college_form_ready(self):
        self.assert_text_group_visible(self.ADD_COLLEGE_FORM_LABELS)
        assert self.visible("input[placeholder='Institutional Name']").is_visible()
        assert self.visible("input[placeholder='••••••••']").is_visible()
        assert self.visible("input[placeholder='https://...']").is_visible()
        assert self.visible("input[placeholder='Detailed physical address']").is_visible()
        assert self.page.locator("select").count() >= 4
        assert self.page.get_by_text("Deploy Institution", exact=True).is_visible()

    def generate_unique_college_name(self):
        return f"{self.AUTOMATION_PREFIX}{int(time.time())}"

    def automation_email_for(self, college_name: str):
        suffix = college_name.lower().replace("_", ".")
        return f"{suffix}@mailinator.com"

    def fill_college_form(
        self,
        name: str,
        city: str,
        state: str = "Telangana",
        college_type: str = "Engineering",
        naac_grade: str = "A+",
        total_students: str = "123",
        placement_percent: str = "77",
        email: str | None = None,
        password: str = "Auto@12345",
        phone: str = "9999999999",
        website: str = "https://automation.example.com",
        address: str = "Automation test address",
        subscription: str = "Basic",
        mou_status: str = "Active",
    ):
        inputs = self.page.locator("input")
        selects = self.page.locator("select")
        email = email or self.automation_email_for(name)

        inputs.nth(2).fill(name)
        inputs.nth(3).fill(city)
        inputs.nth(4).fill(state)
        selects.nth(1).select_option(label=college_type)
        selects.nth(2).select_option(label=naac_grade)
        inputs.nth(5).fill(total_students)
        inputs.nth(6).fill(placement_percent)
        inputs.nth(7).fill(email)
        inputs.nth(8).fill(password)
        inputs.nth(9).fill(phone)
        inputs.nth(10).fill(website)
        inputs.nth(11).fill(address)
        selects.nth(3).select_option(label=subscription)
        selects.nth(4).select_option(label=mou_status)

    def create_college(self, name: str, city: str = "Hyderabad"):
        self.open_add_college_modal()
        self.fill_college_form(name=name, city=city)
        self.click(self.DEPLOY_INSTITUTION_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_college(name)
        self.wait_for_body_text(name, timeout=60)

    def edit_college_city(self, name: str, new_city: str):
        self.search_college(name)
        row = self.college_row(name)
        row.locator("button[title='Edit Record']").click()
        self.wait_for_body_text("EDIT COLLEGE")
        self.page.locator("input").nth(3).fill(new_city)
        self.click(self.UPDATE_INSTITUTION_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_college(name)
        self.wait_for_body_text(new_city, timeout=60)

    def college_exists(self, name: str):
        self.search_college(name)
        return self.college_row(name).count() > 0 and self.college_row(name).is_visible()

    def delete_college_if_present(self, name: str):
        self.navigate_to()
        self.search_college(name)
        row = self.college_row(name)
        if row.count() == 0 or not row.is_visible():
            return False

        row.locator("button[title='Delete Record']").click()
        self.page.wait_for_timeout(500)

        for label in ("Delete", "Confirm", "Yes", "Remove"):
            confirm = self.page.get_by_text(label, exact=True)
            if confirm.count() and confirm.first.is_visible():
                confirm.first.click()
                break

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)
        self.search_college(name)
        try:
            self.college_row(name).wait_for(state="hidden", timeout=5000)
        except PlaywrightTimeoutError:
            pass
        return not (self.college_row(name).count() > 0 and self.college_row(name).is_visible())
