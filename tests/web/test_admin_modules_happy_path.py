import pytest

from pages.web.admin_modules_page import AdminModulesPage


@pytest.fixture
def admin_modules(authenticated_web_page):
    modules = AdminModulesPage(authenticated_web_page)
    modules.load()
    modules.wait_for_dashboard()
    return modules


@pytest.mark.web
def test_gp_mod_001_analytics_page_displays_system_logic_metrics(admin_modules):
    admin_modules.open_module("Analytics")
    admin_modules.assert_module_texts(
        "Analytics",
        [
            "System Logic",
            "Deep behavioral telemetry",
            "Acquisition Velocity",
            "LIVE FLOW",
            "Feature Metrics",
            "Placement",
            "NAAC Score",
            "Engagement",
        ],
    )


@pytest.mark.web
def test_gp_mod_002_organizations_page_displays_partner_table(admin_modules):
    admin_modules.open_module("Organizations")
    admin_modules.assert_module_texts(
        "Organizations",
        [
            "Organizations",
            "partner companies",
            "ADD COMPANY",
            "ORGANIZATION",
            "INDUSTRY / TYPE",
            "MOU STATUS",
            "Microsoft",
            "microsoft@mailinator.com",
            "IT",
            "MNC",
            "Hyderabad, Telangana",
            "Active",
        ],
    )
    admin_modules.assert_table_row_count_at_least(1)


@pytest.mark.web
def test_gp_mod_003_courses_page_displays_existing_course_card(admin_modules):
    admin_modules.open_module("Courses")
    admin_modules.assert_module_texts(
        "Courses",
        [
            "Course Management",
            "Manage curriculum, course assignments, and academic learning resources",
            "Add Course",
            "Apply Search",
            "₹100",
            "BEGINNER",
            "Node.js Backend Development",
            "React.js Development",
            "Python Programming",
            "VIEW CONTENT",
            "Showing 3 of 3 courses",
        ],
    )


@pytest.mark.web
def test_gp_mod_004_problems_route_shows_not_found_page(admin_modules):
    admin_modules.open_module("Problems")
    admin_modules.assert_404_module("Problems")


@pytest.mark.web
def test_gp_mod_005_career_paths_page_displays_live_path_card(admin_modules):
    admin_modules.open_module("Career Paths")
    admin_modules.assert_module_texts(
        "Career Paths",
        [
            "Career Path Matrix",
            "Manage industry-specialized learning tracks",
            "Add Path",
            "LIVE",
            "MERN FULL STACK DEVELOPER",
            "0 MODULES LINKED",
            "MERN Full Stack Web Developer",
            "#react",
            "#nodejs",
            "#aws",
            "#mongodb",
            "#expressjs",
            "Showing 1 of 1 paths",
        ],
    )


@pytest.mark.web
def test_gp_mod_006_users_page_displays_user_management_table(admin_modules):
    admin_modules.open_module("Users")
    admin_modules.assert_module_texts(
        "Users",
        [
            "Users",
            "Invite User",
            "All Roles",
            "ACADEMIC ROLES",
            "Students",
            "College Admin",
            "CORPORATE ROLES",
            "Employee",
            "HR Manager",
            "USER PARTICIPANT",
            "ASSOCIATED ENTITY",
            "ACCOUNT STATUS",
        ],
    )
    admin_modules.assert_table_row_count_at_least(1)


@pytest.mark.web
def test_gp_mod_007_prep_packs_page_displays_pack_card(admin_modules):
    admin_modules.open_module("Prep Packs")
    admin_modules.assert_module_texts(
        "Prep Packs",
        [
            "Prep Pack Management",
            "Industrial preparation and certification resource manager",
            "Create Pack",
            "PUBLISHED",
            "TCS NQT Ultimate Placement Pre",
            "Node.js Backend Developer Prep",
            "ATTEMPTS",
            "AVG. SCORE",
            "MIXED",
            "STUDENT",
            "₹1000",
            "₹200",
            "TCS",
            "INFOSYS",
            "MANAGE CONTENT",
        ],
    )


@pytest.mark.web
def test_gp_mod_008_job_details_route_shows_not_found_page(admin_modules):
    admin_modules.open_module("Job Details")
    admin_modules.assert_404_module("Job Details")


@pytest.mark.web
def test_gp_mod_009_revenue_page_displays_financial_dashboard(admin_modules):
    admin_modules.open_module("Revenue")
    admin_modules.assert_module_texts(
        "Revenue",
        [
            "Revenue Dashboard",
            "Comprehensive financial performance and regional growth tracking",
            "TOTAL REVENUE",
            "₹0.02L",
            "GROWTH RATE",
            "100%",
            "PENDING INVOICES",
            "AVG TICKET SIZE",
            "Revenue by Geography",
            "Recent Transactions",
            "USER",
            "PRODUCT",
            "AMOUNT",
            "STATUS",
            "CAPTURED",
        ],
    )
    admin_modules.assert_table_row_count_at_least(1)


@pytest.mark.web
def test_gp_mod_010_payments_page_displays_transaction_audit(admin_modules):
    admin_modules.open_module("Payments")
    admin_modules.assert_module_texts(
        "Payments",
        [
            "Global Transactions",
            "Complete financial audit and payment logs",
            "APPLY",
            "Filters",
            "STUDENT PURCHASES",
            "SHOWING 15 OF",
            "RECORDS",
            "LIVE SYNC ACTIVE",
            "USER",
            "PRODUCT",
            "AMOUNT",
            "PAYMENT DETAILS",
            "STATUS",
            "CAPTURED",
        ],
    )
    admin_modules.assert_table_row_count_at_least(1)


@pytest.mark.web
def test_gp_mod_011_mou_pipeline_route_shows_not_found_page(admin_modules):
    admin_modules.open_module("MOU Pipeline")
    admin_modules.assert_404_module("MOU Pipeline")


@pytest.mark.web
def test_gp_mod_012_notifications_page_displays_empty_state(admin_modules):
    admin_modules.open_module("Notifications")
    admin_modules.assert_module_texts(
        "Notifications",
        [
            "Notifications",
            "0 new alerts require your attention",
            "BROADCAST",
            "MARK ALL READ",
            "New Ticket",
            "Join Mission Space",
            "ACKNOWLEDGED",
        ],
    )


@pytest.mark.web
def test_gp_mod_013_settings_page_displays_security_form(admin_modules):
    admin_modules.open_module("Settings")
    admin_modules.assert_module_texts(
        "Settings",
        [
            "Settings",
            "Manage your profile, security, and notification preferences.",
            "SECURITY",
            "NOTIFICATIONS",
            "Change Password",
            "OLD PASSWORD",
            "NEW PASSWORD",
            "CONFIRM PASSWORD",
            "UPDATE PASSWORD",
        ],
    )
    assert admin_modules.page.locator("input[type='password']").count() == 3
