from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time


class BasePage:
    """
    Clase base para todas las páginas
    Contiene métodos comunes utilizados en todas las páginas
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to(self, url):
        """Navegar a una URL"""
        self.driver.get(url)
    
    def find_element(self, locator):
        """Encontrar un elemento"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Encontrar múltiples elementos"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator, retry=3):
        """
        Hacer click en un elemento con retry para evitar StaleElementReferenceException
        """
        for attempt in range(retry):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == retry - 1:
                    raise
                time.sleep(0.5)
    
    def type(self, locator, text):
        """Escribir texto en un campo"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Obtener el texto de un elemento"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        """Verificar si un elemento es visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
    
    def get_current_url(self):
        """Obtener la URL actual"""
        return self.driver.current_url
    
    def get_title(self):
        """Obtener el título de la página"""
        return self.driver.title
