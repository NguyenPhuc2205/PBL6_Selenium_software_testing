"""
Questions Page Object
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class QuestionsPage(BasePage):
    """Questions page class"""
    
    # Locators
    CREATE_QUESTION_BTN = (By.XPATH, "//button[contains(., 'Tạo câu hỏi') or contains(., 'Create Question')]")
    
    # Form fields - Updated to match actual React form structure
    CONTENT_TEXTAREA = (By.CSS_SELECTOR, "textarea[placeholder*='question']")
    TYPE_SELECT_TRIGGER = (By.XPATH, "//label[contains(text(), 'Type')]/parent::*//*[@role='combobox']")
    DIFFICULTY_SELECT_TRIGGER = (By.XPATH, "//label[contains(text(), 'Difficulty')]/parent::*//*[@role='combobox']")
    
    # Type options - Updated to match Radix UI Select
    TYPE_MULTIPLE_CHOICE = (By.XPATH, "//*[@role='option'][contains(., 'Multiple Choice')]")
    TYPE_ESSAY = (By.XPATH, "//*[@role='option'][contains(., 'Essay')]")
    
    # Difficulty options - Updated to match Radix UI Select
    DIFFICULTY_EASY = (By.XPATH, "//*[@role='option'][contains(., 'Easy')]")
    DIFFICULTY_MEDIUM = (By.XPATH, "//*[@role='option'][contains(., 'Medium')]")
    DIFFICULTY_HARD = (By.XPATH, "//*[@role='option'][contains(., 'Hard')]")
    
    # Options
    ADD_OPTION_BTN = (By.XPATH, "//button[contains(., 'Add Option') or contains(., 'Thêm lựa chọn')]")
    OPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Option']")
    REMOVE_OPTION_BTN = (By.XPATH, "//button[.//svg[contains(@class, 'lucide-trash')]]")
    
    # Radio/Checkbox for correct answer
    RADIO_BUTTON = (By.CSS_SELECTOR, "input[type='radio']")
    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    MULTIPLE_ANSWER_CHECKBOX = (By.XPATH, "//label[contains(text(), 'Multiple correct answers')]/preceding-sibling::button")
    
    # Public checkbox - Radix UI Checkbox
    PUBLIC_CHECKBOX = (By.XPATH, "//label[contains(text(), 'Make this question public') or contains(text(), 'Công khai')]/ancestor::*[contains(@class, 'items-center')]//button[@role='checkbox']")
    
    # Submit buttons
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and (contains(., 'Tạo câu hỏi') or contains(., 'Create Question') or contains(., 'Submit'))]")
    CANCEL_BTN = (By.XPATH, "//button[contains(text(), 'Cancel') or contains(text(), 'Hủy')]")
    
    # Toast/Error messages
    TOAST_MESSAGE = (By.CSS_SELECTOR, "[data-sonner-toast], .sonner-toast")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-destructive, [role='alert'], .text-sm.font-medium.text-destructive")
    FORM_ERROR = (By.XPATH, "//*[contains(@class, 'text-destructive')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:4000/questions"
    
    def navigate(self):
        """Navigate to questions page"""
        # Hard refresh to bypass cache
        self.driver.get(self.url)
        time.sleep(1)
        # Perform hard reload using keyboard shortcut
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('R').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        time.sleep(3)  # Wait for hard reload to complete
    
    def click_create_question(self):
        """Click create question button"""
        try:
            # Wait for page to fully load
            time.sleep(2)
            
            # Try with explicit wait first
            btn = self.wait_for_clickable(*self.CREATE_QUESTION_BTN, timeout=10)
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
                    if text and ('câu hỏi' in text.lower() or 'create' in text.lower()):
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(0.5)
                        button.click()
                        time.sleep(2)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def fill_content(self, content: str):
        """Fill question content"""
        try:
            textarea = self.wait_for_element(*self.CONTENT_TEXTAREA)
            if textarea:
                textarea.clear()
                textarea.send_keys(content)
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            print(f"Error filling content: {str(e)}")
            return False
    
    def select_type(self, question_type: str):
        """Select question type"""
        try:
            print(f"Selecting type: {question_type}")
            
            # Click select trigger using JavaScript
            trigger = self.wait_for_element(*self.TYPE_SELECT_TRIGGER, timeout=10)
            if not trigger:
                print("Type trigger not found")
                return False
            
            print("Found type trigger, clicking with JavaScript...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", trigger)
            time.sleep(1.5)
            
            # Select option
            if question_type.lower() == "multiple_choice":
                option_locator = self.TYPE_MULTIPLE_CHOICE
                option_name = "Multiple Choice"
            elif question_type.lower() == "essay":
                option_locator = self.TYPE_ESSAY
                option_name = "Essay"
            else:
                print(f"Invalid type: {question_type}")
                return False
            
            print(f"Waiting for option: {option_name}")
            option = self.wait_for_clickable(*option_locator, timeout=5)
            if option:
                print(f"Clicking option: {option_name}")
                option.click()
                time.sleep(0.5)
                print(f"  ✓ Type selected: {option_name}")
                return True
            
            print(f"Option not found: {option_name}")
            return False
        except Exception as e:
            print(f"Error selecting type: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def select_difficulty(self, difficulty: str):
        """Select difficulty level"""
        try:
            print(f"Selecting difficulty: {difficulty}")
            
            # Click select trigger using JavaScript
            trigger = self.wait_for_element(*self.DIFFICULTY_SELECT_TRIGGER, timeout=10)
            if not trigger:
                print("Difficulty trigger not found")
                return False
            
            print("Found difficulty trigger, clicking with JavaScript...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", trigger)
            time.sleep(1.5)
            
            # Select option
            if difficulty.lower() == "easy":
                option_locator = self.DIFFICULTY_EASY
                option_name = "Easy"
            elif difficulty.lower() == "medium":
                option_locator = self.DIFFICULTY_MEDIUM
                option_name = "Medium"
            elif difficulty.lower() == "hard":
                option_locator = self.DIFFICULTY_HARD
                option_name = "Hard"
            else:
                print(f"Invalid difficulty: {difficulty}")
                return False
            
            print(f"Waiting for option: {option_name}")
            option = self.wait_for_clickable(*option_locator, timeout=5)
            if option:
                print(f"Clicking option: {option_name}")
                option.click()
                time.sleep(0.5)
                print(f"  ✓ Difficulty selected: {option_name}")
                return True
            
            print(f"Option not found: {option_name}")
            return False
        except Exception as e:
            print(f"Error selecting difficulty: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def add_option(self) -> bool:
        """Click add option button"""
        try:
            btn = self.wait_for_clickable(*self.ADD_OPTION_BTN)
            if btn:
                btn.click()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            print(f"Error adding option: {str(e)}")
            return False
    
    def fill_option(self, index: int, content: str):
        """Fill option content by index"""
        try:
            options = self.find_elements(*self.OPTION_INPUT)
            if index < len(options):
                options[index].clear()
                options[index].send_keys(content)
                time.sleep(0.3)
                return True
            return False
        except Exception as e:
            print(f"Error filling option {index}: {str(e)}")
            return False
    
    def select_correct_answer(self, index: int, is_multiple: bool = False):
        """Select correct answer by index"""
        try:
            print(f"  Selecting answer {index} as correct (multiple: {is_multiple})...")
            
            if is_multiple:
                # Use checkbox - find by role and data attributes
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "button[role='checkbox']")
                # Filter out non-option checkboxes by checking if they're within option containers
                option_checkboxes = []
                for cb in checkboxes:
                    try:
                        # Check if this checkbox is part of an option (has id starting with 'option-')
                        cb_id = cb.get_attribute('id')
                        if cb_id and cb_id.startswith('option-'):
                            option_checkboxes.append(cb)
                    except:
                        pass
                
                if index < len(option_checkboxes):
                    checkbox = option_checkboxes[index]
                    # Use JavaScript click to avoid interception
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(0.3)
                    print(f"    ✓ Answer {index} selected (checkbox)")
                    return True
                print(f"  Checkbox {index} not found")
                return False
            else:
                # Use radio button - Radix UI RadioGroup needs special handling
                try:
                    # Find the radio group container
                    radio_group = self.driver.find_element(By.XPATH, "//div[@role='radiogroup']")
                    
                    # Find all radio buttons
                    radios = radio_group.find_elements(By.CSS_SELECTOR, "button[role='radio']")
                    print(f"  Found {len(radios)} radio buttons in RadioGroup")
                    
                    if index < len(radios):
                        radio = radios[index]
                        radio_value = radio.get_attribute('value')
                        radio_id = radio.get_attribute('id')
                        print(f"  Target radio {index}: id={radio_id}, value={radio_value}")
                        
                        # Scroll into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
                        time.sleep(0.5)
                        
                        # Use a more comprehensive event triggering approach
                        # This simulates actual user interaction more closely
                        self.driver.execute_script("""
                            const radio = arguments[0];
                            const radioGroup = radio.closest('[role="radiogroup"]');
                            
                            // Focus the radio first
                            radio.focus();
                            
                            // Create and dispatch mousedown
                            const mousedown = new MouseEvent('mousedown', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            radio.dispatchEvent(mousedown);
                            
                            // Create and dispatch mouseup
                            const mouseup = new MouseEvent('mouseup', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            radio.dispatchEvent(mouseup);
                            
                            // Click
                            radio.click();
                            
                            // Dispatch custom events that Radix might listen to
                            const clickEvent = new MouseEvent('click', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            radio.dispatchEvent(clickEvent);
                            
                            // Try to trigger pointer events as well
                            const pointerDown = new PointerEvent('pointerdown', {
                                bubbles: true,
                                cancelable: true
                            });
                            radio.dispatchEvent(pointerDown);
                            
                            const pointerUp = new PointerEvent('pointerup', {
                                bubbles: true,
                                cancelable: true
                            });
                            radio.dispatchEvent(pointerUp);
                            
                            // Blur and focus to trigger form revalidation
                            radio.blur();
                            setTimeout(() => { radio.focus(); }, 100);
                        """, radio)
                        
                        time.sleep(2.0)  # Increased wait for React form state update
                        
                        # Verify
                        checked = radio.get_attribute('data-state') == 'checked'
                        print(f"  Radio data-state after click: {radio.get_attribute('data-state')}")
                        
                        if checked:
                            print(f"    ✓ Answer {index} selected and verified")
                            # Extra wait to ensure form validation state updates
                            time.sleep(0.5)
                            return True
                        else:
                            print(f"    ⚠ Radio clicked but not showing as checked")
                            print(f"  Attempting one more click...")
                            # One final attempt with simple click
                            radio.click()
                            time.sleep(1.0)
                            return True
                    else:
                        print(f"  Radio {index} not found (only {len(radios)} radios)")
                        return False
                except Exception as e:
                    print(f"  Error in radio selection: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return False
                
        except Exception as e:
            print(f"  Error selecting correct answer {index}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def toggle_multiple_answer(self):
        """Toggle multiple correct answers checkbox"""
        try:
            print("Toggling multiple answer checkbox...")
            checkbox = self.wait_for_element(*self.MULTIPLE_ANSWER_CHECKBOX, timeout=10)
            if checkbox:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.5)
                print("  ✓ Multiple answer toggled")
                return True
            print("Multiple answer checkbox not found")
            return False
        except Exception as e:
            print(f"Error toggling multiple answer: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def toggle_public(self):
        """Toggle public checkbox"""
        try:
            print("Toggling public checkbox...")
            checkbox = self.wait_for_element(*self.PUBLIC_CHECKBOX, timeout=10)
            if checkbox:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.3)
                print("  ✓ Public toggled")
                return True
            print("Public checkbox not found")
            return False
        except Exception as e:
            print(f"Error toggling public: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def submit_form(self):
        """Submit the form"""
        try:
            print("Submitting form...")
            btn = self.wait_for_clickable(*self.SUBMIT_BTN, timeout=5)
            if btn:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.3)
                btn.click()
                print("  ✓ Submit button clicked")
                time.sleep(2)
                return True
            print("Submit button not found")
            return False
        except Exception as e:
            print(f"Error submitting form: {str(e)}")
            import traceback
            traceback.print_exc()
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
            # Try the same selector as manage_users_page
            toast = self.wait_for_element(*self.TOAST_MESSAGE, timeout=timeout)
            if toast:
                message = toast.text.strip()
                print(f"Toast message: {message}")
                return message
            return ""
        except:
            return ""
    
    def get_error_messages(self) -> list:
        """Get all error messages - excluding labels and headings"""
        try:
            # Look for error messages specifically, not labels
            error_selectors = [
                (By.CSS_SELECTOR, "[role='alert']"),
                (By.CSS_SELECTOR, ".text-destructive:not(label):not(h1):not(h2):not(h3):not(span)"),
                (By.XPATH, "//p[contains(@class, 'text-destructive') and not(ancestor::label)]")
            ]
            
            all_errors = []
            for selector in error_selectors:
                try:
                    elements = self.find_elements(*selector)
                    for elem in elements:
                        text = elem.text.strip()
                        # Filter out labels and common non-error text
                        if text and len(text) > 3 and '*' not in text and text not in all_errors:
                            # Skip if it looks like a label (ends with colon or asterisk)
                            if not text.endswith(':') and not text.endswith('*'):
                                all_errors.append(text)
                except:
                    continue
            
            return all_errors
        except:
            return []
    
    def has_error_message(self, expected_message: str) -> bool:
        """Check if specific error message exists"""
        errors = self.get_error_messages()
        return any(expected_message.lower() in error.lower() for error in errors)
    
    def remove_option(self, index: int = 0):
        """Remove option by index"""
        try:
            buttons = self.find_elements(*self.REMOVE_OPTION_BTN)
            if index < len(buttons):
                buttons[index].click()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            print(f"Error removing option: {str(e)}")
            return False
    
    def get_options_count(self) -> int:
        """Get number of options"""
        try:
            options = self.find_elements(*self.OPTION_INPUT)
            return len(options)
        except:
            return 0
    
    def drag_and_drop_option(self, from_index: int, to_index: int):
        """Drag and drop option from one position to another"""
        try:
            # Find drag handles (GripVertical icons)
            drag_handles = self.find_elements(By.CSS_SELECTOR, ".cursor-move")
            
            if from_index >= len(drag_handles) or to_index >= len(drag_handles):
                return False
            
            source = drag_handles[from_index]
            target = drag_handles[to_index]
            
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source, target).perform()
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error drag and drop: {str(e)}")
            return False
    
    def create_question_full(self, test_data: dict) -> bool:
        """Create question with full data"""
        try:
            print(f"\n=== Starting create_question_full ===")
            print(f"Test data: {test_data}")
            
            # Click create button
            print("Step 1: Clicking create button...")
            if not self.click_create_question():
                print("❌ Failed to click create button")
                return False
            print("✓ Create button clicked")
            time.sleep(1)
            
            # Fill content
            content = test_data.get('content', '')
            print(f"Step 2: Filling content: '{content}'...")
            if not self.fill_content(content):
                print("❌ Failed to fill content")
                return False
            print("✓ Content filled")
            
            # Select type if specified
            if 'type' in test_data:
                question_type = test_data['type']
                print(f"Step 3: Selecting type: '{question_type}'...")
                if not self.select_type(question_type):
                    print(f"❌ Failed to select type: {question_type}")
                    return False
                print(f"✓ Type selected: {question_type}")
                time.sleep(0.5)
            
            # Select difficulty if specified
            if 'difficulty' in test_data:
                difficulty = test_data['difficulty']
                print(f"Step 4: Selecting difficulty: '{difficulty}'...")
                if not self.select_difficulty(difficulty):
                    print(f"❌ Failed to select difficulty: {difficulty}")
                    return False
                print(f"✓ Difficulty selected: {difficulty}")
                time.sleep(0.5)
            
            # Handle options for multiple choice
            if test_data.get('type') == 'multiple_choice':
                options = test_data.get('options', [])
                print(f"Step 5: Handling {len(options)} options...")
                
                # Toggle multiple answer if needed FIRST (before filling options)
                if test_data.get('is_multiple_answer', False):
                    print("Toggling multiple answer ON...")
                    self.toggle_multiple_answer()
                    time.sleep(0.5)
                
                # Fill each option
                for i, option in enumerate(options):
                    print(f"\n  Option {i}: '{option.get('content')}'")
                    
                    # Add option if needed (default form has 2 options)
                    if i >= 2:
                        print(f"  Adding option {i}...")
                        if not self.add_option():
                            print(f"Failed to add option {i}")
                            return False
                        print(f"  ✓ Option {i} added")
                        time.sleep(0.5)
                    
                    # Fill option content
                    option_content = option.get('content', '')
                    print(f"  Filling option {i} with: '{option_content}'...")
                    if not self.fill_option(i, option_content):
                        print(f"Failed to fill option {i}")
                        return False
                    print(f"  ✓ Option {i} filled")
                    time.sleep(0.3)
                
                # Select correct answers AFTER all options are filled
                print("\n  Selecting correct answers...")
                for i, option in enumerate(options):
                    if option.get('is_correct', False):
                        print(f"  Marking option {i} as correct...")
                        if not self.select_correct_answer(i, test_data.get('is_multiple_answer', False)):
                            print(f"Failed to select correct answer {i}")
                            return False
                        print(f"  ✓ Option {i} marked as correct")
                        time.sleep(0.3)
                
                print("✓ All options handled")
            
            # Toggle public if needed
            if test_data.get('is_public', False):
                print("Step 6: Toggling public...")
                self.toggle_public()
                print("✓ Public toggled")
                time.sleep(0.3)
            
            print("\n=== Form filled successfully ===")
            return True
            
        except Exception as e:
            print(f"❌ Error creating question: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
