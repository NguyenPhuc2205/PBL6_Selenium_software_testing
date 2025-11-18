"""Pages package"""
from .base_page import BasePage
from .login_page import LoginPage
from .questions_page import QuestionsPage
from .manage_users_page import ManageUsersPage

__all__ = ['BasePage', 'LoginPage', 'QuestionsPage', 'ManageUsersPage']
