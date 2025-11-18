import pytest
from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage


class TestParaBank:
    """
    Suite de tests para ParaBank
    """
    
    # Credenciales de prueba (puedes crear una cuenta o usar estas de ejemplo)
    VALID_USERNAME = "john"
    VALID_PASSWORD = "demo"
    INVALID_USERNAME = "invalid_user"
    INVALID_PASSWORD = "wrong_password"
    
    def test_access_parabank_website(self, driver, base_url):
        """
        Test 1: Verificar que se puede acceder al sitio web de ParaBank
        """
        driver.get(base_url)
        
        # Verificar que la página se carga correctamente
        assert "ParaBank" in driver.title
        assert "parabank.parasoft.com" in driver.current_url
    
    def test_login_with_valid_credentials(self, driver, base_url):
        """
        Test 2: Login exitoso con credenciales válidas
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Realizar login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # Verificar que el login fue exitoso
        accounts_page = AccountsOverviewPage(driver)
        assert accounts_page.is_accounts_overview_displayed(), "No se pudo acceder a la página de cuentas"
    
    def test_login_with_invalid_credentials(self, driver, base_url):
        """
        Test 3: Login con credenciales inválidas debe mostrar error y NO permitir acceso
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Intentar login con credenciales inválidas
        login_page.login(self.INVALID_USERNAME, self.INVALID_PASSWORD)
        
        # Verificar que se muestra mensaje de error
        assert login_page.is_error_displayed(), "No se mostró mensaje de error"
        error_message = login_page.get_error_message()
        assert error_message != "", "El mensaje de error está vacío"
        print(f"✓ Error mostrado: {error_message}")
        
        # Verificar que NO se logueó (debe seguir en página de login)
        current_url = driver.current_url
        assert "overview" not in current_url.lower(), "ERROR: Se logueó con credenciales inválidas"
        assert "login" in current_url.lower() or "index" in current_url.lower(), "No se quedó en la página de login"
    
    def test_login_with_empty_credentials(self, driver, base_url):
        """
        Test 4: Login con campos vacíos debe mostrar error y NO permitir acceso
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Intentar login sin ingresar credenciales
        login_page.click_login()
        
        # Verificar que se muestra mensaje de error
        assert login_page.is_error_displayed(), "No se mostró mensaje de error con campos vacíos"
        error_message = login_page.get_error_message()
        assert error_message != "", "El mensaje de error está vacío"
        print(f"✓ Error mostrado: {error_message}")
        
        # Verificar que NO se logueó (debe seguir en página de login)
        current_url = driver.current_url
        assert "overview" not in current_url.lower(), "ERROR: Se logueó sin credenciales"
        assert "login" in current_url.lower() or "index" in current_url.lower(), "No se quedó en la página de login"
    
    def test_navigation_to_register_page(self, driver, base_url):
        """
        Test 5: Navegar a la página de registro
        """
        import time
        
        # 1. Ir a la página de login
        driver.get(base_url)
        print(f"\n1. URL inicial: {driver.current_url}")
        
        login_page = LoginPage(driver)
        
        # 2. Click en el enlace de registro
        login_page.click_register()
        time.sleep(1)  # Esperar a que navegue
        
        # 3. Verificar la URL después del click
        current_url = driver.current_url
        print(f"2. URL después del click: {current_url}")
        
        # PAUSA PARA VER LA PÁGINA (comentar después)
        print("\n⏸️  PÁGINA DE REGISTRO ABIERTA - Esperando 5 segundos...")
        time.sleep(5)  # ← Quitar o comentar esto después de verificar
        
        # 4. Verificar que se navega a la página de registro
        assert "register.htm" in current_url, f"No se navegó a register.htm. URL actual: {current_url}"
        assert "Register" in driver.page_source, "No se encontró el texto 'Register' en la página"
        
        print("✓ Navegación a registro exitosa")
    
    def test_accounts_overview_elements(self, driver, base_url):
        """
        Test 6: Verificar elementos en la página de resumen de cuentas
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # Verificar elementos en la página de cuentas
        accounts_page = AccountsOverviewPage(driver)
        assert accounts_page.is_accounts_overview_displayed()
        
        # Verificar que hay cuentas disponibles
        account_numbers = accounts_page.get_account_numbers()
        assert len(account_numbers) > 0, "No se encontraron cuentas"
    
    def test_logout_functionality(self, driver, base_url):
        """
        Test 7: Verificar funcionalidad de logout
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # Logout
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_logout()
        
        # Verificar que regresa a la página de login
        assert "index.htm" in driver.current_url
        
    def test_navigate_to_transfer_funds(self, driver, base_url):
        """
        Test 8: Navegar a la página de transferencia de fondos
        """
        import time
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Transfer Funds
        accounts_page = AccountsOverviewPage(driver)
        print(f"\n1. URL antes del click: {driver.current_url}")
        
        accounts_page.click_transfer_funds()
        time.sleep(1)
        
        # Verificar la navegación
        current_url = driver.current_url
        print(f"2. URL después del click: {current_url}")
        
        assert "transfer.htm" in current_url, f"URL esperada con 'transfer.htm', pero se obtuvo: {current_url}"
        print("✓ Navegación a Transfer Funds exitosa")
    
    def test_transfer_funds_between_accounts(self, driver, base_url):
        """
        Test 8b: Realizar una transferencia de fondos entre cuentas
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Obtener las cuentas disponibles antes de la transferencia
        accounts_page = AccountsOverviewPage(driver)
        account_numbers = accounts_page.get_account_numbers()
        print(f"\n1. Cuentas disponibles: {account_numbers}")
        
        # Verificar que hay al menos 2 cuentas para hacer transferencia
        assert len(account_numbers) >= 2, "Se necesitan al menos 2 cuentas para hacer una transferencia"
        
        # Navegar a Transfer Funds
        accounts_page.click_transfer_funds()
        time.sleep(1)
        
        current_url = driver.current_url
        print(f"2. En página de transferencia: {current_url}")
        assert "transfer.htm" in current_url
        
        # Ingresar monto a transferir
        amount_input = driver.find_element(By.ID, "amount")
        transfer_amount = "10.00"
        amount_input.clear()
        amount_input.send_keys(transfer_amount)
        print(f"3. Monto a transferir: ${transfer_amount}")
        
        # Seleccionar cuenta de origen (fromAccountId)
        from_account_select = Select(driver.find_element(By.ID, "fromAccountId"))
        from_account = from_account_select.first_selected_option.text
        print(f"4. Cuenta origen: {from_account}")
        
        # Seleccionar cuenta destino (toAccountId) - debe ser diferente a la origen
        to_account_select = Select(driver.find_element(By.ID, "toAccountId"))
        to_account_options = to_account_select.options
        
        # Seleccionar la primera opción diferente a la cuenta origen
        for option in to_account_options:
            if option.text != from_account:
                to_account_select.select_by_visible_text(option.text)
                to_account = option.text
                break
        
        print(f"5. Cuenta destino: {to_account}")
        
        # Hacer click en Transfer
        transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
        transfer_button.click()
        time.sleep(2)
        
        # Verificar que la transferencia fue exitosa
        success_message = "Transfer Complete!" in driver.page_source
        assert success_message, "No se encontró el mensaje de confirmación de transferencia"
        
        # Verificar detalles de la transferencia en la página de resultado
        assert transfer_amount in driver.page_source, f"No se encontró el monto transferido: ${transfer_amount}"
        
        print(f"✓ Transferencia de ${transfer_amount} realizada exitosamente")
        print(f"  Desde: {from_account}")
        print(f"  Hacia: {to_account}")
    
    def test_transfer_funds_with_invalid_amount(self, driver, base_url):
        """
        Test 8c: Intentar transferir con monto inválido (debe mostrar error)
        """
        import time
        from selenium.webdriver.common.by import By
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Transfer Funds
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_transfer_funds()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Intentar transferir sin ingresar monto (dejar vacío)
        amount_input = driver.find_element(By.ID, "amount")
        amount_input.clear()
        print("2. Campo de monto dejado vacío")
        
        # Hacer click en Transfer
        transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
        transfer_button.click()
        time.sleep(2)
        
        # Verificar que NO se completó la transferencia
        # Debe mostrar error o quedarse en la misma página
        current_url = driver.current_url
        
        # Si muestra error, la URL debería seguir siendo transfer.htm
        # O debería haber un mensaje de error
        has_error = "error" in driver.page_source.lower() or "transfer.htm" in current_url
        
        print(f"3. URL después del intento: {current_url}")
        print(f"4. ¿Muestra error o se queda en transfer?: {has_error}")
        
        # Verificar que NO dice "Transfer Complete!"
        assert "Transfer Complete!" not in driver.page_source, "ERROR: La transferencia se completó sin monto"
        
        print("✓ Validación correcta: no permite transferencia sin monto")
    
    def test_navigate_to_bill_pay(self, driver, base_url):
        """
        Test 9: Navegar a la página de pago de facturas
        """
        import time
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Bill Pay
        accounts_page = AccountsOverviewPage(driver)
        print(f"\n1. URL antes del click: {driver.current_url}")
        
        accounts_page.click_bill_pay()
        time.sleep(1)
        
        # Verificar la navegación
        current_url = driver.current_url
        print(f"2. URL después del click: {current_url}")
        
        assert "billpay.htm" in current_url, f"URL esperada con 'billpay.htm', pero se obtuvo: {current_url}"
        assert "Bill Payment Service" in driver.page_source, "No se encontró el título 'Bill Payment Service'"
        
        print("✓ Navegación a Bill Pay exitosa")
    
    def test_bill_pay_complete_payment(self, driver, base_url):
        """
        Test 9b: Realizar un pago de factura completo
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Bill Pay
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_bill_pay()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Completar el formulario de pago de factura
        # Payee Name
        payee_name = "Electric Company"
        driver.find_element(By.NAME, "payee.name").send_keys(payee_name)
        print(f"2. Nombre del beneficiario: {payee_name}")
        
        # Address
        address = "123 Main Street"
        driver.find_element(By.NAME, "payee.address.street").send_keys(address)
        
        # City
        city = "New York"
        driver.find_element(By.NAME, "payee.address.city").send_keys(city)
        
        # State
        state = "NY"
        driver.find_element(By.NAME, "payee.address.state").send_keys(state)
        
        # Zip Code
        zip_code = "10001"
        driver.find_element(By.NAME, "payee.address.zipCode").send_keys(zip_code)
        
        # Phone
        phone = "555-1234"
        driver.find_element(By.NAME, "payee.phoneNumber").send_keys(phone)
        
        # Account Number
        account_number = "98765"
        driver.find_element(By.NAME, "payee.accountNumber").send_keys(account_number)
        
        # Verify Account
        driver.find_element(By.NAME, "verifyAccount").send_keys(account_number)
        
        # Amount
        amount = "50.00"
        driver.find_element(By.NAME, "amount").send_keys(amount)
        print(f"3. Monto a pagar: ${amount}")
        
        # Select Account (from which account to pay)
        from_account_select = Select(driver.find_element(By.NAME, "fromAccountId"))
        from_account = from_account_select.first_selected_option.text
        print(f"4. Cuenta de pago: {from_account}")
        
        # Click Send Payment
        send_payment_button = driver.find_element(By.XPATH, "//input[@value='Send Payment']")
        send_payment_button.click()
        time.sleep(2)
        
        # Verificar que el pago fue exitoso
        current_url = driver.current_url
        print(f"5. URL después del pago: {current_url}")
        
        # Buscar mensaje de confirmación
        success_message = "Bill Payment Complete" in driver.page_source or "Bill Payment to" in driver.page_source
        assert success_message, "No se encontró el mensaje de confirmación de pago"
        
        # Verificar que aparece el nombre del beneficiario y el monto
        assert payee_name in driver.page_source, f"No se encontró el beneficiario: {payee_name}"
        assert amount in driver.page_source, f"No se encontró el monto: ${amount}"
        
        print(f"✓ Pago de ${amount} a {payee_name} realizado exitosamente")
    
    def test_bill_pay_with_empty_fields(self, driver, base_url):
        """
        Test 9c: Intentar pagar factura con campos vacíos (debe mostrar errores)
        """
        import time
        from selenium.webdriver.common.by import By
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Bill Pay
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_bill_pay()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Intentar enviar el formulario sin llenar campos
        send_payment_button = driver.find_element(By.XPATH, "//input[@value='Send Payment']")
        send_payment_button.click()
        time.sleep(2)
        
        print("2. Formulario enviado sin datos")
        
        # Verificar que muestra mensajes de error
        current_url = driver.current_url
        print(f"3. URL después del intento: {current_url}")
        
        # Debe quedarse en la misma página (billpay.htm)
        assert "billpay.htm" in current_url, "No se quedó en la página de bill pay"
        
        # Buscar mensajes de error en el formulario
        errors_found = driver.page_source.lower().count("is required") > 0 or driver.page_source.count("error") > 0
        
        print(f"4. ¿Muestra errores de validación?: {errors_found}")
        
        # Verificar que NO se completó el pago
        assert "Bill Payment Complete" not in driver.page_source, "ERROR: El pago se completó sin datos"
        
        print("✓ Validación correcta: no permite pago sin completar campos requeridos")
    
    def test_bill_pay_with_mismatched_account_numbers(self, driver, base_url):
        """
        Test 9d: Intentar pagar con números de cuenta que no coinciden (debe mostrar error)
        """
        import time
        from selenium.webdriver.common.by import By
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Bill Pay
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_bill_pay()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Llenar campos básicos
        driver.find_element(By.NAME, "payee.name").send_keys("Test Payee")
        driver.find_element(By.NAME, "payee.address.street").send_keys("123 Street")
        driver.find_element(By.NAME, "payee.address.city").send_keys("City")
        driver.find_element(By.NAME, "payee.address.state").send_keys("State")
        driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
        driver.find_element(By.NAME, "payee.phoneNumber").send_keys("555-0000")
        
        # Account Number y Verify Account NO coinciden
        driver.find_element(By.NAME, "payee.accountNumber").send_keys("11111")
        driver.find_element(By.NAME, "verifyAccount").send_keys("22222")  # Diferente
        print("2. Números de cuenta NO coinciden: 11111 vs 22222")
        
        driver.find_element(By.NAME, "amount").send_keys("10.00")
        
        # Click Send Payment
        send_payment_button = driver.find_element(By.XPATH, "//input[@value='Send Payment']")
        send_payment_button.click()
        time.sleep(2)
        
        current_url = driver.current_url
        print(f"3. URL después del intento: {current_url}")
        
        # Debe quedarse en billpay.htm o mostrar error
        assert "billpay.htm" in current_url, "No se quedó en la página de bill pay"
        
        # Verificar que NO se completó el pago
        assert "Bill Payment Complete" not in driver.page_source, "ERROR: El pago se completó con cuentas que no coinciden"
        
        print("✓ Validación correcta: no permite pago con números de cuenta diferentes")
    
    def test_navigate_to_open_new_account(self, driver, base_url):
        """
        Test 10: Navegar a la página de abrir nueva cuenta
        """
        import time
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Open New Account
        accounts_page = AccountsOverviewPage(driver)
        print(f"\n1. URL antes del click: {driver.current_url}")
        
        accounts_page.click_open_new_account()
        time.sleep(1)
        
        # Verificar la navegación
        current_url = driver.current_url
        print(f"2. URL después del click: {current_url}")
        
        assert "openaccount.htm" in current_url, f"URL esperada con 'openaccount.htm', pero se obtuvo: {current_url}"
        
        # Verificar que aparece el título de la página
        assert "Open New Account" in driver.page_source, "No se encontró el título 'Open New Account'"
        print("✓ Navegación a Open New Account exitosa")
    
    def test_open_new_savings_account(self, driver, base_url):
        """
        Test 11: Abrir una nueva cuenta de ahorros (Savings)
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Open New Account
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_open_new_account()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Seleccionar tipo de cuenta (Savings)
        account_type_select = Select(driver.find_element(By.ID, "type"))
        account_type_select.select_by_visible_text("SAVINGS")
        print("2. Tipo de cuenta seleccionado: SAVINGS")
        
        # El formulario ya tiene una cuenta seleccionada por defecto para transferir fondos
        # Solo necesitamos hacer click en "Open New Account"
        open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
        open_button.click()
        time.sleep(2)
        
        # Verificar que se creó la cuenta exitosamente
        current_url = driver.current_url
        print(f"3. URL después de crear cuenta: {current_url}")
        
        # Buscar mensaje de éxito
        success_message = "Account Opened!" in driver.page_source or "Congratulations" in driver.page_source
        assert success_message, "No se encontró mensaje de confirmación de cuenta creada"
        
        # Verificar que hay un número de cuenta nuevo
        if "newAccountId" in current_url:
            print("✓ Nueva cuenta creada exitosamente")
        else:
            # Buscar el número de cuenta en el contenido
            assert "new account number" in driver.page_source.lower(), "No se encontró el número de cuenta nueva"
            print("✓ Nueva cuenta SAVINGS creada exitosamente")
    
    def test_open_new_checking_account(self, driver, base_url):
        """
        Test 12: Abrir una nueva cuenta corriente (Checking)
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Open New Account
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_open_new_account()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Seleccionar tipo de cuenta (Checking - por defecto)
        account_type_select = Select(driver.find_element(By.ID, "type"))
        current_selection = account_type_select.first_selected_option.text
        print(f"2. Tipo de cuenta seleccionado: {current_selection}")
        
        # Verificar que CHECKING está seleccionado (es el default)
        assert "CHECKING" in current_selection.upper(), "CHECKING no está seleccionado por defecto"
        
        # Click en "Open New Account"
        open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
        open_button.click()
        time.sleep(2)
        
        # Verificar que se creó la cuenta exitosamente
        success_message = "Account Opened!" in driver.page_source or "Congratulations" in driver.page_source
        assert success_message, "No se encontró mensaje de confirmación de cuenta creada"
        
        print("✓ Nueva cuenta CHECKING creada exitosamente")
    
    def test_navigate_to_find_transactions(self, driver, base_url):
        """
        Test 13: Navegar a la página de buscar transacciones
        """
        import time
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Find Transactions
        accounts_page = AccountsOverviewPage(driver)
        print(f"\n1. URL antes del click: {driver.current_url}")
        
        accounts_page.click_find_transactions()
        time.sleep(1)
        
        # Verificar la navegación
        current_url = driver.current_url
        print(f"2. URL después del click: {current_url}")
        
        assert "findtrans.htm" in current_url, f"URL esperada con 'findtrans.htm', pero se obtuvo: {current_url}"
        assert "Find Transactions" in driver.page_source, "No se encontró el título 'Find Transactions'"
        
        print("✓ Navegación a Find Transactions exitosa")
    
    def test_find_transactions_by_id(self, driver, base_url):
        """
        Test 13b: Buscar transacción por ID
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Primero, hacer una transferencia para tener una transacción reciente
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_transfer_funds()
        time.sleep(1)
        
        # Realizar transferencia
        driver.find_element(By.ID, "amount").send_keys("5.00")
        driver.find_element(By.XPATH, "//input[@value='Transfer']").click()
        time.sleep(2)
        
        # Obtener el ID de la transacción si está disponible
        transaction_id = None
        if "Transaction ID:" in driver.page_source or "transfer id" in driver.page_source.lower():
            # Intentar extraer el ID de la transacción
            print("1. Transferencia realizada")
        
        # Navegar a Find Transactions
        accounts_page.click_find_transactions()
        time.sleep(1)
        
        print(f"2. En página: {driver.current_url}")
        
        # Seleccionar una cuenta
        account_select = Select(driver.find_element(By.ID, "accountId"))
        selected_account = account_select.first_selected_option.text
        print(f"3. Cuenta seleccionada: {selected_account}")
        
        # Buscar por ID (usar un ID ficticio para demostrar)
        # Nota: En un test real, usarías el ID de una transacción real
        transaction_id_input = driver.find_element(By.ID, "transactionId")
        transaction_id_input.send_keys("12345")
        print("4. Buscando transacción por ID: 12345")
        
        # Click en Find Transactions by ID (es el primer botón)
        find_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Find Transactions')]")
        if len(find_buttons) > 0:
            find_buttons[0].click()  # Primer botón es para ID
        else:
            # Fallback: buscar cualquier botón de submit
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Verificar que se realizó la búsqueda
        current_url = driver.current_url
        print(f"5. URL después de buscar: {current_url}")
        
        # Puede mostrar "Transaction Results" o "Error!"
        has_results = "Transaction Results" in driver.page_source or "Error!" in driver.page_source or "Could not find" in driver.page_source
        assert has_results, "No se encontró respuesta de búsqueda"
        
        print("✓ Búsqueda por ID ejecutada")
    
    def test_find_transactions_by_date(self, driver, base_url):
        """
        Test 13c: Buscar transacciones por fecha
        """
        import time
        from datetime import datetime
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Find Transactions
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_find_transactions()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Seleccionar una cuenta
        account_select = Select(driver.find_element(By.ID, "accountId"))
        selected_account = account_select.first_selected_option.text
        print(f"2. Cuenta seleccionada: {selected_account}")
        
        # Ingresar fecha (formato MM-DD-YYYY)
        today = datetime.now().strftime("%m-%d-%Y")
        date_input = driver.find_element(By.ID, "transactionDate")
        date_input.send_keys(today)
        print(f"3. Buscando transacciones en fecha: {today}")
        
        # Click en Find Transactions by Date (es el segundo botón)
        find_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Find Transactions')]")
        if len(find_buttons) > 1:
            find_buttons[1].click()  # Segundo botón es para Date
        else:
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Verificar que se realizó la búsqueda
        current_url = driver.current_url
        print(f"4. URL después de buscar: {current_url}")
        
        # Puede mostrar resultados o mensaje de que no hay transacciones
        has_response = "Transaction Results" in driver.page_source or "No transactions found" in driver.page_source or "transactions for" in driver.page_source.lower()
        assert has_response, "No se encontró respuesta de búsqueda"
        
        print("✓ Búsqueda por fecha ejecutada")
    
    def test_find_transactions_by_date_range(self, driver, base_url):
        """
        Test 13d: Buscar transacciones por rango de fechas
        """
        import time
        from datetime import datetime, timedelta
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Find Transactions
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_find_transactions()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Seleccionar una cuenta
        account_select = Select(driver.find_element(By.ID, "accountId"))
        selected_account = account_select.first_selected_option.text
        print(f"2. Cuenta seleccionada: {selected_account}")
        
        # Ingresar rango de fechas (últimos 30 días)
        today = datetime.now()
        from_date = (today - timedelta(days=30)).strftime("%m-%d-%Y")
        to_date = today.strftime("%m-%d-%Y")
        
        from_date_input = driver.find_element(By.ID, "fromDate")
        from_date_input.send_keys(from_date)
        
        to_date_input = driver.find_element(By.ID, "toDate")
        to_date_input.send_keys(to_date)
        
        print(f"3. Buscando transacciones desde {from_date} hasta {to_date}")
        
        # Click en Find Transactions by Date Range (es el tercer botón)
        find_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Find Transactions')]")
        if len(find_buttons) > 2:
            find_buttons[2].click()  # Tercer botón es para Date Range
        else:
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Verificar que se realizó la búsqueda
        current_url = driver.current_url
        print(f"4. URL después de buscar: {current_url}")
        
        # Puede mostrar resultados o mensaje de que no hay transacciones
        has_response = "Transaction Results" in driver.page_source or "No transactions found" in driver.page_source or "transactions for" in driver.page_source.lower()
        assert has_response, "No se encontró respuesta de búsqueda"
        
        print("✓ Búsqueda por rango de fechas ejecutada")
    
    def test_find_transactions_by_amount(self, driver, base_url):
        """
        Test 13e: Buscar transacciones por monto
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Find Transactions
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_find_transactions()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Seleccionar una cuenta
        account_select = Select(driver.find_element(By.ID, "accountId"))
        selected_account = account_select.first_selected_option.text
        print(f"2. Cuenta seleccionada: {selected_account}")
        
        # Ingresar monto a buscar
        amount = "10.00"
        amount_input = driver.find_element(By.ID, "amount")
        amount_input.send_keys(amount)
        print(f"3. Buscando transacciones por monto: ${amount}")
        
        # Click en Find Transactions by Amount (es el cuarto botón)
        find_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Find Transactions')]")
        if len(find_buttons) > 3:
            find_buttons[3].click()  # Cuarto botón es para Amount
        else:
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Verificar que se realizó la búsqueda
        current_url = driver.current_url
        print(f"4. URL después de buscar: {current_url}")
        
        # Puede mostrar resultados o mensaje de que no hay transacciones
        has_response = "Transaction Results" in driver.page_source or "No transactions found" in driver.page_source or "transactions for" in driver.page_source.lower()
        assert has_response, "No se encontró respuesta de búsqueda"
        
        print("✓ Búsqueda por monto ejecutada")
    
    def test_update_contact_info_street(self, driver, base_url):
        """
        Test 15: Actualizar información de contacto - cambiar calle (street)
        """
        import time
        from selenium.webdriver.common.by import By
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Update Contact Info
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_update_contact_info()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Verificar que estamos en Update Contact Info
        assert "updateprofile" in driver.current_url.lower()
        print("2. Página Update Contact Info cargada")
        
        # Obtener el valor actual de street
        street_input = driver.find_element(By.ID, "customer.address.street")
        current_street = street_input.get_attribute("value")
        print(f"3. Calle actual: {current_street}")
        
        # Cambiar la calle
        new_street = "123 New Street Avenue"
        street_input.clear()
        street_input.send_keys(new_street)
        print(f"4. Nueva calle ingresada: {new_street}")
        
        # Hacer scroll al botón y hacer click
        update_button = driver.find_element(By.CSS_SELECTOR, "input[value='Update Profile']")
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button)
        time.sleep(0.5)
        update_button.click()
        time.sleep(2)
        
        # Verificar que se actualizó correctamente
        current_url = driver.current_url
        print(f"5. URL después de actualizar: {current_url}")
        
        # Verificar mensaje de éxito
        success_message = "Profile Updated" in driver.page_source or "Your updated address and phone number have been added to the system" in driver.page_source
        assert success_message, "No se encontró mensaje de éxito al actualizar perfil"
        
        print("✓ Información de contacto actualizada exitosamente")
    
    def test_navigate_to_request_loan(self, driver, base_url):
        """
        Test 16a: Navegar a Request Loan
        """
        import time
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Request Loan
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_request_loan()
        time.sleep(1)
        
        # Verificar que estamos en Request Loan
        assert "requestloan" in driver.current_url.lower()
        assert "Apply for a Loan" in driver.page_source
        print("\n✓ Navegación a Request Loan exitosa")
    
    def test_request_loan_successful(self, driver, base_url):
        """
        Test 16b: Solicitar préstamo exitosamente
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Request Loan
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_request_loan()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Ingresar monto del préstamo
        loan_amount = "1000"
        amount_input = driver.find_element(By.ID, "amount")
        amount_input.send_keys(loan_amount)
        print(f"2. Monto solicitado: ${loan_amount}")
        
        # Ingresar down payment
        down_payment = "100"
        down_payment_input = driver.find_element(By.ID, "downPayment")
        down_payment_input.send_keys(down_payment)
        print(f"3. Down payment: ${down_payment}")
        
        # Seleccionar cuenta para el down payment
        from_account_select = Select(driver.find_element(By.ID, "fromAccountId"))
        selected_account = from_account_select.first_selected_option.text
        print(f"4. Cuenta seleccionada: {selected_account}")
        
        # Click en Apply Now
        apply_button = driver.find_element(By.CSS_SELECTOR, "input[value='Apply Now']")
        apply_button.click()
        time.sleep(2)
        
        # Verificar que se procesó la solicitud
        current_url = driver.current_url
        print(f"5. URL después de solicitar: {current_url}")
        
        # Puede ser aprobado o denegado
        has_response = "Loan Request Processed" in driver.page_source or "Congratulations" in driver.page_source or "denied" in driver.page_source.lower()
        assert has_response, "No se encontró respuesta de solicitud de préstamo"
        
        print("✓ Solicitud de préstamo procesada")
    
    def test_request_loan_empty_fields(self, driver, base_url):
        """
        Test 16c: Intentar solicitar préstamo con campos vacíos
        """
        import time
        from selenium.webdriver.common.by import By
        
        driver.get(base_url)
        login_page = LoginPage(driver)
        
        # Login
        login_page.login(self.VALID_USERNAME, self.VALID_PASSWORD)
        time.sleep(1)
        
        # Navegar a Request Loan
        accounts_page = AccountsOverviewPage(driver)
        accounts_page.click_request_loan()
        time.sleep(1)
        
        print(f"\n1. En página: {driver.current_url}")
        
        # Click en Apply Now sin llenar campos
        apply_button = driver.find_element(By.CSS_SELECTOR, "input[value='Apply Now']")
        apply_button.click()
        time.sleep(1)
        
        # Verificar que se muestran errores de validación o se queda en la misma página
        still_in_request = "Apply for a Loan" in driver.page_source or "requestloan" in driver.current_url.lower()
        assert still_in_request, "No se detectó validación de campos vacíos"
        
        print("2. ✓ Validación de campos vacíos funcionando")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])
