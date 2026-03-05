from .base_page import BasePage
from playwright.sync_api import Page

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.admin_menu_item = page.locator("a[href*='/admin/viewAdminModule']")

    def navigate_to_admin(self):
        self.admin_menu_item.click()
        # Wait for the Admin page to load
        self.page.wait_for_url("**/admin/viewSystemUsers**")
        self.page.wait_for_load_state('networkidle')
