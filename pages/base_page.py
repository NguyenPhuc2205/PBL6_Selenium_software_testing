"""
Base Page class for Page Object Model
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config.settings import Config


class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def find_element(self, by: By, value: str):
        """Find element"""
        return self.driver.find_element(by, value)
    
    def find_elements(self, by: By, value: str):
        """Find multiple elements"""
        return self.driver.find_elements(by, value)
    
    def wait_for_element(self, by: By, value: str, timeout: int = None):
        """Wait for element to be present"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def wait_for_clickable(self, by: By, value: str, timeout: int = None):
        """Wait for element to be clickable"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def click(self, by: By, value: str):
        """Click element"""
        element = self.wait_for_clickable(by, value)
        if element:
            element.click()
            return True
        return False
    
    def input_text(self, by: By, value: str, text: str):
        """Input text to element"""
        element = self.wait_for_element(by, value)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
    
    def get_text(self, by: By, value: str) -> str:
        """Get text from element"""
        element = self.wait_for_element(by, value)
        return element.text if element else ""
    
    def is_element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, element):
        """Scroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title
