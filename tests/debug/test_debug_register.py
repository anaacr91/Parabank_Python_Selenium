import pytest
from pages.login_page import LoginPage
import time


def test_debug_register_navigation(driver, base_url):
    """
    Verificar paso a paso la navegación a registro
    """
    # 1. Ir a la página principal
    print(f"\n1. Navegando a: {base_url}")
    driver.get(base_url)
    time.sleep(1)
    
    current_url = driver.current_url
    print(f"2. URL actual: {current_url}")
    
    # 2. Buscar el enlace de registro
    login_page = LoginPage(driver)
    print("3. Haciendo click en el enlace 'Register'...")
    
    try:
        login_page.click_register()
        time.sleep(2)  # Esperar a que navegue
        
        # 3. Verificar la nueva URL
        new_url = driver.current_url
        print(f"4. Nueva URL después del click: {new_url}")
        
        # 4. Verificar contenido
        has_register_text = "Register" in driver.page_source
        print(f"5. ¿Contiene 'Register' en el HTML?: {has_register_text}")
        
        # 5. Verificar elementos de la página de registro
        print(f"6. Título de la página: {driver.title}")
        
        # 6. Tomar screenshot para ver qué página está mostrando
        driver.save_screenshot("register_page_debug.png")
        print("7. Screenshot guardado como: register_page_debug.png")
        
        # Verificaciones
        assert "register.htm" in new_url, f"No se navegó a register.htm. URL actual: {new_url}"
        assert has_register_text, "No se encontró texto 'Register' en la página"
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        driver.save_screenshot("error_register.png")
        raise
