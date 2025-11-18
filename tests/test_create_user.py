"""
Test cases for Create User functionality
"""
import pytest
import time
from datetime import datetime
from pages.login_page import LoginPage
from pages.manage_users_page import ManageUsersPage
from utils.json_utils import JsonUtils
from utils.selenium_utils import SeleniumUtils
from utils.report_utils import ReportUtils
from config.settings import Config
import os


class TestCreateUser:
    """Test Create User functionality"""
    
    @pytest.fixture(scope="class")
    def test_data(self):
        """Load test data from JSON"""
        json_file = os.path.join(Config.TEST_DATA_DIR, 'create_user.json')
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
            f"create_user_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
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
    
    def test_tc_cu_001(self, driver, test_data, setup_teardown):
        """TC_CU_001: Tạo người dùng thành công - Đầy đủ thông tin hợp lệ (User)"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_CU_001'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            # Login
            assert self.login_helper(driver, test_case['args']['login_email'], test_case['args']['login_password']), \
                "Login failed"
            
            # Navigate to manage users page
            manage_users_page = ManageUsersPage(driver)
            manage_users_page.navigate()
            time.sleep(2)
            
            # Create user
            assert manage_users_page.create_user_full(test_case['args']), \
                "Failed to fill form"
            
            # Submit
            assert manage_users_page.submit_form(), "Failed to submit"
            
            # Verify success
            time.sleep(2)
            toast_message = manage_users_page.get_toast_message()
            
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
            # Take screenshot on failure
            if not test_result['screenshot']:
                screenshot_path = SeleniumUtils.take_screenshot(
                    driver,
                    test_case['test_case_id'] + "_FAIL",
                    Config.SCREENSHOTS_DIR
                )
                test_result['screenshot'] = screenshot_path
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            # Take screenshot on failure
            if not test_result['screenshot']:
                screenshot_path = SeleniumUtils.take_screenshot(
                    driver,
                    test_case['test_case_id'] + "_FAIL",
                    Config.SCREENSHOTS_DIR
                )
                test_result['screenshot'] = screenshot_path
            raise
    
    def test_tc_cu_002(self, driver, test_data, setup_teardown):
        """TC_CU_002: Tạo giảng viên thành công"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == 'TC_CU_002'), None)
        
        if not test_case:
            pytest.skip("Test case not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            assert self.login_helper(driver, test_case['args']['login_email'], test_case['args']['login_password']), "Login failed"
            manage_users_page = ManageUsersPage(driver)
            manage_users_page.navigate()
            time.sleep(2)
            assert manage_users_page.create_user_full(test_case['args']), "Failed to fill form"
            assert manage_users_page.submit_form(), "Failed to submit"
            time.sleep(2)
            toast_message = manage_users_page.get_toast_message()
            screenshot_path = SeleniumUtils.take_screenshot(driver, test_case['test_case_id'], Config.SCREENSHOTS_DIR)
            test_result['screenshot'] = screenshot_path
            assert 'success' in toast_message.lower() or 'thành công' in toast_message.lower(), f"Expected success, got: {toast_message}"
            test_result['actual'] = ReportUtils.format_actual_result(True, toast_message)
            test_result['result'] = 'PASS'
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case['test_case_id'] + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case['test_case_id'] + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
    
    @pytest.mark.parametrize("test_case_id", [
        "TC_CU_003", "TC_CU_004", "TC_CU_005"
    ])
    def test_optional_fields_success(self, driver, test_data, setup_teardown, test_case_id):
        """Test successful user creation with optional fields empty"""
        test_result = setup_teardown
        test_case = next((tc for tc in test_data if tc['test_case_id'] == test_case_id), None)
        
        if not test_case:
            pytest.skip(f"Test case {test_case_id} not found")
        
        test_result['test_case_id'] = test_case['test_case_id']
        test_result['description'] = test_case['description']
        test_result['expected'] = test_case['expected']
        test_result['input'] = ReportUtils.format_input_data(test_case['args'])
        
        try:
            assert self.login_helper(driver, test_case['args']['login_email'], test_case['args']['login_password']), "Login failed"
            manage_users_page = ManageUsersPage(driver)
            manage_users_page.navigate()
            time.sleep(2)
            assert manage_users_page.create_user_full(test_case['args']), "Failed to fill form"
            assert manage_users_page.submit_form(), "Failed to submit"
            time.sleep(2)
            toast_message = manage_users_page.get_toast_message()
            screenshot_path = SeleniumUtils.take_screenshot(driver, test_case_id, Config.SCREENSHOTS_DIR)
            test_result['screenshot'] = screenshot_path
            assert 'success' in toast_message.lower() or 'thành công' in toast_message.lower(), f"Expected success, got: {toast_message}"
            test_result['actual'] = ReportUtils.format_actual_result(True, toast_message)
            test_result['result'] = 'PASS'
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case_id + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case_id + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
    
    @pytest.mark.parametrize("test_case_id", [
        "TC_CU_006", "TC_CU_007", "TC_CU_008", "TC_CU_009", "TC_CU_010",
        "TC_CU_011", "TC_CU_012", "TC_CU_013", "TC_CU_014", "TC_CU_015"
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
            assert self.login_helper(driver, test_case['args']['login_email'], test_case['args']['login_password']), \
                "Login failed"
            
            # Navigate to manage users page
            manage_users_page = ManageUsersPage(driver)
            manage_users_page.navigate()
            time.sleep(2)
            
            # Create user with invalid data
            manage_users_page.create_user_full(test_case['args'])
            
            # Try to submit
            manage_users_page.submit_form()
            time.sleep(2)
            
            # Get errors
            errors = manage_users_page.get_error_messages()
            
            # Take screenshot
            screenshot_path = SeleniumUtils.take_screenshot(
                driver,
                test_case_id,
                Config.SCREENSHOTS_DIR
            )
            test_result['screenshot'] = screenshot_path
            
            # Verify errors exist
            assert len(errors) > 0, "Expected validation errors but got none"
            
            print(f"\n✓ Validation errors found: {errors}")
            
            test_result['actual'] = ReportUtils.format_actual_result(
                True,
                "Validation errors displayed",
                errors
            )
            test_result['result'] = 'PASS'
            
        except AssertionError as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, str(e))
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case_id + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
        except Exception as e:
            test_result['actual'] = ReportUtils.format_actual_result(False, f"Exception: {str(e)}")
            test_result['result'] = 'FAIL'
            if not test_result['screenshot']:
                test_result['screenshot'] = SeleniumUtils.take_screenshot(driver, test_case_id + "_FAIL", Config.SCREENSHOTS_DIR)
            raise
