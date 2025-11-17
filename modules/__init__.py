#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modules package for Kagan Business Management System
Contains all business module sections
"""

from .salon_section import SalonSection
from .cafe_section import CafeSection
from .gamnet_section import GamnetSection
from .inventory_section import InventorySection
from .invoice_section import InvoiceSection
from .customer_section import CustomerSection
from .employee_section import EmployeeSection
from .reports_section import ReportsSection
from .supplier_expense_section import SupplierExpenseSection
from .campaign_section import CampaignSection
from .sms_section import SmsSection
from .sms_service import SmsService
from .settings_section import SettingsSection

__all__ = [
    'SalonSection',
    'CafeSection',
    'GamnetSection',
    'InventorySection',
    'InvoiceSection',
    'CustomerSection',
    'EmployeeSection',
    'ReportsSection',
    'SupplierExpenseSection',
    'CampaignSection',
    'SmsSection',
    'SmsService',
    'SettingsSection',
]
