from urllib.parse import urljoin

from config.settings import WebConfig
from pages.web.base_page import BaseWebPage


class LaunchPage(BaseWebPage):
    ROOT = "#root"
    ROLE_LABELS = ["STUDENT", "MENTOR", "HOD", "COLLEGE", "TPO", "ADMIN"]
    EMAIL_FIELD = "input[type='email'], input[name*='email' i], input[placeholder*='email' i]"
    PASSWORD_FIELD = "input[type='password'], input[name*='password' i], input[placeholder*='password' i]"
    SUBMIT_BUTTON = "button:has-text('Login to Dashboard')"

    def __init__(self, page, config: WebConfig | None = None):
        super().__init__(page)
        self.config = config or WebConfig()

    @property
    def login_url(self):
        return urljoin(self.config.base_url, "/login/")

    def load(self):
        self.open(self.login_url)
        self.present(self.ROOT)
        self.page.wait_for_load_state("domcontentloaded")
        self.wait_for_role_cards()

    def select_role(self, role_label: str):
        self.page.locator("button").filter(has_text=role_label.upper()).click(
            timeout=self.config.timeout_ms,
        )
        self.wait_for_body_text("LOGGING IN AS", timeout=20)

    def has_role_cards(self):
        body_text = self.body_text()
        return all(role in body_text for role in self.ROLE_LABELS)

    def wait_for_role_cards(self):
        for role_label in self.ROLE_LABELS:
            self.wait_for_body_text(role_label)
        return True

    def login_as_role(self, role_label: str, email: str, password: str):
        if not self.page.locator(self.EMAIL_FIELD).count():
            self.select_role(role_label)
        self.type(self.EMAIL_FIELD, email)
        self.type(self.PASSWORD_FIELD, password)
        submit_button = self.visible(self.SUBMIT_BUTTON)
        try:
            submit_button.click(timeout=10000, force=True)
        except Exception:
            submit_button.dispatch_event("click")
        self.page.wait_for_timeout(500)
        if self.page.locator(self.SUBMIT_BUTTON).count():
            self.page.locator(self.SUBMIT_BUTTON).first.click(force=True)
            self.page.keyboard.press("Enter")
