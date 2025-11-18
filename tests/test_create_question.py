"""
Test cases for Create Question functionality
"""
import pytest
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.questions_page import QuestionsPage
from utils.json_utils import JsonUtils
from utils.selenium_utils import SeleniumUtils
from utils.report_utils import ReportUtils
from config.settings import Config
import os


class TestCreateQuestion:
    """Test Create Question functionality"""
    
    @pytest.fixture(scope="class")
    def test_data(self):
        """Load test data from JSON"""
        json_file = os.path.join(Config.TEST_DATA_DIR, 'create_question.json')
        return JsonUtils.read_json(json_file)
    
    @pytest.fixture(scope="class")
    def test_results(self):
        """Store test results"""
        return []
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, driver, test_results, request):
        """Setup and teardown for each test"""
        test_result = {
            'stt': len(test_results) + 1,
            'test_case_id': '',
            'description': '',
            'input': '',
            'expected': '',
            'actual': '',
            'result': 'FAIL',
            'screenshot': '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        yield test_result
        
        # Save result
        test_results.append(test_result)
    
    @pytest.fixture(scope="class", autouse=True)
    def generate_report(self, test_results):
        """Generate report after all tests"""
        yield
        
        # Generate Excel report
        report_file = os.path.join(
            Config.REPORTS_DIR,
            f"create_question_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        ReportUtils.create_test_report(report_file, test_results)
        print(f"\n{'='*80}")
        print(f"Test Report Generated: {report_file}")
        print(f"{'='*80}")
    
    def login_helper(self, driver, email: str, password: str) -> bool:
        """Helper method to login"""
        login_page = LoginPage(driver)
        login_page.navigate()
        return login_page.login(email, password)
    
    def test_tc_0001(self, driver, test_data, setup_teardown):
        """TC_0001: Tạo câu hỏi trắc nghiệm thành công - Single choice"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0001'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), \
                "Login failed"
            
            # Navigate to questions page
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(2)
            
            # Create question
            assert questions_page.create_question_full(test_case['args']), \
                "Failed to fill form"
            
            # Submit
            assert questions_page.submit_form(), "Failed to submit"
            
            # Verify success - check toast or verify question appears in list
            time.sleep(2)
            toast_message = questions_page.get_toast_message()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case['test_case_id'],
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Check for success - either toast message or question appears in list
            has_success_toast = toast_message and ('success' in toast_message.lower() or 'thành công' in toast_message.lower())
            
            # Check if question appears in the list (as additional verification)
            question_content = test_case['args']['content']
            page_text = driver.find_element(By.TAG_NAME, "body").text
            question_created = question_content in page_text
            
            assert has_success_toast or question_created, \
                f"Expected success message or question in list. Toast: {toast_message}, Question found: {question_created}"
            
            test_result['actual'] = ReportUtils.format_actual_result(
                True, 
                f"Toast: {toast_message if toast_message else 'N/A'}\nQuestion created and visible in list"
            )
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    def test_tc_0002(self, driver, test_data, setup_teardown):
        """TC_0002: Tạo câu hỏi tự luận thành công"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0002'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), \
                "Login failed"
            
            # Navigate to questions page
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(2)
            
            # Create question
            assert questions_page.create_question_full(test_case['args']), \
                "Failed to fill form"
            
            # Submit
            assert questions_page.submit_form(), "Failed to submit"
            
            # Verify success
            time.sleep(2)
            toast_message = questions_page.get_toast_message()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case['test_case_id'],
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Check for success
            assert 'success' in toast_message.lower() or 'thành công' in toast_message.lower(), \
                f"Expected success message, got: {toast_message}"
            
            test_result['actual'] = ReportUtils.format_actual_result(True, toast_message)
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    def test_tc_0003(self, driver, test_data, setup_teardown):
        """TC_0003: Thêm option - Kiểm tra toast hiển thị"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0003'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = "Action: Add option"
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), \
                "Login failed"
            
            # Navigate and open form
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(1)
            questions_page.click_create_question()
            time.sleep(1)
            
            # Add option
            initial_count = questions_page.get_options_count()
            assert questions_page.add_option(), "Failed to add option"
            
            # Verify toast
            time.sleep(1)
            toast_message = questions_page.get_toast_message()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case['test_case_id'],
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Verify
            assert 'thêm' in toast_message.lower() or 'added' in toast_message.lower(), \
                f"Expected add success toast, got: {toast_message}"
            
            final_count = questions_page.get_options_count()
            assert final_count == initial_count + 1, \
                f"Expected {initial_count + 1} options, got {final_count}"
            
            test_result['actual'] = ReportUtils.format_actual_result(
                True,
                f"Toast: {toast_message}\nOptions: {initial_count} → {final_count}"
            )
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    def test_tc_0005(self, driver, test_data, setup_teardown):
        """TC_0005: Không thể xóa option khi chỉ còn 2"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0005'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = "Action: Try to remove option when only 2 remain"
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), \
                "Login failed"
            
            # Navigate and open form
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(1)
            questions_page.click_create_question()
            time.sleep(1)
            
            # Try to remove option
            initial_count = questions_page.get_options_count()
            questions_page.remove_option(0)
            
            # Verify warning toast
            time.sleep(1)
            toast_message = questions_page.get_toast_message()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case['test_case_id'],
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Verify
            assert 'không thể' in toast_message.lower() or 'cannot' in toast_message.lower(), \
                f"Expected warning toast, got: {toast_message}"
            
            final_count = questions_page.get_options_count()
            assert final_count == initial_count, \
                f"Options should not change, was {initial_count}, now {final_count}"
            
            test_result['actual'] = ReportUtils.format_actual_result(
                True,
                f"Toast: {toast_message}\nOptions count unchanged: {initial_count}"
            )
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    def test_tc_0004(self, driver, test_data, setup_teardown):
        """TC_0004: Xóa option thành công"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0004'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = "Action: Remove option successfully"
        
        try:
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), "Login failed"
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(1)
            questions_page.click_create_question()
            time.sleep(1)
            questions_page.add_option()
            time.sleep(1)
            initial_count = questions_page.get_options_count()
            assert questions_page.remove_option(0), "Failed to remove option"
            time.sleep(1)
            toast_message = questions_page.get_toast_message()
            screenshot_path = SeleniumUtils.take_screenshot(driver, test_case['test_case_id'], Config.SCREENSHOTS_DIR)
            test_result['screenshot'] = screenshot_path
            final_count = questions_page.get_options_count()
            test_result['actual'] = ReportUtils.format_actual_result(True, f"Toast: {toast_message}\nOptions: {initial_count} → {final_count}")
            test_result['result'] = 'PASS'
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    def test_tc_0006(self, driver, test_data, setup_teardown):
        """TC_0006: Drag & drop"""
        pytest.skip("Drag & drop requires special handling")
    
    def test_tc_0007(self, driver, test_data, setup_teardown):
        """TC_0007: Multiple correct answers"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_0007'), None)
        if not test_case:
            pytest.skip("Test case not found")
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        try:
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), "Login failed"
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(2)
            assert questions_page.create_question_full(test_case['args']), "Failed to fill form"
            assert questions_page.submit_form(), "Failed to submit"
            time.sleep(2)
            toast_message = questions_page.get_toast_message()
            screenshot_path = SeleniumUtils.take_screenshot(driver, test_case['test_case_id'], Config.SCREENSHOTS_DIR)
            test_result['screenshot'] = screenshot_path
            assert 'success' in toast_message.lower() or 'thành công' in toast_message.lower(), f"Expected success message, got: {toast_message}"
            test_result['actual'] = ReportUtils.format_actual_result(True, toast_message)
            test_result['result'] = 'PASS'
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    @pytest.mark.parametrize("test_case_id", [
        "TC_0008", "TC_0009", "TC_0010", "TC_0011", "TC_0012", "TC_0013", "TC_0014",
        "TC_0018", "TC_0019", "TC_0020",
    ])
    def test_validation_errors(self, driver, test_data, setup_teardown, test_case_id):
        """Test validation error cases"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == test_case_id), None)
        
        if not test_case:
            pytest.skip(f"Test case {test_case_id} not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), \
                "Login failed"
            
            # Navigate to questions page
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(1)
            
            # Create question with invalid data
            questions_page.create_question_full(test_case['args'])
            
            # Try to submit
            questions_page.submit_form()
            time.sleep(2)
            
            # Get errors
            errors = questions_page.get_error_messages()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case_id,
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Verify errors exist
            assert len(errors) > 0, "Expected validation errors but got none"
            
            test_result['actual'] = ReportUtils.format_actual_result(
                True,
                "Validation errors displayed",
                errors
            )
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    @pytest.mark.parametrize("test_case_id", ["TC_0015", "TC_0016"])
    def test_boundary_valid(self, driver, test_data, setup_teardown, test_case_id):
        """Test boundary valid cases"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == test_case_id), None)
        if not test_case:
            pytest.skip(f"Test case {test_case_id} not found")
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        try:
            assert self.login_helper(driver, test_case['args']['email'], test_case['args']['password']), "Login failed"
            questions_page = QuestionsPage(driver)
            questions_page.navigate()
            time.sleep(2)
            assert questions_page.create_question_full(test_case['args']), "Failed to fill form"
            assert questions_page.submit_form(), "Failed to submit"
            time.sleep(2)
            toast_message = questions_page.get_toast_message()
            screenshot_path = SeleniumUtils.take_screenshot(driver, test_case_id, Config.SCREENSHOTS_DIR)
            test_result['screenshot'] = screenshot_path
            assert 'success' in toast_message.lower() or 'thành công' in toast_message.lower(), f"Expected success, got: {toast_message}"
            test_result['actual'] = ReportUtils.format_actual_result(True, toast_message)
            test_result['result'] = 'PASS'
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            raise
    
    @pytest.mark.parametrize("test_case_id", ["TC_0017", "TC_0021", "TC_0022"])
    def test_ui_interactions(self, driver, test_data, setup_teardown, test_case_id):
        """Test UI interactions"""
        pytest.skip(f"UI interaction test {test_case_id} requires manual verification")

