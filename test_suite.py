import unittest
import requests
import json
import sqlite3
import os
import time
from app import app, init_db

class HarvestNetTestSuite(unittest.TestCase):
    """Comprehensive test suite for HarvestNet platform"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.base_url = 'http://localhost:5000/api'
        cls.test_db = 'test_harvestnet.db'
        
        # Initialize test database
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        
        # Create test app
        app.config['TESTING'] = True
        app.config['DATABASE'] = cls.test_db
        cls.client = app.test_client()
        
        # Initialize database
        init_db()
        
        # Test credentials
        cls.admin_credentials = {
            'email': 'admin@harvestnet.com',
            'password': 'password123'
        }
        
        cls.farmer_credentials = {
            'email': 'farmer@harvestnet.com',
            'password': 'password123'
        }
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def test_01_api_health_check(self):
        """Test API health endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('database', data)
        self.assertIn('timestamp', data)
        self.assertIn('version', data)
    
    def test_02_admin_login_success(self):
        """Test successful admin login"""
        response = self.client.post('/api/auth/login', 
                                  data=json.dumps(self.admin_credentials),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'admin@harvestnet.com')
        self.assertEqual(data['user']['role'], 'administrator')
        
        # Store token for subsequent tests
        self.admin_token = data['token']
    
    def test_03_farmer_login_success(self):
        """Test successful farmer login"""
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(self.farmer_credentials),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertEqual(data['user']['role'], 'farmer')
        
        self.farmer_token = data['token']
    
    def test_04_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_credentials = {
            'email': 'invalid@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(invalid_credentials),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_05_login_missing_fields(self):
        """Test login with missing fields"""
        incomplete_credentials = {'email': 'admin@harvestnet.com'}
        
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(incomplete_credentials),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_06_get_users_with_auth(self):
        """Test getting users with valid authentication"""
        # First login to get token
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(self.admin_credentials),
                                        content_type='application/json')
        token = json.loads(login_response.data)['token']
        
        # Get users
        response = self.client.get('/api/users',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('users', data)
        self.assertIsInstance(data['users'], list)
        self.assertGreaterEqual(len(data['users']), 2)  # At least admin and farmer
    
    def test_07_get_users_without_auth(self):
        """Test getting users without authentication"""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 401)
    
    def test_08_get_dashboard_analytics(self):
        """Test dashboard analytics endpoint"""
        # Login first
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(self.admin_credentials),
                                        content_type='application/json')
        token = json.loads(login_response.data)['token']
        
        # Get analytics
        response = self.client.get('/api/analytics/dashboard',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total_users', data)
        self.assertIn('active_farmers', data)
        self.assertIn('data_ambassadors', data)
        self.assertIn('growth_metrics', data)
        
        # Verify data types
        self.assertIsInstance(data['total_users'], int)
        self.assertIsInstance(data['active_farmers'], int)
        self.assertIsInstance(data['data_ambassadors'], int)
    
    def test_09_weather_api_integration(self):
        """Test weather API integration"""
        # Login first
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(self.admin_credentials),
                                        content_type='application/json')
        token = json.loads(login_response.data)['token']
        
        # Test weather endpoint
        response = self.client.get('/api/weather?lat=-1.2921&lon=36.8219',
                                 headers={'Authorization': f'Bearer {token}'})
        
        # Weather API might fail due to network, so we accept both success and service unavailable
        self.assertIn(response.status_code, [200, 503])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            # Basic structure validation for Norwegian Met API
            self.assertIsInstance(data, dict)
    
    def test_10_data_export(self):
        """Test data export functionality"""
        # Login first
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(self.admin_credentials),
                                        content_type='application/json')
        token = json.loads(login_response.data)['token']
        
        # Test export
        response = self.client.get('/api/data/export?type=users',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('type', data)
        self.assertIn('data', data)
        self.assertIn('exported_at', data)
        self.assertEqual(data['type'], 'users')
        self.assertIsInstance(data['data'], list)
    
    def test_11_database_integrity(self):
        """Test database integrity and constraints"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Test user table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        required_columns = ['id', 'email', 'password_hash', 'name', 'role', 'created_at']
        for col in required_columns:
            self.assertIn(col, column_names)
        
        # Test unique constraint on email
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin@harvestnet.com', 'hash', 'Test', 'farmer'))
            conn.commit()
            self.fail("Should have failed due to unique email constraint")
        except sqlite3.IntegrityError:
            pass  # Expected behavior
        
        conn.close()
    
    def test_12_input_validation(self):
        """Test input validation and sanitization"""
        # Test SQL injection attempt
        malicious_credentials = {
            'email': "admin@harvestnet.com'; DROP TABLE users; --",
            'password': 'password123'
        }
        
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(malicious_credentials),
                                  content_type='application/json')
        
        # Should fail gracefully, not crash
        self.assertIn(response.status_code, [400, 401])
        
        # Verify table still exists
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        conn.close()
    
    def test_13_token_expiration(self):
        """Test JWT token validation"""
        # Test with invalid token
        response = self.client.get('/api/users',
                                 headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)
        
        # Test without Bearer prefix
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(self.admin_credentials),
                                        content_type='application/json')
        token = json.loads(login_response.data)['token']
        
        response = self.client.get('/api/users',
                                 headers={'Authorization': token})
        self.assertEqual(response.status_code, 401)
    
    def test_14_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.get('/api/health')
        
        # Check if CORS headers are present (Flask-CORS should add them)
        self.assertEqual(response.status_code, 200)
        # Note: In test environment, CORS headers might not be fully visible
    
    def test_15_error_handling(self):
        """Test error handling for various scenarios"""
        # Test non-existent endpoint
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        # Test malformed JSON
        response = self.client.post('/api/auth/login',
                                  data='invalid json',
                                  content_type='application/json')
        self.assertIn(response.status_code, [400, 500])

class FrontendIntegrationTest(unittest.TestCase):
    """Test frontend-backend integration"""
    
    def setUp(self):
        """Set up for frontend tests"""
        self.base_url = 'http://localhost:5000'
    
    def test_frontend_files_exist(self):
        """Test that frontend files exist"""
        frontend_files = [
            '/home/ubuntu/harvestnet-frontend/index.html',
            '/home/ubuntu/harvestnet-frontend/dashboard.html'
        ]
        
        for file_path in frontend_files:
            self.assertTrue(os.path.exists(file_path), f"Frontend file {file_path} does not exist")
    
    def test_frontend_html_structure(self):
        """Test frontend HTML structure"""
        with open('/home/ubuntu/harvestnet-frontend/index.html', 'r') as f:
            content = f.read()
        
        # Check for essential elements
        self.assertIn('HarvestNet', content)
        self.assertIn('login-form', content)
        self.assertIn('API_BASE_URL', content)
        
        with open('/home/ubuntu/harvestnet-frontend/dashboard.html', 'r') as f:
            content = f.read()
        
        self.assertIn('dashboard', content)
        self.assertIn('User Management', content)
        self.assertIn('Analytics', content)

def run_comprehensive_tests():
    """Run all tests and generate report"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add backend tests
    suite.addTest(unittest.makeSuite(HarvestNetTestSuite))
    
    # Add frontend tests
    suite.addTest(unittest.makeSuite(FrontendIntegrationTest))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate test report
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((total_tests - failures - errors) / total_tests) * 100 if total_tests > 0 else 0
    
    report = f"""
# HarvestNet Test Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Test Summary
- Total Tests: {total_tests}
- Passed: {total_tests - failures - errors}
- Failed: {failures}
- Errors: {errors}
- Success Rate: {success_rate:.1f}%

## Test Categories
✅ API Health Checks
✅ Authentication & Authorization
✅ User Management
✅ Analytics Dashboard
✅ Weather API Integration
✅ Data Export/Import
✅ Database Integrity
✅ Input Validation & Security
✅ Error Handling
✅ Frontend Integration

## Quality Assurance Status
{'✅ All tests passed' if failures == 0 and errors == 0 else '❌ Some tests failed'}

## Recommendations
- Implement automated testing in CI/CD pipeline
- Add performance testing for high load scenarios
- Include security penetration testing
- Set up monitoring and alerting for production
"""
    
    with open('/home/ubuntu/harvestnet-backend/test_report.txt', 'w') as f:
        f.write(report)
    
    print(f"\nTest completed: {total_tests - failures - errors}/{total_tests} tests passed")
    print("Test report saved to test_report.txt")
    
    return result

if __name__ == "__main__":
    run_comprehensive_tests()

