"""
Configuration settings for the test framework
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Test configuration"""
    
    # Browser settings
    DEFAULT_BROWSER = os.getenv('DEFAULT_BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))
    
    # URLs
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:3000')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
    
    # Directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_DATA_DIR = os.path.join(BASE_DIR, 'data')
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        for directory in [cls.TEST_DATA_DIR, cls.SCREENSHOTS_DIR, cls.REPORTS_DIR]:
            os.makedirs(directory, exist_ok=True)
