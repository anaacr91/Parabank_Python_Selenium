import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que inicializa y cierra el navegador para cada test
    Selenium 4.26+ incluye Selenium Manager que descarga automáticamente el driver correcto
    """
    driver = None
    
    try:
        # Intentar con Chrome primero
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless")  # Descomentar para ejecutar sin abrir ventana
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        # Selenium Manager descarga automáticamente el driver correcto
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ Chrome iniciado correctamente")
        
    except Exception as e:
        print(f"✗ No se pudo inicializar Chrome: {e}")
        print("Intentando con Microsoft Edge...")
        
        try:
            # Intentar con Edge
            edge_options = EdgeOptions()
            # edge_options.add_argument("--headless")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--start-maximized")
            
            driver = webdriver.Edge(options=edge_options)
            print("✓ Edge iniciado correctamente")
            
        except Exception as e2:
            print(f"✗ No se pudo inicializar Edge: {e2}")
            raise Exception("No se pudo inicializar ningún navegador (Chrome o Edge)")
    
    # Timeout implícito
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cerrar el navegador después del test
    if driver:
        driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """
    URL base de ParaBank
    """
    return "https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC"
