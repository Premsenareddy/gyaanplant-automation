from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.web.dashboard_page import DashboardPage
from utils.web_test_data import CollegeFormData, WebTestDataFactory


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
        "COUNTRY *",
        "STATE *",
        "TYPE",
        "NAAC GRADE *",
        "TOTAL STUDENTS *",
        "PLACEMENT %",
        "EMAIL *",
        "PASSWORD *",
        "PHONE",
        "WEBSITE URL",
        "CITY *",
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
        assert self.page.locator("select").count() >= 4
        assert self.page.get_by_text("Deploy Institution", exact=True).is_visible()

    def generate_unique_college_name(self):
        return WebTestDataFactory(self.AUTOMATION_PREFIX.rstrip("_")).entity("college").name

    def generate_college_form_data(self):
        return WebTestDataFactory(self.AUTOMATION_PREFIX.rstrip("_")).college()

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
        email = email or self.automation_email_for(name)

        inputs.nth(2).fill(name)
        self._select_form_option("Select Country", "India")
        self._select_form_option("Select State", state)
        self._select_form_option("Select Type", college_type)
        self._select_form_option("Select Grade", naac_grade)
        inputs.nth(3).fill(total_students)
        inputs.nth(4).fill(placement_percent)
        inputs.nth(5).fill(email)
        inputs.nth(6).fill(password)
        inputs.nth(7).fill(phone)
        inputs.nth(8).fill(website)
        self._select_form_option("Select City", city)
        self._select_form_option("Select Tier", subscription)
        self._select_form_option("Select Status", mou_status)

    def _select_form_option(self, placeholder_text: str, label: str):
        select = self.page.locator("select").filter(has_text=placeholder_text).first
        if select.count():
            select.select_option(label=label)
            return

        trigger = self.page.get_by_text(placeholder_text, exact=False).last
        trigger.click()
        option = self.page.get_by_text(label, exact=True).last
        option.click()

    def create_college(self, name: str, city: str = "Hyderabad"):
        self.open_add_college_modal()
        self.fill_college_form(name=name, city=city)
        self.click(self.DEPLOY_INSTITUTION_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_college(name)
        self.wait_for_body_text(name, timeout=60)

    def create_college_from_data(self, data: CollegeFormData):
        self.open_add_college_modal()
        self.fill_college_form(
            name=data.name,
            city=data.city,
            state=data.state,
            college_type=data.college_type,
            naac_grade=data.naac_grade,
            total_students=data.total_students,
            placement_percent=data.placement_percent,
            email=data.email,
            password=data.password,
            phone=data.phone,
            website=data.website,
            address=data.address,
            subscription=data.subscription,
            mou_status=data.mou_status,
        )
        self.click(self.DEPLOY_INSTITUTION_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_college(data.name)
        self.wait_for_body_text(data.name, timeout=60)

    def assert_college_row_matches_form_data(self, data: CollegeFormData):
        self.search_college(data.name)
        row_text = self.college_row(data.name).inner_text()
        expected_values = [
            data.name,
            data.email,
            data.city,
            data.total_students,
            data.naac_grade,
            data.placement_percent,
            data.mou_status,
        ]
        for value in expected_values:
            assert value in row_text, f"Expected created college row to contain {value!r}"

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
