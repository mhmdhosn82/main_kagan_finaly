#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify all components of the Kagan Business Management System
"""

import sys
import os

# Set QT platform for headless testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from gui import MainWindow, LoginDialog
        from modules.salon_section import SalonSection
        from modules.cafe_section import CafeSection
        from modules.gamnet_section import GamnetSection
        from modules.inventory_section import InventorySection
        from modules.invoice_section import InvoiceSection
        from modules.customer_section import CustomerSection
        from modules.employee_section import EmployeeSection
        from modules.reports_section import ReportsSection
        from modules.supplier_expense_section import SupplierExpenseSection
        from modules.campaign_section import CampaignSection
        from modules.sms_section import SmsSection
        from modules.sms_service import SmsService
        from modules.settings_section import SettingsSection
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_login_dialog():
    """Test login dialog creation"""
    print("\nTesting login dialog...")
    try:
        from gui import LoginDialog
        app = QApplication(sys.argv)
        login = LoginDialog()
        
        # Check properties
        assert login.windowTitle() == "ورود به سیستم - Kagan"
        assert login.width() == 400
        assert login.height() == 300
        
        print("✓ Login dialog created successfully")
        print(f"  - Title: {login.windowTitle()}")
        print(f"  - Size: {login.width()}x{login.height()}")
        return True
    except Exception as e:
        print(f"✗ Login dialog test failed: {e}")
        return False


def test_main_window():
    """Test main window creation"""
    print("\nTesting main window...")
    try:
        from gui import MainWindow
        app = QApplication(sys.argv)
        window = MainWindow()
        
        # Check properties
        assert window.windowTitle() == "سیستم مدیریت کاگان - Kagan Business Manager"
        assert window.minimumWidth() == 1200
        assert window.minimumHeight() == 700
        
        print("✓ Main window created successfully")
        print(f"  - Title: {window.windowTitle()}")
        print(f"  - Minimum size: {window.minimumWidth()}x{window.minimumHeight()}")
        return True
    except Exception as e:
        print(f"✗ Main window test failed: {e}")
        return False


def test_modules():
    """Test that all modules are loaded"""
    print("\nTesting modules...")
    try:
        from gui import MainWindow
        app = QApplication(sys.argv)
        window = MainWindow()
        
        # Expected modules
        expected_modules = [
            'salon', 'cafe', 'gamnet', 'inventory', 'invoice', 
            'customer', 'employee', 'reports', 'supplier_expense', 
            'campaign', 'sms', 'settings'
        ]
        
        # Check all modules exist
        for module_id in expected_modules:
            assert module_id in window.modules, f"Module {module_id} not found"
        
        print(f"✓ All {len(window.modules)} modules loaded successfully")
        for module_id in expected_modules:
            print(f"  - {module_id}")
        return True
    except Exception as e:
        print(f"✗ Modules test failed: {e}")
        return False


def test_sms_service():
    """Test SMS service functionality"""
    print("\nTesting SMS service...")
    try:
        from modules.sms_service import SmsService
        
        service = SmsService()
        service.configure("test_api_key", "https://api.example.com", "1234567890")
        
        # Test send_sms
        result = service.send_sms("09123456789", "Test message")
        assert result == True
        
        # Test get_balance
        balance = service.get_balance()
        assert balance == 1000
        
        print("✓ SMS service tested successfully")
        print(f"  - Balance: {balance}")
        return True
    except Exception as e:
        print(f"✗ SMS service test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Kagan Business Management System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_login_dialog,
        test_main_window,
        test_modules,
        test_sms_service,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
