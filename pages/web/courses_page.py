from urllib.parse import urljoin
import re

from pages.web.dashboard_page import DashboardPage
from utils.web_test_data import WebTestDataFactory


class CoursesPage(DashboardPage):
    ADD_COURSE_BUTTON = "button:has-text('Add Course')"
    SEARCH_INPUT = "input[placeholder='Search courses, skills, or paths...']"
    APPLY_SEARCH_BUTTON = "button:has-text('Apply Search')"
    LAUNCH_COURSE_BUTTON = "button:has-text('Launch Course')"
    AUTOMATION_PREFIX = "AUTO_TEST_COURSE_"
    ADD_COURSE_FORM_LABELS = [
        "ADD NEW COURSE",
        "COURSE TITLE",
        "DESCRIPTION",
        "COURSE THUMBNAIL",
        "UPLOAD IMAGE",
        "COURSE METADATA",
        "CATEGORY",
        "AUDIENCE",
        "LEVEL",
        "LANGUAGE",
        "PRICE",
        "PASSING SCORE (%)",
        "MANDATORY",
        "PUBLISHED",
        "PREMIUM COURSE",
        "TARGET CAREER PATHS",
        "MODULES",
        "COURSE CURRICULUM (0 SECTIONS)",
        "ADD SECTION",
        "Launch Course",
    ]
    PAGE_TEXTS = [
        "Course Management",
        "Manage curriculum, course assignments, and academic learning resources",
        "Add Course",
        "Apply Search",
    ]
    COURSE_CARD_TEXTS = ["BEGINNER", "VIEW CONTENT"]
    EXPECTED_COURSES = {
        "Node.js Backend Development": ["Node.js Backend Development", "BEGINNER", "VIEW CONTENT"],
        "React.js Development": ["React.js Development", "BEGINNER", "VIEW CONTENT"],
        "Python Programming": ["Python Programming", "BEGINNER", "VIEW CONTENT"],
    }

    def navigate_to(self):
        self.open(urljoin(self.config.base_url, "/courses/"))
        self.wait_for_courses()

    def wait_for_courses(self):
        self.wait_until_url_contains("/courses")
        self.page.wait_for_load_state("networkidle")
        self.wait_for_body_text("Course Management", timeout=60)
        self.wait_for_body_text("Add Course", timeout=60)

    def generate_unique_course_title(self):
        return WebTestDataFactory(self.AUTOMATION_PREFIX.rstrip("_")).entity("course").name

    def open_add_course_modal(self):
        self.click(self.ADD_COURSE_BUTTON)
        self.wait_for_body_text("ADD NEW COURSE")

    def has_visible_delete_cleanup_action(self):
        body_text = self.body_text()
        return "Delete Course" in body_text or "Remove Course" in body_text

    def search_course(self, course_title: str):
        self.type(self.SEARCH_INPUT, course_title)
        self.click(self.APPLY_SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def assert_courses_page_loaded(self):
        self.assert_text_group_visible([*self.PAGE_TEXTS, *self.COURSE_CARD_TEXTS])

    def assert_search_controls_ready(self):
        assert self.visible(self.SEARCH_INPUT).is_visible()
        assert self.page.get_by_text("Apply Search", exact=True).is_visible()

    def course_card(self, course_title: str):
        return self.page.locator("body").filter(has_text=course_title).first

    def assert_course_card_contains(self, course_title: str, expected_values):
        self.search_course(course_title)
        body_text = self.body_text()
        for value in expected_values:
            assert value in body_text, f"Expected course card/search result to include {value!r}"

    def assert_course_actions_available(self):
        body_text = self.body_text()
        assert "VIEW CONTENT" in body_text
        assert self.page.get_by_text(re.compile(r"VIEW\s+CONTENT", re.I)).count() >= 1

    def assert_expected_courses_visible(self):
        for expected_values in self.EXPECTED_COURSES.values():
            self.assert_text_group_visible(expected_values)

    def assert_add_course_form_ready(self):
        self.open_add_course_modal()
        self.assert_text_group_visible(self.ADD_COURSE_FORM_LABELS)
        assert self.visible("input[placeholder='e.g. Advanced JavaScript Mastery']").is_visible()
        assert self.visible("textarea[placeholder='Describe what students will learn...']").is_visible()
        assert self.visible("input[placeholder='Search paths...']").is_visible()
        assert self.page.locator("select").count() >= 3
        assert self.page.get_by_text("Launch Course", exact=True).is_visible()
        self.click("button:has-text('Cancel')")
