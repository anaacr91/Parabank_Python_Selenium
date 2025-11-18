from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object para la página de login de ParaBank
    """
    
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FORGOT_LOGIN_LINK = (By.LINK_TEXT, "Forgot login info?")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")
    ERROR_TITLE = (By.XPATH, "//h1[@class='title']")
    WELCOME_MESSAGE = (By.XPATH, "//p[@class='smallText']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_username(self, username):
        """Ingresar nombre de usuario"""
        self.type(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Ingresar contraseña"""
        self.type(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Hacer click en el botón de login"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Realizar login completo"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def click_register(self):
        """Hacer click en el enlace de registro"""
        self.click(self.REGISTER_LINK)
    
    def is_error_displayed(self):
        """Verificar si se muestra un mensaje de error"""
        # ParaBank puede mostrar el error en diferentes elementos
        return (self.is_element_visible(self.ERROR_MESSAGE) or 
                self.is_element_visible(self.ERROR_TITLE))
    
    def get_error_message(self):
        """Obtener el mensaje de error"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        elif self.is_element_visible(self.ERROR_TITLE):
            return self.get_text(self.ERROR_TITLE)
        return ""
    
    def is_login_successful(self):
        """Verificar si el login fue exitoso"""
        return self.is_element_visible(self.WELCOME_MESSAGE)
