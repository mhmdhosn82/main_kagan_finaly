#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities Module
Common utilities, logging, validation, and helper functions
"""

import os
import logging
import re
from datetime import datetime
from pathlib import Path


def setup_logging():
    """
    Setup logging configuration for the application
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create log file path with date
    log_file = log_dir / f'kagan_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")


class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate Iranian phone number
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not phone:
            return False
        
        # Remove spaces and dashes
        phone = phone.replace(' ', '').replace('-', '')
        
        # Check Iranian mobile number format (09xx-xxx-xxxx)
        mobile_pattern = r'^09\d{9}$'
        
        # Check Iranian landline format (0xx-xxxx-xxxx)
        landline_pattern = r'^0\d{10}$'
        
        return bool(re.match(mobile_pattern, phone) or re.match(landline_pattern, phone))
    
    @staticmethod
    def validate_email(email):
        """
        Validate email address
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_required(value, field_name="این فیلد"):
        """
        Validate that a field is not empty
        
        Args:
            value: Value to check
            field_name (str): Field name for error message
            
        Raises:
            ValueError: If value is empty
        """
        if not value or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{field_name} الزامی است")
    
    @staticmethod
    def validate_positive_number(value, field_name="مقدار"):
        """
        Validate that a number is positive
        
        Args:
            value: Value to check
            field_name (str): Field name for error message
            
        Raises:
            ValueError: If value is not positive
        """
        try:
            num = float(value)
            if num < 0:
                raise ValueError(f"{field_name} باید مثبت باشد")
            return num
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} باید یک عدد معتبر باشد")
    
    @staticmethod
    def validate_integer(value, field_name="مقدار"):
        """
        Validate that a value is an integer
        
        Args:
            value: Value to check
            field_name (str): Field name for error message
            
        Returns:
            int: The validated integer value
            
        Raises:
            ValueError: If value is not a valid integer
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} باید یک عدد صحیح باشد")


class DateFormatter:
    """Date formatting utilities"""
    
    @staticmethod
    def format_datetime(dt, format_str="%Y-%m-%d %H:%M"):
        """
        Format datetime to string
        
        Args:
            dt (datetime): Datetime object
            format_str (str): Format string
            
        Returns:
            str: Formatted datetime string
        """
        if dt is None:
            return ""
        return dt.strftime(format_str)
    
    @staticmethod
    def format_date(dt):
        """Format datetime to date string"""
        return DateFormatter.format_datetime(dt, "%Y-%m-%d")
    
    @staticmethod
    def format_time(dt):
        """Format datetime to time string"""
        return DateFormatter.format_datetime(dt, "%H:%M")
    
    @staticmethod
    def parse_date(date_str, format_str="%Y-%m-%d"):
        """
        Parse date string to datetime
        
        Args:
            date_str (str): Date string
            format_str (str): Format string
            
        Returns:
            datetime: Parsed datetime object
        """
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError:
            return None


class NumberFormatter:
    """Number formatting utilities"""
    
    @staticmethod
    def format_currency(amount, currency="ریال"):
        """
        Format number as currency
        
        Args:
            amount (float): Amount to format
            currency (str): Currency symbol
            
        Returns:
            str: Formatted currency string
        """
        if amount is None:
            return "0 " + currency
        
        # Format with thousand separators
        formatted = "{:,.0f}".format(amount)
        return f"{formatted} {currency}"
    
    @staticmethod
    def format_number(number, decimals=2):
        """
        Format number with decimals
        
        Args:
            number (float): Number to format
            decimals (int): Number of decimal places
            
        Returns:
            str: Formatted number string
        """
        if number is None:
            return "0"
        
        return f"{number:,.{decimals}f}"


def generate_invoice_number(prefix="INV"):
    """
    Generate unique invoice number
    
    Args:
        prefix (str): Invoice number prefix
        
    Returns:
        str: Generated invoice number
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"


def calculate_tax(amount, tax_rate=9.0):
    """
    Calculate tax amount
    
    Args:
        amount (float): Amount to calculate tax on
        tax_rate (float): Tax rate percentage (default 9%)
        
    Returns:
        float: Tax amount
    """
    return round(amount * (tax_rate / 100), 2)


def calculate_discount(amount, discount_percentage=0, discount_amount=0):
    """
    Calculate discount
    
    Args:
        amount (float): Original amount
        discount_percentage (float): Discount percentage
        discount_amount (float): Fixed discount amount
        
    Returns:
        float: Discount amount
    """
    discount = discount_amount
    
    if discount_percentage > 0:
        discount += amount * (discount_percentage / 100)
    
    return round(min(discount, amount), 2)


def is_stock_low(current_stock, min_level):
    """
    Check if stock level is low
    
    Args:
        current_stock (int): Current stock quantity
        min_level (int): Minimum stock level
        
    Returns:
        bool: True if stock is low
    """
    return current_stock <= min_level
