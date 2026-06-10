from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.web.dashboard_page import DashboardPage
from utils.web_test_data import OrganizationFormData, WebTestDataFactory


class OrganizationsPage(DashboardPage):
    ADD_COMPANY_BUTTON = "button:has-text('ADD COMPANY')"
    SEARCH_INPUT = "input[placeholder='Search organizations...']"
    SEARCH_BUTTON = "button:has-text('SEARCH')"
    ESTABLISH_PARTNERSHIP_BUTTON = "button:has-text('Establish Partnership')"
    UPDATE_PARTNERSHIP_BUTTON = "button:has-text('Update Partner Record')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    AUTOMATION_PREFIX = "AUTO_TEST_COMPANY_"
    EXPECTED_COMPANY_ROW = {
        "Microsoft": [
            "microsoft@mailinator.com",
            "IT",
            "MNC",
            "Hyderabad, Telangana",
            "Active",
        ]
    }
    ADD_COMPANY_FORM_LABELS = [
        "REGISTER NEW PARTNER",
        "ORGANIZATION NAME *",
        "INDUSTRY *",
        "TYPE *",
        "EMAIL *",
        "PASSWORD *",
        "PHONE",
        "WEBSITE",
        "COUNTRY *",
        "STATE/PROVINCE",
        "CITY *",
        "MOU STATUS *",
        "SUBSCRIPTION *",
    ]

    def navigate_to(self):
        self.open(urljoin(self.config.base_url, "/organizations/"))
        self.wait_for_organizations()

    def wait_for_organizations(self):
        self.wait_until_url_contains("/organizations")
        self.page.wait_for_load_state("networkidle")
        self.wait_for_body_text("ADD COMPANY", timeout=60)
        self.wait_for_body_text("partners", timeout=60)

    def generate_unique_company_name(self):
        return WebTestDataFactory(self.AUTOMATION_PREFIX.rstrip("_")).entity("company").name

    def generate_organization_form_data(self):
        return WebTestDataFactory(self.AUTOMATION_PREFIX.rstrip("_")).organization()

    def automation_email_for(self, company_name: str):
        suffix = company_name.lower().replace("_", ".")
        return f"{suffix}@mailinator.com"

    def company_row(self, company_name: str):
        return self.page.locator("table tbody tr").filter(has_text=company_name).first

    def search_company(self, company_name: str):
        self.type(self.SEARCH_INPUT, company_name)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def assert_organizations_page_loaded(self):
        self.assert_text_group_visible(
            [
                "Organizations",
                "partner companies",
                "ADD COMPANY",
                "ORGANIZATION",
                "INDUSTRY / TYPE",
                "LOCATION",
                "MOU STATUS",
                "ACTIONS",
            ]
        )
        assert self.page.locator("table tbody tr").count() >= 1

    def assert_expected_company_rows_visible(self):
        for company_name, expected_values in self.EXPECTED_COMPANY_ROW.items():
            row_text = self.company_row(company_name).inner_text()
            for value in [company_name, *expected_values]:
                assert value in row_text, f"Expected {value} in {company_name} row"

    def assert_add_company_form_ready(self):
        self.open_add_company_modal()
        self.assert_text_group_visible(self.ADD_COMPANY_FORM_LABELS)
        assert self.visible("input[placeholder='Enter organization name']").is_visible()
        assert self.visible("input[placeholder='••••••••']").is_visible()
        assert self.visible("input[placeholder='https://...']").is_visible()
        assert self.page.get_by_text("Establish Partnership", exact=True).is_visible()
        self.click(self.CANCEL_BUTTON)

    def open_add_company_modal(self):
        self.click(self.ADD_COMPANY_BUTTON)
        self.wait_for_body_text("REGISTER NEW PARTNER")

    def fill_company_form(
        self,
        name: str,
        city: str = "Hyderabad",
        state: str = "Telangana",
        industry: str = "IT",
        company_type: str = "Startup",
        email: str | None = None,
        password: str = "Auto@12345",
        phone: str = "9999999999",
        website: str = "https://automation.example.com",
        address: str = "Automation company address",
        mou_status: str = "Active",
        subscription: str = "Basic",
    ):
        inputs = self.page.locator("input")
        selects = self.page.locator("select")
        email = email or self.automation_email_for(name)

        inputs.nth(2).fill(name)
        selects.nth(2).select_option(label=industry)
        selects.nth(3).select_option(label=company_type)
        inputs.nth(3).fill(email)
        inputs.nth(4).fill(password)
        inputs.nth(5).fill(phone)
        inputs.nth(6).fill(website)
        self._select_form_option("Select Country", "India")
        self._select_form_option("Select State", state)
        self._select_form_option("Select City", city)

    def _select_form_option(self, placeholder_text: str, label: str):
        select = self.page.locator("select").filter(has_text=placeholder_text).first
        if select.count():
            select.select_option(label=label)
            return

        trigger = self.page.get_by_text(placeholder_text, exact=False).last
        trigger.click()
        option = self.page.get_by_text(label, exact=True).last
        option.click()

    def create_company(self, name: str, city: str = "Hyderabad"):
        self.open_add_company_modal()
        self.fill_company_form(name=name, city=city)
        self.click(self.ESTABLISH_PARTNERSHIP_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_company(name)
        self.wait_for_body_text(name, timeout=60)

    def create_company_from_data(self, data: OrganizationFormData):
        self.open_add_company_modal()
        self.fill_company_form(
            name=data.name,
            city=data.city,
            state=data.state,
            industry=data.industry,
            company_type=data.company_type,
            email=data.email,
            password=data.password,
            phone=data.phone,
            website=data.website,
            address=data.address,
            subscription=data.subscription,
            mou_status=data.mou_status,
        )
        self.click(self.ESTABLISH_PARTNERSHIP_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.search_company(data.name)
        self.wait_for_body_text(data.name, timeout=60)

    def assert_company_row_matches_form_data(self, data: OrganizationFormData):
        self.search_company(data.name)
        row_text = self.company_row(data.name).inner_text()
        expected_values = [
            data.name,
            data.email,
            data.industry,
            data.company_type,
            data.city,
            data.mou_status,
        ]
        for value in expected_values:
            assert value in row_text, f"Expected created organization row to contain {value!r}"

    def company_exists(self, name: str):
        self.search_company(name)
        return self.company_row(name).count() > 0 and self.company_row(name).is_visible()

    def edit_company_city(self, name: str, new_city: str):
        self.search_company(name)
        row = self.company_row(name)
        row.locator("button").nth(0).click()
        self.wait_for_body_text("EDIT")
        self.page.locator("input").nth(7).fill(new_city)
        update_button = self.page.get_by_text("Update Partner Record", exact=True)
        if update_button.count() == 0:
            update_button = self.page.get_by_text("Update", exact=False)
        update_button.first.click()
        self.page.wait_for_load_state("networkidle")
        self.search_company(name)
        self.wait_for_body_text(new_city, timeout=60)

    def delete_company_if_present(self, name: str):
        self.navigate_to()
        self.search_company(name)
        row = self.company_row(name)
        if row.count() == 0 or not row.is_visible():
            return False

        delete_button = row.locator(
            "button[title='Delete Record'], button[aria-label*='delete' i], button[title*='Delete' i]"
        ).first
        if delete_button.count() == 0:
            delete_button = row.locator("button").last

        self.page.once("dialog", lambda dialog: dialog.accept())
        delete_button.click()
        self.page.wait_for_timeout(500)
        for label in ("Delete", "Confirm", "Yes", "Remove"):
            confirm = self.page.get_by_text(label, exact=True)
            if confirm.count() and confirm.first.is_visible():
                confirm.first.click()
                break

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)
        self.search_company(name)
        try:
            self.company_row(name).wait_for(state="hidden", timeout=5000)
        except PlaywrightTimeoutError:
            pass
        if self.company_row(name).count() == 0 or not self.company_row(name).is_visible():
            return True

        row_text = self.company_row(name).inner_text()
        return "Expired" in row_text
