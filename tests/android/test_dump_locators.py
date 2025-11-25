import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


def test_dump_locators(android_driver):
    time.sleep(2)  # allow screen to settle

    elements = android_driver.find_elements(By.XPATH, "//*")

    print("\n================= LOCATOR DUMP =================\n")

    unique = set()

    for el in elements:
        try:
            aid = el.get_attribute("content-desc")
            text = el.get_attribute("text")
            rid = el.get_attribute("resource-id")
            cls = el.get_attribute("className")

            if aid:
                unique.add(f'ACCESSIBILITY_ID: "{aid}"')
            if text:
                unique.add(f'TEXT: "{text}"')
            if rid:
                unique.add(f'ID: "{rid}"')
            if cls and not aid and not text:
                # fallback class locators
                unique.add(f'CLASS: "{cls}"')
        except Exception:
            pass

    for item in sorted(unique):
        print(item)

    print("\n=================================================\n")

