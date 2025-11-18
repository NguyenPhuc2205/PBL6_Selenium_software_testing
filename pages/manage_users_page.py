"""
Manage Users Page Object
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class ManageUsersPage(BasePage):
    """Manage Users page class"""
    
    # Locators
    CREATE_USER_BTN = (By.XPATH, "//button[contains(., 'Thêm người dùng') or contains(., 'Add User') or contains(., 'Tạo người dùng')]")
    
    # Dialog
    DIALOG = (By.CSS_SELECTOR, "[role='dialog']")
    DIALOG_TITLE = (By.XPATH, "//h2[contains(text(), 'Thêm người dùng mới') or contains(text(), 'Add New User')]")
    
    # Form fields
    FULL_NAME_INPUT = (By.CSS_SELECTOR, "input[name='fullName']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[name='phone']")
    DATE_OF_BIRTH_INPUT = (By.CSS_SELECTOR, "input[name='dateOfBirth']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='confirmPassword']")
    
    # Select dropdowns (using label + parent + button structure within dialog)
    GENDER_SELECT_TRIGGER = (By.XPATH, "//div[@role='dialog']//label[contains(text(), 'Giới tính')]/parent::*//*[@role='combobox']")
    ROLE_SELECT_TRIGGER = (By.XPATH, "//div[@role='dialog']//label[contains(text(), 'Vai trò')]/parent::*//*[@role='combobox']")
    
    # Gender options (using role='option' from Radix UI Select)
    GENDER_MALE = (By.XPATH, "//*[@role='option'][contains(., 'Nam') and not(contains(., 'Nữ'))]")
    GENDER_FEMALE = (By.XPATH, "//*[@role='option'][contains(., 'Nữ')]")
    GENDER_OTHER = (By.XPATH, "//*[@role='option'][contains(., 'Khác')]")
    
    # Role options (using role='option' from Radix UI Select)
    ROLE_USER = (By.XPATH, "//*[@role='option'][contains(., 'Học viên')]")
    ROLE_TEACHER = (By.XPATH, "//*[@role='option'][contains(., 'Giảng viên')]")
    ROLE_ADMIN = (By.XPATH, "//*[@role='option'][contains(., 'Quản trị viên')]")
    
    # Buttons
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and (contains(., 'Tạo người dùng') or contains(., 'Create User'))]")
    CANCEL_BTN = (By.XPATH, "//button[contains(text(), 'Hủy') or contains(text(), 'Cancel')]")
    
    # Toast/Error messages
    TOAST_MESSAGE = (By.CSS_SELECTOR, "[data-sonner-toast], .sonner-toast, [data-toast]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-destructive, [role='alert']")
    FORM_ERROR = (By.XPATH, "//*[contains(@class, 'text-destructive') or contains(@class, 'text-sm')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:4000/admin/manage-users"
    
    def navigate(self):
        """Navigate to manage users page"""
        self.driver.get(self.url)
        time.sleep(2)
    
    def click_create_user(self):
        """Click create user button"""
        try:
            # Wait for page to fully load
            time.sleep(2)
            
            # Try with explicit wait first
            btn = self.wait_for_clickable(*self.CREATE_USER_BTN, timeout=10)
            if btn:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.5)
                btn.click()
                time.sleep(2)
                return True
            
            # Try finding all buttons with text
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            
            for button in all_buttons:
                try:
                    text = button.text.strip()
                    if text and ('người dùng' in text.lower() or 'add user' in text.lower() or 'tạo' in text.lower()):
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(0.5)
                        button.click()
                        time.sleep(2)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error clicking create user: {str(e)}")
            return False
    
    def wait_for_dialog(self, timeout: int = 10):
        """Wait for dialog to appear"""
        try:
            dialog = self.wait_for_element(*self.DIALOG, timeout=timeout)
            return dialog is not None
        except:
            return False
    
    def fill_full_name(self, full_name: str):
        """Fill full name field"""
        try:
            print(f"  → Filling full name: '{full_name}'")
            input_field = self.wait_for_element(*self.FULL_NAME_INPUT, timeout=10)
            if input_field:
                input_field.clear()
                input_field.send_keys(full_name)
                time.sleep(0.3)
                print(f"  ✓ Full name filled")
                return True
            print(f"  ❌ Full name input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling full name: {str(e)}")
            return False
    
    def fill_email(self, email: str):
        """Fill email field"""
        try:
            print(f"  → Filling email: '{email}'")
            input_field = self.wait_for_element(*self.EMAIL_INPUT, timeout=10)
            if input_field:
                input_field.clear()
                input_field.send_keys(email)
                time.sleep(0.3)
                print(f"  ✓ Email filled")
                return True
            print(f"  ❌ Email input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling email: {str(e)}")
            return False
    
    def fill_phone(self, phone: str):
        """Fill phone field"""
        try:
            print(f"  → Filling phone: '{phone}'")
            input_field = self.wait_for_element(*self.PHONE_INPUT, timeout=10)
            if input_field:
                input_field.clear()
                input_field.send_keys(phone)
                time.sleep(0.3)
                print(f"  ✓ Phone filled")
                return True
            print(f"  ❌ Phone input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling phone: {str(e)}")
            return False
    
    def fill_date_of_birth(self, date_str: str):
        """Fill date of birth field (format: YYYY-MM-DD)"""
        try:
            print(f"  → Filling date of birth: '{date_str}'")
            input_field = self.wait_for_element(*self.DATE_OF_BIRTH_INPUT, timeout=10)
            if input_field:
                # Clear existing value
                input_field.clear()
                time.sleep(0.2)
                
                # Use JavaScript to set the date value (more reliable for date inputs)
                self.driver.execute_script(f"arguments[0].value = '{date_str}';", input_field)
                
                # Trigger change and input events
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_field)
                time.sleep(0.3)
                print(f"  ✓ Date of birth filled")
                return True
            print(f"  ❌ Date of birth input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling date of birth: {str(e)}")
            return False
    
    def select_gender(self, gender: str):
        """Select gender (male, female, other)"""
        try:
            print(f"  → Attempting to select gender: {gender}")
            
            # Click select trigger using JavaScript to avoid interception
            trigger = self.wait_for_element(*self.GENDER_SELECT_TRIGGER, timeout=10)
            if not trigger:
                print("  ❌ Gender trigger not found")
                return False
            
            print(f"  → Found gender trigger, clicking with JavaScript...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
            time.sleep(0.3)
            # Use JavaScript click to avoid interception
            self.driver.execute_script("arguments[0].click();", trigger)
            time.sleep(1.5)  # Wait longer for dropdown to fully render
            
            # Select option based on gender
            gender_lower = gender.lower()
            if gender_lower in ['male', 'nam']:
                option_locator = self.GENDER_MALE
                option_name = "Nam"
            elif gender_lower in ['female', 'nữ', 'nu']:
                option_locator = self.GENDER_FEMALE
                option_name = "Nữ"
            elif gender_lower in ['other', 'khác', 'khac']:
                option_locator = self.GENDER_OTHER
                option_name = "Khác"
            else:
                print(f"  ❌ Invalid gender: {gender}")
                return False
            
            print(f"  → Waiting for option: {option_name}")
            option = self.wait_for_clickable(*option_locator, timeout=5)
            
            if option:
                print(f"  → Clicking option: {option_name}")
                option.click()
                time.sleep(0.5)
                print(f"  ✓ Gender selected: {option_name}")
                return True
            else:
                print(f"  ❌ Gender option not found: {option_name}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error selecting gender: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def select_role(self, role: str):
        """Select role (user, teacher, admin)"""
        try:
            print(f"  → Attempting to select role: {role}")
            
            # Click select trigger using JavaScript to avoid interception
            trigger = self.wait_for_element(*self.ROLE_SELECT_TRIGGER, timeout=10)
            if not trigger:
                print("  ❌ Role trigger not found")
                return False
            
            print(f"  → Found role trigger, clicking with JavaScript...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
            time.sleep(0.3)
            # Use JavaScript click to avoid interception
            self.driver.execute_script("arguments[0].click();", trigger)
            time.sleep(1.5)  # Wait longer for dropdown to fully render
            
            # Select option based on role
            role_lower = role.lower()
            if role_lower in ['user', 'học viên', 'hoc vien', 'sinh viên', 'sinh vien']:
                option_locator = self.ROLE_USER
                option_name = "Học viên"
            elif role_lower in ['teacher', 'giảng viên', 'giang vien']:
                option_locator = self.ROLE_TEACHER
                option_name = "Giảng viên"
            elif role_lower in ['admin', 'quản trị', 'quan tri', 'quản trị viên']:
                option_locator = self.ROLE_ADMIN
                option_name = "Quản trị viên"
            else:
                print(f"  ❌ Invalid role: {role}")
                return False
            
            print(f"  → Waiting for option: {option_name}")
            option = self.wait_for_clickable(*option_locator, timeout=5)
            
            if option:
                print(f"  → Clicking option: {option_name}")
                option.click()
                time.sleep(0.5)
                print(f"  ✓ Role selected: {option_name}")
                return True
            else:
                print(f"  ❌ Role option not found: {option_name}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error selecting role: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def fill_password(self, password: str):
        """Fill password field"""
        try:
            print(f"  → Filling password field")
            input_field = self.wait_for_element(*self.PASSWORD_INPUT, timeout=10)
            if input_field:
                input_field.clear()
                input_field.send_keys(password)
                time.sleep(0.3)
                print(f"  ✓ Password filled")
                return True
            print(f"  ❌ Password input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling password: {str(e)}")
            return False
    
    def fill_confirm_password(self, confirm_password: str):
        """Fill confirm password field"""
        try:
            print(f"  → Filling confirm password field")
            input_field = self.wait_for_element(*self.CONFIRM_PASSWORD_INPUT, timeout=10)
            if input_field:
                input_field.clear()
                input_field.send_keys(confirm_password)
                time.sleep(0.3)
                print(f"  ✓ Confirm password filled")
                return True
            print(f"  ❌ Confirm password input not found")
            return False
        except Exception as e:
            print(f"  ❌ Error filling confirm password: {str(e)}")
            return False
    
    def submit_form(self):
        """Submit the form"""
        try:
            btn = self.wait_for_clickable(*self.SUBMIT_BTN, timeout=5)
            if btn:
                btn.click()
                time.sleep(2)
                return True
            return False
        except Exception as e:
            print(f"Error submitting form: {str(e)}")
            return False
    
    def cancel_form(self):
        """Cancel the form"""
        try:
            btn = self.wait_for_clickable(*self.CANCEL_BTN)
            if btn:
                btn.click()
                time.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"Error canceling form: {str(e)}")
            return False
    
    def get_toast_message(self, timeout: int = 5) -> str:
        """Get toast message"""
        try:
            toast = self.wait_for_element(*self.TOAST_MESSAGE, timeout=timeout)
            if toast:
                return toast.text
            return ""
        except:
            return ""
    
    def get_error_messages(self) -> list:
        """Get all error messages from form"""
        try:
            time.sleep(0.5)  # Wait for errors to appear
            errors = self.find_elements(*self.FORM_ERROR)
            error_texts = []
            for error in errors:
                text = error.text.strip()
                if text and len(text) > 0:
                    error_texts.append(text)
            return error_texts
        except Exception as e:
            print(f"Error getting error messages: {str(e)}")
            return []
    
    def has_error_message(self, expected_message: str) -> bool:
        """Check if specific error message exists"""
        errors = self.get_error_messages()
        return any(expected_message.lower() in error.lower() for error in errors)
    
    def create_user_full(self, test_data: dict) -> bool:
        """Create user with full data"""
        try:
            print(f"\n=== Starting create_user_full ===")
            print(f"Test data: {test_data}")
            
            # Click create button
            print("Step 1: Clicking create user button...")
            if not self.click_create_user():
                print("❌ Failed to click create button")
                return False
            print("✓ Create button clicked")
            
            # Wait for dialog
            print("\nStep 2: Waiting for dialog...")
            if not self.wait_for_dialog(timeout=10):
                print("❌ Dialog did not appear")
                return False
            print("✓ Dialog appeared")
            
            # Fill full name
            if 'full_name' in test_data:
                print("\nStep 3: Filling full name...")
                if not self.fill_full_name(test_data['full_name']):
                    return False
            
            # Fill email
            if 'email' in test_data:
                print("\nStep 4: Filling email...")
                if not self.fill_email(test_data['email']):
                    return False
            
            # Fill phone (optional)
            if 'phone' in test_data and test_data['phone']:
                print("\nStep 5: Filling phone...")
                if not self.fill_phone(test_data['phone']):
                    return False
            
            # Select gender (optional)
            if 'gender' in test_data and test_data['gender']:
                print("\nStep 6: Selecting gender...")
                if not self.select_gender(test_data['gender']):
                    return False
            
            # Fill date of birth (optional)
            if 'date_of_birth' in test_data and test_data['date_of_birth']:
                print("\nStep 7: Filling date of birth...")
                if not self.fill_date_of_birth(test_data['date_of_birth']):
                    return False
            
            # Select role
            if 'role' in test_data:
                print("\nStep 8: Selecting role...")
                if not self.select_role(test_data['role']):
                    return False
            
            # Fill password
            if 'password' in test_data:
                print("\nStep 9: Filling password...")
                if not self.fill_password(test_data['password']):
                    return False
            
            # Fill confirm password
            if 'confirm_password' in test_data:
                print("\nStep 10: Filling confirm password...")
                if not self.fill_confirm_password(test_data['confirm_password']):
                    return False
            
            print("\n=== ✓ Form filled successfully ===")
            return True
            
        except Exception as e:
            print(f"\n❌ Error creating user: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
