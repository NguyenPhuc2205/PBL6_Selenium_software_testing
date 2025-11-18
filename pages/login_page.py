"""
Login Page Object
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class LoginPage(BasePage):
    """Login page class"""
    
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-destructive, [role='alert']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:4000/auth/login"
    
    def navigate(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        time.sleep(1)
    
    def login(self, email: str, password: str) -> bool:
        """Perform login"""
        try:
            # Wait for email input
            email_input = self.wait_for_element(*self.EMAIL_INPUT)
            if not email_input:
                return False
            
            # Clear and input email
            email_input.clear()
            email_input.send_keys(email)
            time.sleep(0.5)
            
            # Input password
            password_input = self.wait_for_element(*self.PASSWORD_INPUT)
            if not password_input:
                return False
            
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(0.5)
            
            # Click login button
            login_button = self.wait_for_clickable(*self.LOGIN_BUTTON)
            if not login_button:
                return False
            
            login_button.click()
            
            # Wait for navigation or error
            time.sleep(3)
            
            # Check if still on login page (login failed)
            if "/auth/login" in self.driver.current_url:
                return False
            
            return True
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    def get_error_message(self) -> str:
        """Get error message"""
        try:
            error_element = self.wait_for_element(*self.ERROR_MESSAGE, timeout=5)
            return error_element.text if error_element else ""
        except:
            return ""
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return "/auth/login" not in self.driver.current_url
