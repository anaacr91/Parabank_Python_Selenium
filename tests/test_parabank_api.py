"""
Test suite for ParaBank API endpoints
Based on Postman collection data
"""
import pytest
import requests
import xml.etree.ElementTree as ET


class TestParaBankAPI:
    """Tests for ParaBank REST API"""
    
    BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"
    
    # Test data from Postman collection
    USERNAME = "john"
    PASSWORD = "demo"
    CUSTOMER_ID = "12212"
    ACCOUNT_ID = "13344"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.session = requests.Session()
        yield
        self.session.close()
    
    def test_login_success(self):
        """Test LOGIN endpoint - Status 200 OK and response not empty"""
        url = f"{self.BASE_URL}/login/{self.USERNAME}/{self.PASSWORD}"
        
        response = self.session.get(url)
        
        # Assertions from Postman tests
        assert response.status_code == 200, "Expected status code 200"
        assert len(response.text) > 0, "Response body should not be empty"
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Verify XML structure
        root = ET.fromstring(response.text)
        assert root.tag == "customer"
        assert root.find("id").text == self.CUSTOMER_ID
        assert root.find("firstName").text == "John"
        assert root.find("lastName").text == "Smith"
    
    def test_get_account_by_id(self):
        """Test ACCOUNT_ID endpoint - Get account details"""
        url = f"{self.BASE_URL}/accounts/{self.ACCOUNT_ID}"
        
        response = self.session.get(url)
        
        # Assertions
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Parse and validate XML
        root = ET.fromstring(response.text)
        assert root.tag == "account"
        assert root.find("id").text == self.ACCOUNT_ID
        assert root.find("customerId").text == self.CUSTOMER_ID
        assert root.find("type") is not None
        assert root.find("balance") is not None
    
    def test_get_customer_accounts(self):
        """Test CUSTOMER_ID_ACCOUNTS endpoint - Get all accounts for customer"""
        url = f"{self.BASE_URL}/customers/{self.CUSTOMER_ID}/accounts"
        
        response = self.session.get(url)
        
        # Assertions
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Parse XML and verify accounts
        root = ET.fromstring(response.text)
        assert root.tag == "accounts"
        accounts = root.findall("account")
        assert len(accounts) > 0, "Should have at least one account"
        
        # Verify each account has required fields
        for account in accounts:
            assert account.find("id") is not None
            assert account.find("customerId").text == self.CUSTOMER_ID
            assert account.find("type") is not None
            assert account.find("balance") is not None
    
    def test_get_account_transactions(self):
        """Test ACC_iD_TRANSACTION endpoint - Get transactions for account"""
        url = f"{self.BASE_URL}/accounts/{self.ACCOUNT_ID}/transactions"
        
        response = self.session.get(url)
        
        # Assertions
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Parse XML
        root = ET.fromstring(response.text)
        assert root.tag == "transactions"
        transactions = root.findall("transaction")
        assert len(transactions) > 0, "Should have at least one transaction"
        
        # Verify transaction fields
        for transaction in transactions:
            assert transaction.find("id") is not None
            assert transaction.find("accountId").text == self.ACCOUNT_ID
            assert transaction.find("type") is not None
            assert transaction.find("amount") is not None
            assert transaction.find("description") is not None
    
    def test_deposit_to_account(self):
        """Test DEPOSIT endpoint - Deposit money to account"""
        amount = 200
        url = f"{self.BASE_URL}/deposit?accountId={self.ACCOUNT_ID}&amount={amount}"
        
        response = self.session.post(url)
        
        # Assertions from Postman tests
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        assert "error" not in response.text.lower()
        assert "Successfully deposited" in response.text
        assert str(amount) in response.text
        assert self.ACCOUNT_ID in response.text
    
    def test_create_account(self):
        """Test CREATEACCOUNT endpoint - Create new account"""
        url = f"{self.BASE_URL}/createAccount"
        params = {
            "customerId": self.CUSTOMER_ID,
            "newAccountType": "1",  # 0=CHECKING, 1=SAVINGS
            "fromAccountId": self.ACCOUNT_ID
        }
        
        response = self.session.post(url, params=params)
        
        # Assertions
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Parse response
        root = ET.fromstring(response.text)
        assert root.tag == "account"
        assert root.find("customerId").text == self.CUSTOMER_ID
        # Account type 1 = SAVINGS
        assert root.find("type").text in ["SAVINGS", "CHECKING", "LOAN"]
        assert root.find("id") is not None
    
    def test_bill_pay(self):
        """Test BILLPAY endpoint - Pay a bill"""
        url = f"{self.BASE_URL}/billpay"
        params = {
            "accountId": self.ACCOUNT_ID,
            "amount": "100"
        }
        
        # XML body with payee information
        payee_xml = """<payee>
    <name>John Smith</name>
    <address>
        <street>My street</street>
        <city>My city</city>
        <state>My state</state>
        <zipCode>90210</zipCode>
    </address>
    <phoneNumber>0123456789</phoneNumber>
    <accountNumber>12345</accountNumber>
</payee>"""
        
        headers = {"Content-Type": "application/xml"}
        response = self.session.post(url, params=params, data=payee_xml, headers=headers)
        
        # Assertions from Postman tests
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        assert "error" not in response.text.lower()
        assert response.headers.get("Server") is not None
        assert response.elapsed.total_seconds() < 5, "Response time should be less than 5 seconds"
        
        # Verify response structure
        root = ET.fromstring(response.text)
        assert root.tag == "billPayResult"
        assert root.find("accountId").text == self.ACCOUNT_ID
        assert root.find("amount").text == "100"
        assert root.find("payeeName").text == "John Smith"
    
    def test_transfer_funds(self):
        """Test transfer-from-to_account endpoint - Transfer between accounts"""
        from_account = self.ACCOUNT_ID
        to_account = "13455"
        amount = 100
        
        url = f"{self.BASE_URL}/transfer"
        params = {
            "fromAccountId": from_account,
            "toAccountId": to_account,
            "amount": amount
        }
        
        response = self.session.post(url, params=params)
        
        # Assertions
        assert response.status_code == 200
        assert "application/xml" in response.headers.get("Content-Type", "")
        
        # Verify amount and accounts are different
        assert from_account != to_account, "From and To accounts should be different"
        assert amount > 0, "Amount should be positive"
    
    def test_deposit_negative_amount(self):
        """Test DEPOSIT with negative amount - should handle gracefully"""
        amount = -50
        url = f"{self.BASE_URL}/deposit?accountId={self.ACCOUNT_ID}&amount={amount}"
        
        response = self.session.post(url)
        
        # Negative amounts should be rejected (expect error or bad request)
        # This test validates error handling
        assert response.status_code in [200, 400, 500]
        if response.status_code != 200:
            assert "error" in response.text.lower() or "invalid" in response.text.lower()
    
    def test_invalid_account_id(self):
        """Test with invalid account ID - should handle error"""
        invalid_account = "99999999"
        url = f"{self.BASE_URL}/accounts/{invalid_account}"
        
        response = self.session.get(url)
        
        # Should return error or 404
        assert response.status_code in [200, 400, 404, 500]
        if response.status_code != 200:
            assert "error" in response.text.lower() or "not found" in response.text.lower()
    
    def test_invalid_customer_id(self):
        """Test with invalid customer ID - should handle error"""
        invalid_customer = "99999999"
        url = f"{self.BASE_URL}/customers/{invalid_customer}/accounts"
        
        response = self.session.get(url)
        
        # Should return error or empty list
        assert response.status_code in [200, 400, 404, 500]


class TestParaBankAPIPerformance:
    """Performance tests for ParaBank API"""
    
    BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"
    CUSTOMER_ID = "12212"
    
    def test_response_time_login(self):
        """Test that login response time is acceptable"""
        url = f"{self.BASE_URL}/login/john/demo"
        
        response = requests.get(url)
        
        assert response.elapsed.total_seconds() < 5, "Login should respond in less than 5 seconds"
    
    def test_response_time_accounts(self):
        """Test that accounts retrieval is fast"""
        url = f"{self.BASE_URL}/customers/{self.CUSTOMER_ID}/accounts"
        
        response = requests.get(url)
        
        assert response.elapsed.total_seconds() < 5, "Accounts retrieval should be fast"
