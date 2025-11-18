"""
Common utility functions for Selenium testing
"""
import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SeleniumUtils:
    """Selenium helper functions"""
    
    @staticmethod
    def wait_for_element(driver, by: By, value: str, timeout: int = 10):
        """Wait for element to be present"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    @staticmethod
    def wait_for_element_clickable(driver, by: By, value: str, timeout: int = 10):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    @staticmethod
    def take_screenshot(driver, name: str, directory: str = './screenshots'):
        """Take screenshot and save to directory"""
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(directory, filename)
        driver.save_screenshot(filepath)
        return filepath
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll to element"""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    @staticmethod
    def scroll_to_bottom(driver):
        """Scroll to bottom of page"""
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    
    @staticmethod
    def get_element_text(driver, by: By, value: str, timeout: int = 10) -> str:
        """Get text from element"""
        element = SeleniumUtils.wait_for_element(driver, by, value, timeout)
        return element.text if element else ""
    
    @staticmethod
    def click_element(driver, by: By, value: str, timeout: int = 10) -> bool:
        """Click element"""
        element = SeleniumUtils.wait_for_element_clickable(driver, by, value, timeout)
        if element:
            element.click()
            return True
        return False
    
    @staticmethod
    def input_text(driver, by: By, value: str, text: str, timeout: int = 10) -> bool:
        """Input text to element"""
        element = SeleniumUtils.wait_for_element(driver, by, value, timeout)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
