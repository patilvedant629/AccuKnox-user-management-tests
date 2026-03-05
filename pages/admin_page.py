from .base_page import BasePage
from playwright.sync_api import Page, expect

class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button = page.get_by_role("button", name="Add")
        self.search_username_input = page.locator(".oxd-input").nth(1)
        self.search_button = page.get_by_role("button", name="Search")
        self.save_button = page.get_by_role("button", name="Save")
        self.success_toast = page.locator(".oxd-toast-content--success")
        self.save_button_form = page.get_by_role("button", name="Save")
        
        # User details locators for adding/editing a user
        self.user_role_dropdown = page.locator(".oxd-select-text").nth(0)
        self.employee_name_input = page.get_by_placeholder("Type for hints...")
        self.status_dropdown = page.locator(".oxd-select-text").nth(1)
        self.username_input = page.locator("input.oxd-input").nth(1)  # On add/edit page
        self.password_input = page.locator("input[type='password']").nth(0)
        self.confirm_password_input = page.locator("input[type='password']").nth(1)

        # Grid locators
        self.table_row = page.locator(".oxd-table-row").nth(1) # The first data row
        self.delete_icon = self.table_row.locator(".bi-trash")
        self.edit_icon = self.table_row.locator(".bi-pencil-fill")
        self.confirm_delete_button = page.get_by_role("button", name="Yes, Delete")

    def click_add(self):
        self.add_button.click()
        self.page.wait_for_url("**/admin/saveSystemUser")

    def enter_user_details(self, user_role, employee_part, status, username, password=None):
        self.page.wait_for_load_state("networkidle")
        
        # Select User Role
        self.user_role_dropdown.click()
        self.page.get_by_role("option", name=user_role).click()
        
        # Enter Employee Name and wait for the dynamic autocomplete to load
        self.employee_name_input.fill(employee_part)
        
        # Explicit wait for the search API request to finish and render options
        self.page.wait_for_timeout(3000)
        
        # Wait for the dropdown wrapper to appear (OrangeHRM uses this class)
        self.page.locator(".oxd-autocomplete-dropdown").wait_for(state="visible", timeout=10000)
        # Click the very first suggestion that appears to avoid demo DB data issues
        self.page.get_by_role("option").first.click()
        
        # Select Status
        self.status_dropdown.click()
        self.page.get_by_role("option", name=status).click()

        # Enter Username
        self.username_input.fill(username)

        # Enter Password if provided (for adding new user)
        if password:
            self.password_input.fill(password)
            self.confirm_password_input.fill(password)
    
    def click_save(self):
        self.save_button_form.click()

    def wait_for_success(self):
        # Wait for the toast to appear, then wait for the network to settle down
        self.success_toast.wait_for(state="visible", timeout=10000)
        self.page.wait_for_load_state('networkidle')

    def search_for_user(self, username):
        # Clear the field sometimes helps if there's pre-existing text
        self.search_username_input.fill("")
        self.search_username_input.fill(username)
        self.search_button.click()
        self.page.wait_for_load_state('networkidle')

    def get_user_role_from_grid(self):
        # Index 2 is the User Role in the grid (Checkbox, Username, User Role, Employee Name, Status)
        return self.table_row.locator(".oxd-table-cell").nth(2).inner_text()
    
    def get_username_from_grid(self):
        return self.table_row.locator(".oxd-table-cell").nth(1).inner_text()

    def click_edit_user(self):
        self.edit_icon.click()
        self.page.wait_for_load_state('networkidle')

    def click_delete_user(self):
        self.delete_icon.click()
        self.confirm_delete_button.click()
