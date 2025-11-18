import pytest
from pages.login_page import LoginPage
import time


def test_navigation_to_register_page_WITH_PAUSE(driver, base_url):
    """
    Test para VER la navegación a la página de registro
    El navegador se quedará abierto hasta que presiones Enter
    """
    # 1. Ir a la página de login
    driver.get(base_url)
    print(f"\n1. URL inicial: {driver.current_url}")
    time.sleep(1)
    
    login_page = LoginPage(driver)
    
    # 2. Click en el enlace de registro
    print("2. Haciendo click en 'Register'...")
    login_page.click_register()
    time.sleep(2)
    
    # 3. Mostrar la URL actual
    current_url = driver.current_url
    print(f"3. URL después del click: {current_url}")
    
    # 4. PAUSA - El navegador se queda abierto
    print("\n" + "="*60)
    print("🌐 NAVEGADOR ABIERTO EN LA PÁGINA DE REGISTRO")
    print("="*60)
    print(f"URL: {current_url}")
    print("\nMira el navegador Chrome que se abrió.")
    print("Presiona ENTER para continuar y cerrar el navegador...")
    input()  # ← Pausa hasta que presiones Enter
    
    # 5. Verificaciones
    assert "register.htm" in current_url
    assert "Register" in driver.page_source
    print("✓ Test completado")
