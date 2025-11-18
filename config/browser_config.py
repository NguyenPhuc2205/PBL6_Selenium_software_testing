"""
Browser configuration and driver management
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dotenv import load_dotenv

load_dotenv()


class BrowserConfig:
    """Browser configuration and initialization"""
    
    @staticmethod
    def get_chrome_driver(headless=False):
        """Initialize Chrome driver"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Use webdriver-manager with proper cache handling
        from webdriver_manager.core.os_manager import ChromeType
        driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
        
        # Fix for Windows path issue - ensure we get the actual exe
        if 'THIRD_PARTY_NOTICES' in driver_path:
            import os
            driver_dir = os.path.dirname(driver_path)
            driver_path = os.path.join(driver_dir, 'chromedriver.exe')
        
        driver = webdriver.Chrome(
            service=ChromeService(driver_path),
            options=options
        )
        return driver
    
    @staticmethod
    def get_firefox_driver(headless=False):
        """Initialize Firefox driver"""
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        return driver
    
    @staticmethod
    def get_edge_driver(headless=False):
        """Initialize Edge driver"""
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        return driver
    
    @staticmethod
    def get_driver(browser_name='chrome', headless=False):
        """Get driver based on browser name"""
        browser_name = browser_name.lower()
        
        if browser_name == 'chrome':
            return BrowserConfig.get_chrome_driver(headless)
        elif browser_name == 'firefox':
            return BrowserConfig.get_firefox_driver(headless)
        elif browser_name == 'edge':
            return BrowserConfig.get_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
