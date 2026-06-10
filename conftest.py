import sys
import os
import re
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
            item.add_marker(pytest.mark.live)

            if "crud" in nodeid:
                item.add_marker(pytest.mark.crud)
                if not run_live_crud:
                    item.add_marker(
                        pytest.mark.skip(
                            reason="Live CRUD tests require --run-live-crud because they can modify LMS data."
                        )
                    )
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
