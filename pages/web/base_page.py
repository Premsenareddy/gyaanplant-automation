from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

DEFAULT_TIMEOUT = 20


class BaseWebPage:
    def __init__(self, page):
        self.page = page

    def by_test_id(self, test_id: str):
        return self.page.get_by_test_id(test_id)

    def visible_by_test_id(self, test_id: str, timeout=DEFAULT_TIMEOUT):
        element = self.by_test_id(test_id).first
        element.wait_for(state="visible", timeout=timeout * 1000)
        return element

    def click_by_test_id(self, test_id: str, timeout=DEFAULT_TIMEOUT):
        element = self.visible_by_test_id(test_id, timeout)
        element.click()
        return element

    def type_by_test_id(self, test_id: str, text, timeout=DEFAULT_TIMEOUT, clear=True):
        element = self.visible_by_test_id(test_id, timeout)
        if clear:
            element.fill("")
        element.fill(text)
        return element

    def open(self, url: str):
        try:
            self.page.goto(url, wait_until="domcontentloaded")
        except PlaywrightTimeoutError:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def visible(self, locator: str, timeout=DEFAULT_TIMEOUT):
        element = self.page.locator(locator).first
        element.wait_for(state="visible", timeout=timeout * 1000)
        return element

    def present(self, locator: str, timeout=DEFAULT_TIMEOUT):
        element = self.page.locator(locator).first
        element.wait_for(state="attached", timeout=timeout * 1000)
        return element

    def click(self, locator: str, timeout=DEFAULT_TIMEOUT):
        element = self.visible(locator, timeout)
        element.click()
        return element

    def type(self, locator: str, text, timeout=DEFAULT_TIMEOUT, clear=True):
        element = self.visible(locator, timeout)
        if clear:
            element.fill("")
        element.fill(text)
        return element

    def wait_until_url_contains(self, text: str, timeout=DEFAULT_TIMEOUT):
        self.page.wait_for_url(f"**{text}**", timeout=timeout * 1000)

    def text_visible(self, text: str, timeout=DEFAULT_TIMEOUT):
        element = self.page.get_by_text(text, exact=True).first
        element.wait_for(state="visible", timeout=timeout * 1000)
        return element

    def body_text(self):
        return self.page.locator("body").inner_text()

    def wait_for_body_text(self, text: str, timeout=DEFAULT_TIMEOUT):
        timeout_ms = timeout * 1000
        interval_ms = 250
        elapsed_ms = 0

        while elapsed_ms <= timeout_ms:
            if text in self.body_text():
                return True
            self.page.wait_for_timeout(interval_ms)
            elapsed_ms += interval_ms

        raise AssertionError(f"Expected text not found on page: {text}")
