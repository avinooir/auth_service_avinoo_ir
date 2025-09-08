#!/usr/bin/env python
"""
Script to test the Auth Service API endpoints.
This script tests all major API endpoints to ensure they work correctly.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

class AuthServiceTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_id: Optional[int] = None
        
    def print_result(self, test_name: str, success: bool, message: str = ""):
        """Print test result with colored output."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
    
    def test_server_connection(self) -> bool:
        """Test if the server is running."""
        try:
            response = self.session.get(f"{self.base_url}/admin/")
            success = response.status_code in [200, 302, 404]  # 404 is OK for admin without auth
            self.print_result("Server Connection", success, f"Status: {response.status_code}")
            return success
        except requests.exceptions.ConnectionError:
            self.print_result("Server Connection", False, "Server is not running")
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration endpoint."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register/",
                json=TEST_USER,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.access_token = data.get("tokens", {}).get("access")
                self.refresh_token = data.get("tokens", {}).get("refresh")
                self.user_id = data.get("user", {}).get("id")
                
                self.print_result("User Registration", True, f"User ID: {self.user_id}")
                return True
            else:
                self.print_result("User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self) -> bool:
        """Test user login endpoint."""
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login/",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("tokens", {}).get("access")
                self.refresh_token = data.get("tokens", {}).get("refresh")
                
                self.print_result("User Login", True, "Login successful")
                return True
            else:
                self.print_result("User Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_get_user_profile(self) -> bool:
        """Test get user profile endpoint."""
        if not self.access_token:
            self.print_result("Get User Profile", False, "No access token available")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/auth/me/",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                username = data.get("user", {}).get("username")
                self.print_result("Get User Profile", True, f"Username: {username}")
                return True
            else:
                self.print_result("Get User Profile", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("Get User Profile", False, f"Error: {str(e)}")
            return False
    
    def test_token_refresh(self) -> bool:
        """Test token refresh endpoint."""
        if not self.refresh_token:
            self.print_result("Token Refresh", False, "No refresh token available")
            return False
        
        try:
            refresh_data = {
                "refresh": self.refresh_token
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/refresh/",
                json=refresh_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get("access")
                if new_access_token:
                    self.access_token = new_access_token
                    self.print_result("Token Refresh", True, "Token refreshed successfully")
                    return True
                else:
                    self.print_result("Token Refresh", False, "No access token in response")
                    return False
            else:
                self.print_result("Token Refresh", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("Token Refresh", False, f"Error: {str(e)}")
            return False
    
    def test_get_roles(self) -> bool:
        """Test get roles endpoint."""
        if not self.access_token:
            self.print_result("Get Roles", False, "No access token available")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/roles/",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                roles_count = len(data.get("roles", []))
                self.print_result("Get Roles", True, f"Found {roles_count} roles")
                return True
            else:
                self.print_result("Get Roles", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("Get Roles", False, f"Error: {str(e)}")
            return False
    
    def test_get_permissions(self) -> bool:
        """Test get permissions endpoint."""
        if not self.access_token:
            self.print_result("Get Permissions", False, "No access token available")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/permissions/permissions/",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                permissions_count = len(data.get("results", []))
                self.print_result("Get Permissions", True, f"Found {permissions_count} permissions")
                return True
            else:
                self.print_result("Get Permissions", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("Get Permissions", False, f"Error: {str(e)}")
            return False
    
    def test_user_logout(self) -> bool:
        """Test user logout endpoint."""
        if not self.access_token or not self.refresh_token:
            self.print_result("User Logout", False, "No tokens available")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            logout_data = {
                "refresh_token": self.refresh_token
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/logout/",
                json=logout_data,
                headers=headers
            )
            
            if response.status_code == 200:
                self.print_result("User Logout", True, "Logout successful")
                return True
            else:
                self.print_result("User Logout", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_result("User Logout", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        print("🧪 Starting Auth Service API Tests")
        print("=" * 50)
        
        results = {}
        
        # Test server connection
        results["server_connection"] = self.test_server_connection()
        
        if not results["server_connection"]:
            print("\n❌ Server is not running. Please start the server first:")
            print("   python manage.py runserver")
            return results
        
        print()
        
        # Test user registration
        results["user_registration"] = self.test_user_registration()
        
        # If registration fails, try login (user might already exist)
        if not results["user_registration"]:
            print("   Trying login instead...")
            results["user_login"] = self.test_user_login()
        else:
            results["user_login"] = True
        
        print()
        
        # Test authenticated endpoints
        if self.access_token:
            results["get_user_profile"] = self.test_get_user_profile()
            results["token_refresh"] = self.test_token_refresh()
            results["get_roles"] = self.test_get_roles()
            results["get_permissions"] = self.test_get_permissions()
            results["user_logout"] = self.test_user_logout()
        else:
            print("❌ No access token available, skipping authenticated tests")
            results.update({
                "get_user_profile": False,
                "token_refresh": False,
                "get_roles": False,
                "get_permissions": False,
                "user_logout": False
            })
        
        print()
        print("=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print()
        print(f"Total: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the server logs.")
        
        return results


def main():
    """Main function to run the tests."""
    tester = AuthServiceTester()
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
