import pytest
from pages.login_page import LoginPage
import time


class TestDebug:
    """
    Tests de depuración para ver qué pasa realmente
    """
    
    def test_debug_empty_credentials(self, driver, base_url):
        """
        Verificar qué pasa cuando NO ingresamos credenciales
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # NO ingresamos nada, solo hacemos click en login
        login_page.click_login()
        time.sleep(2)
        
        # Verificar si sigue en la página de login o fue redirigido
        current_url = driver.current_url
        print(f"\n🔍 URL después de login vacío: {current_url}")
        
        # Verificar si hay mensaje de error
        has_error = login_page.is_error_displayed()
        print(f"🔍 ¿Muestra error?: {has_error}")
        
        if has_error:
            error_msg = login_page.get_error_message()
            print(f"🔍 Mensaje de error: {error_msg}")
        
        # Verificar si llegó a la página de cuentas (no debería)
        is_logged_in = "overview" in current_url.lower()
        print(f"🔍 ¿Logueó sin credenciales?: {is_logged_in}")
        
        # El test debería verificar que NO se logueó
        assert not is_logged_in, "¡ERROR! El sistema permitió login sin credenciales"
        assert has_error or "index" in current_url, "Debería mostrar error o quedarse en login"
    
    def test_debug_invalid_credentials(self, driver, base_url):
        """
        Verificar qué pasa con credenciales inválidas
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Intentar con credenciales inválidas
        invalid_user = "usuario_que_no_existe_12345"
        invalid_pass = "password_incorrecto_98765"
        
        login_page.login(invalid_user, invalid_pass)
        time.sleep(2)
        
        # Verificar URL
        current_url = driver.current_url
        print(f"\n🔍 URL después de login inválido: {current_url}")
        
        # Verificar error
        has_error = login_page.is_error_displayed()
        print(f"🔍 ¿Muestra error?: {has_error}")
        
        if has_error:
            error_msg = login_page.get_error_message()
            print(f"🔍 Mensaje de error: {error_msg}")
        
        # Verificar si logueó (no debería)
        is_logged_in = "overview" in current_url.lower()
        print(f"🔍 ¿Logueó con credenciales inválidas?: {is_logged_in}")
        
        # El test debería verificar que NO se logueó
        assert not is_logged_in, "¡ERROR! El sistema permitió login con credenciales inválidas"
        assert has_error, "Debería mostrar un mensaje de error"
    
    def test_debug_valid_credentials(self, driver, base_url):
        """
        Verificar qué pasa con credenciales válidas (john/demo)
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login con credenciales válidas
        login_page.login("john", "demo")
        time.sleep(2)
        
        # Verificar URL
        current_url = driver.current_url
        print(f"\n🔍 URL después de login válido: {current_url}")
        
        # Verificar si logueó correctamente
        is_logged_in = "overview" in current_url.lower()
        print(f"🔍 ¿Logueó correctamente?: {is_logged_in}")
        
        # Este SÍ debería loguear
        assert is_logged_in, "¡ERROR! No se pudo loguear con credenciales válidas"
