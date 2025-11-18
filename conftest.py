"""
Pytest configuration and fixtures
"""
import pytest
from config.browser_config import BrowserConfig
from config.settings import Config


@pytest.fixture(scope="function")
def driver(request):
    """Setup and teardown browser driver"""
    browser = request.config.getoption("--browser", default=Config.DEFAULT_BROWSER)
    headless = request.config.getoption("--headless", default=Config.HEADLESS)
    
    # Setup
    driver = BrowserConfig.get_driver(browser, headless)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    # Teardown
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    Config.ensure_directories()


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=Config.HEADLESS,
        help="Run tests in headless mode"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            from utils.selenium_utils import SeleniumUtils
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                f"failed_{item.name}",
                Config.SCREENSHOTS_DIR
            )
            print(f"\nScreenshot saved: {screenshot_path}")
