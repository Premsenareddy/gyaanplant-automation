import sys
import os
import re
import json
from datetime import datetime, timezone
from pathlib import Path
import pytest
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.driver import create_web_page
from config.settings import WebConfig


def _safe_artifact_name(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


def _web_artifact_path(*parts: str) -> Path:
    base_dir = Path(WebConfig().artifacts_dir)
    path = base_dir.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def pytest_addoption(parser):
    parser.addoption(
        "--run-live-crud",
        action="store_true",
        default=False,
        help="Run live CRUD tests that can create or modify LMS records.",
    )


def pytest_collection_modifyitems(config, items):
    run_live_crud = config.getoption("--run-live-crud")

    for item in items:
        nodeid = item.nodeid.lower()

        if "/web/" in nodeid or nodeid.startswith("tests/web/"):
            item.add_marker(pytest.mark.web)
            if "mocked" in nodeid or "mock_" in item.name.lower():
                item.add_marker(pytest.mark.mocked)
            else:
                item.add_marker(pytest.mark.live)

            if "crud" in nodeid:
                item.add_marker(pytest.mark.crud)
                if not run_live_crud:
                    item.add_marker(
                        pytest.mark.skip(
                            reason="Live CRUD tests require --run-live-crud because they can modify LMS data."
                        )
                    )
            elif "mocked" in nodeid or "mock_" in item.name.lower():
                item.add_marker(pytest.mark.regression)
            elif "smoke" in nodeid:
                item.add_marker(pytest.mark.smoke)
            else:
                item.add_marker(pytest.mark.regression)

            if "launch_page_roles" in nodeid or "role" in item.name.lower():
                item.add_marker(pytest.mark.rbac)


@pytest.fixture
def web_page(request):
    config = WebConfig()
    playwright, browser, context, page = create_web_page()
    trace_mode = config.trace_mode.lower()
    trace_enabled = trace_mode in ("on", "retain-on-failure")

    if trace_enabled:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    report = getattr(request.node, "rep_call", None)
    failed = bool(report and report.failed)
    artifact_name = _safe_artifact_name(request.node.nodeid)

    if trace_enabled:
        if trace_mode == "on" or failed:
            trace_path = _web_artifact_path("traces", f"{artifact_name}.zip")
            context.tracing.stop(path=str(trace_path))
            print(f"\n[web trace] saved: {trace_path}")
        else:
            context.tracing.stop()

    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture(scope="session")
def admin_storage_state():
    config = WebConfig()
    state_path = Path(config.auth_state_path)
    if config.reuse_auth_state and state_path.exists():
        return str(state_path)

    email = os.getenv("LMS_EMAIL")
    password = os.getenv("LMS_PASSWORD")
    if not email or not password:
        pytest.skip("Set LMS_EMAIL and LMS_PASSWORD to create an authenticated storage state.")

    from pages.web.dashboard_page import DashboardPage

    state_path.parent.mkdir(parents=True, exist_ok=True)
    playwright, browser, context, page = create_web_page()
    try:
        dashboard = DashboardPage(page, config)
        dashboard.load()
        dashboard.login(email, password)
        dashboard.wait_for_dashboard()
        context.storage_state(path=str(state_path))
        return str(state_path)
    finally:
        context.close()
        browser.close()
        playwright.stop()


@pytest.fixture
def authenticated_web_page(request, admin_storage_state):
    config = WebConfig()
    playwright, browser, context, page = create_web_page(storage_state=admin_storage_state)
    trace_mode = config.trace_mode.lower()
    trace_enabled = trace_mode in ("on", "retain-on-failure")

    if trace_enabled:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    report = getattr(request.node, "rep_call", None)
    failed = bool(report and report.failed)
    artifact_name = _safe_artifact_name(request.node.nodeid)

    if trace_enabled:
        if trace_mode == "on" or failed:
            trace_path = _web_artifact_path("traces", f"{artifact_name}.zip")
            context.tracing.stop(path=str(trace_path))
            print(f"\n[web trace] saved: {trace_path}")
        else:
            context.tracing.stop()

    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------
# 📸 AUTOMATIC SCREENSHOT ON TEST FAILURE
# ----------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, f"rep_{result.when}", result)

    if result.when == "call" and result.failed:
        if "web_page" in item.fixturenames:
            page = item.funcargs.get("web_page")
            if page:
                screenshot_path = _web_artifact_path(
                    "screenshots", f"{_safe_artifact_name(item.nodeid)}.png"
                )
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n[web screenshot] saved: {screenshot_path}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    web_config = WebConfig()
    summary_dir = Path(web_config.artifacts_dir)
    summary_dir.mkdir(parents=True, exist_ok=True)

    stats = terminalreporter.stats
    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "exitstatus": exitstatus,
        "base_url": web_config.base_url,
        "browser": web_config.browser,
        "headless": web_config.headless,
        "passed": len(stats.get("passed", [])),
        "failed": len(stats.get("failed", [])),
        "skipped": len(stats.get("skipped", [])),
        "errors": len(stats.get("error", [])),
        "xfailed": len(stats.get("xfailed", [])),
        "xpassed": len(stats.get("xpassed", [])),
        "failed_tests": [report.nodeid for report in stats.get("failed", [])],
        "error_tests": [report.nodeid for report in stats.get("error", [])],
        "html_report": str(summary_dir / "pytest_report.html"),
        "screenshots_dir": str(summary_dir / "screenshots"),
        "traces_dir": str(summary_dir / "traces"),
    }

    json_path = summary_dir / "test_summary.json"
    markdown_path = summary_dir / "test_summary.md"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = [
        "# GyaanPlant Web Automation Test Summary",
        "",
        f"- Generated UTC: `{results['generated_at']}`",
        f"- Base URL: `{results['base_url']}`",
        f"- Browser: `{results['browser']}`",
        f"- Headless: `{results['headless']}`",
        f"- Exit status: `{results['exitstatus']}`",
        f"- Passed: `{results['passed']}`",
        f"- Failed: `{results['failed']}`",
        f"- Errors: `{results['errors']}`",
        f"- Skipped: `{results['skipped']}`",
        f"- HTML report: `{results['html_report']}`",
        f"- Screenshots: `{results['screenshots_dir']}`",
        f"- Traces: `{results['traces_dir']}`",
        "",
    ]
    if results["failed_tests"] or results["error_tests"]:
        lines.append("## Failed/Error Tests")
        lines.append("")
        for nodeid in [*results["failed_tests"], *results["error_tests"]]:
            lines.append(f"- `{nodeid}`")
        lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    terminalreporter.write_line(f"[web summary] saved: {markdown_path}")
