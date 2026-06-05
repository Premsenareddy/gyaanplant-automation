⭐ GyaanPlant Mobile & Web Test Automation Framework












A complete Python Test Automation Framework designed for both Mobile (Android) and Web testing.
This framework is built using PyTest, Appium, Playwright, Page Object Model (POM), Fixtures, and Allure reporting, making it production-ready and portfolio-worthy.

📌 Key Features
✔ Mobile Automation (Appium)

Android application testing

POM-based page layers

Device capabilities from config

Context switching, gestures, waits

✔ Web Automation (Playwright)

Structured web flows

Dynamic waits & reusable actions

✔ Robust Framework Architecture

Page Object Model (POM)

Fixtures-driven test execution

Utilities for logs, waits, test data

Automatic screenshot capture

✔ Reporting

Allure Reports

HTML + XML JUnit output

Screenshots on failure

✔ CI/CD Ready

Can easily plug into GitHub Actions or Jenkins

Supports headless mode

📁 Project Structure
gyaanplant_automation
│
├── app/                 # Appium driver, app utilities
├── config/              # Environment & capability configs
├── core/                # Base classes, driver factory, hooks
├── locators/            # Page-specific locators
├── pages/               # Page Object Model (POM) pages
├── tests/               # UI/Mobile test cases
├── testdata/            # Test input files (JSON, CSV, etc.)
├── utils/               # Helpers: waits, logger, data utils
│
├── reports/             # Test execution reports
├── screenshots/         # Screenshots (clean or optional)
│
├── conftest.py          # PyTest fixtures
├── pytest.ini           # PyTest settings
├── requirement.txt      # Dependencies
├── Makefile             # Quick run commands
└── README.md

🚀 How to Run Tests
1️⃣ Install dependencies
pip install -r requirement.txt

2️⃣ Run all tests
pytest -v

3️⃣ Run tests in parallel
pytest -n auto


(if pytest-xdist installed)

4️⃣ Generate Allure report
pytest --alluredir=reports/allure
allure serve reports/allure

📱 Mobile Test Execution (Appium)

Ensure Appium server is running:

appium


Then run:

pytest -m mobile -v


Device capabilities are configured in:

config/appium_config.json

🧪 Test Design Standards

POM Architecture

Fixtures (session, module, function-level)

Reusable driver factory

Data-driven tests

Custom waits & utility library

🛠 Tech Stack Summary
Category	Tools
Language	Python 3.12
Test Runner	PyTest
Web Automation	Playwright
Mobile Testing	Appium
Reporting	Allure
Parallel Exec	PyTest-xdist
Architecture	POM + Fixtures
CI/CD Ready	GitHub Actions
🤝 Purpose of This Framework

This repo is a clean, professional demonstration of:

Your mobile automation skills

Python-based automation architecture

POM design pattern

CI/CD-friendly test structure

Real-world framework capabilities


📬 Contact

Premsena Reddy Anumandla
Senior QA Automation Engineer

📌 GitHub: @Premsenareddy
📌 LinkedIn: https://www.linkedin.com/in/premsena-anumandla-a802b4179/
