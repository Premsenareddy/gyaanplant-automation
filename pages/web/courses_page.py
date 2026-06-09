import time
from urllib.parse import urljoin

from pages.web.dashboard_page import DashboardPage


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

    def navigate_to(self):
        self.open(urljoin(self.config.base_url, "/courses/"))
        self.wait_for_courses()

    def wait_for_courses(self):
        self.wait_until_url_contains("/courses")
        self.page.wait_for_load_state("networkidle")
        self.wait_for_body_text("Course Management", timeout=60)
        self.wait_for_body_text("Add Course", timeout=60)

    def generate_unique_course_title(self):
        return f"{self.AUTOMATION_PREFIX}{int(time.time())}"

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
        self.assert_text_group_visible(
            [
                "Course Management",
                "Manage curriculum, course assignments, and academic learning resources",
                "Add Course",
                "Apply Search",
                "Rust",
                "Rust programming",
                "BEGINNER",
                "VIEW CONTENT",
            ]
        )

    def assert_add_course_form_ready(self):
        self.open_add_course_modal()
        self.assert_text_group_visible(self.ADD_COURSE_FORM_LABELS)
        assert self.visible("input[placeholder='e.g. Advanced JavaScript Mastery']").is_visible()
        assert self.visible("textarea[placeholder='Describe what students will learn...']").is_visible()
        assert self.visible("input[placeholder='Search paths...']").is_visible()
        assert self.page.get_by_text("Launch Course", exact=True).is_visible()
        self.click("button:has-text('Cancel')")
