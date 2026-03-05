import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

# Test data
USERNAME = "Admin"
PASSWORD = "admin123"
NEW_USER_ROLE = "Admin"
NEW_USER_EMPLOYEE_PART = "m"
NEW_USER_EMPLOYEE_FULL = "manda user" # This needs to be an existing employee in OrangeHRM demo data
NEW_USER_STATUS = "Enabled" # or Disabled
NEW_USER_USERNAME = "accuknox_tester_12345"
NEW_USER_PASSWORD = "StrongPassword123!"

# Updated data
UPDATED_USER_ROLE = "ESS"

# Note: We use module scope for some state, or we rely on the tests running in order.
# For simplicity in this assessment, we ensure they run in order and use the same page fixture.
# A better practice for totally independent tests would be creating a fresh user via API for each test,
# but UI E2E tests often follow a flow. pytest-dependency or just logical ordering works.

def test_navigate_to_admin_module(page: Page):
    """Scenario 1: Navigate to the Admin Module"""
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    
    # Pre-condition: User is logged in
    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login(USERNAME, PASSWORD)
    
    # Step: Click on Admin
    dashboard_page.navigate_to_admin()
    
    # Expected: The Admin User Management page is displayed
    expect(page.locator(".oxd-topbar-header-breadcrumb-module")).to_contain_text("Admin")

def test_add_new_user(page: Page):
    """Scenario 2: Add a New User"""
    admin_page = AdminPage(page)
    
    # Ensure we are on the page (from previous test flow)
    admin_page.click_add()
    
    # The DOM for adding a user is tricky in OrangeHRM, so we rely on precise interaction
    admin_page.enter_user_details(
        user_role=NEW_USER_ROLE,
        employee_part="a", # 'a' is a very safe bet to trigger the auto-complete hints for any employee
        status=NEW_USER_STATUS,
        username=NEW_USER_USERNAME,
        password=NEW_USER_PASSWORD
    )
    admin_page.click_save()
    
    # Verify success toast and grid row
    admin_page.wait_for_success()

def test_search_newly_created_user(page: Page):
    """Scenario 3: Search the Newly Created User"""
    admin_page = AdminPage(page)
    
    admin_page.search_for_user(NEW_USER_USERNAME)
    
    # Expected: The grid filters to show only the newly created user
    assert admin_page.get_username_from_grid() == NEW_USER_USERNAME
    assert admin_page.get_user_role_from_grid() == NEW_USER_ROLE

def test_edit_user_details(page: Page):
    """Scenario 4: Edit User Details"""
    admin_page = AdminPage(page)
    
    # Pre-condition: User must be searched and in the grid 
    # (Assuming we continue from previous test's state)
    admin_page.click_edit_user()
    
    # Change the role to ESS
    page.locator(".oxd-select-text").nth(0).click()
    page.get_by_role("option", name=UPDATED_USER_ROLE).click()
    
    admin_page.click_save()
    admin_page.wait_for_success()

def test_validate_updated_details(page: Page):
    """Scenario 5: Validate Updated Details"""
    admin_page = AdminPage(page)
    
    admin_page.search_for_user(NEW_USER_USERNAME)
    
    # Verify the User Role is now ESS
    assert admin_page.get_user_role_from_grid() == UPDATED_USER_ROLE

def test_delete_user(page: Page):
    """Scenario 6: Delete the User"""
    admin_page = AdminPage(page)
    
    # Pre-condition: User is searched and in grid
    admin_page.click_delete_user()
    admin_page.wait_for_success()
    
    # Verify deletion by searching again
    admin_page.search_for_user(NEW_USER_USERNAME)
    expect(page.locator(".oxd-toast-content--info")).to_contain_text("No Records Found")
