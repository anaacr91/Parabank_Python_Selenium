from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AccountsOverviewPage(BasePage):
    """
    Page Object para la página de resumen de cuentas
    """
    
    # Locators
    ACCOUNTS_OVERVIEW_TITLE = (By.XPATH, "//h1[contains(text(), 'Accounts Overview')]")
    ACCOUNT_TABLE = (By.ID, "accountTable")
    ACCOUNT_LINKS = (By.XPATH, "//table[@id='accountTable']//a")
    BALANCE_TOTAL = (By.XPATH, "//b[contains(text(), 'Balance')]/following-sibling::b")
    AVAILABLE_AMOUNT_TOTAL = (By.XPATH, "//b[contains(text(), 'Available Amount')]/following-sibling::b")
    
    # Menu items
    OPEN_NEW_ACCOUNT_LINK = (By.LINK_TEXT, "Open New Account")
    ACCOUNTS_OVERVIEW_LINK = (By.LINK_TEXT, "Accounts Overview")
    TRANSFER_FUNDS_LINK = (By.LINK_TEXT, "Transfer Funds")
    BILL_PAY_LINK = (By.LINK_TEXT, "Bill Pay")
    FIND_TRANSACTIONS_LINK = (By.LINK_TEXT, "Find Transactions")
    UPDATE_CONTACT_INFO_LINK = (By.LINK_TEXT, "Update Contact Info")
    REQUEST_LOAN_LINK = (By.LINK_TEXT, "Request Loan")
    LOG_OUT_LINK = (By.LINK_TEXT, "Log Out")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_accounts_overview_displayed(self):
        """Verificar si la página de resumen de cuentas está visible"""
        return self.is_element_visible(self.ACCOUNTS_OVERVIEW_TITLE)
    
    def get_account_numbers(self):
        """Obtener lista de números de cuenta"""
        account_elements = self.find_elements(self.ACCOUNT_LINKS)
        return [element.text for element in account_elements]
    
    def click_account(self, account_number):
        """Hacer click en una cuenta específica"""
        locator = (By.LINK_TEXT, str(account_number))
        self.click(locator)
    
    def get_total_balance(self):
        """Obtener el balance total"""
        return self.get_text(self.BALANCE_TOTAL)
    
    def click_open_new_account(self):
        """Navegar a abrir nueva cuenta"""
        self.click(self.OPEN_NEW_ACCOUNT_LINK)
    
    def click_transfer_funds(self):
        """Navegar a transferir fondos"""
        self.click(self.TRANSFER_FUNDS_LINK)
    
    def click_bill_pay(self):
        """Navegar a pagar facturas"""
        self.click(self.BILL_PAY_LINK)
    
    def click_find_transactions(self):
        """Navegar a buscar transacciones"""
        self.click(self.FIND_TRANSACTIONS_LINK)
    
    def click_update_contact_info(self):
        """Navegar a actualizar información de contacto"""
        self.click(self.UPDATE_CONTACT_INFO_LINK)
    
    def click_request_loan(self):
        """Navegar a solicitar préstamo"""
        self.click(self.REQUEST_LOAN_LINK)
    
    def click_logout(self):
        """Cerrar sesión"""
        self.click(self.LOG_OUT_LINK)
