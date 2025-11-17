#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Models
SQLAlchemy ORM models for all entities
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User roles enumeration"""
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STAFF, nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role.value}')>"


class Customer(Base):
    """Customer model"""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    address = Column(Text)
    loyalty_points = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")
    gaming_sessions = relationship("GamingSession", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer(name='{self.name}', phone='{self.phone}')>"


class Employee(Base):
    """Employee model"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    position = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    salary = Column(Float)
    hire_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    appointments = relationship("Appointment", back_populates="stylist")
    
    def __repr__(self):
        return f"<Employee(name='{self.name}', position='{self.position}')>"


class Service(Base):
    """Service model for salon services"""
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration = Column(Integer)  # in minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="service")
    
    def __repr__(self):
        return f"<Service(name='{self.name}', price={self.price})>"


class Appointment(Base):
    """Appointment model for salon bookings"""
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    stylist_id = Column(Integer, ForeignKey('employees.id'))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    stylist = relationship("Employee", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, date='{self.appointment_date}')>"


class Product(Base):
    """Product model for inventory"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # cafe, salon, general
    description = Column(Text)
    price = Column(Float, nullable=False)
    cost = Column(Float)
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)
    unit = Column(String(20))  # kg, liter, piece, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
    invoice_items = relationship("InvoiceItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', stock={self.stock_quantity})>"


class Order(Base):
    """Order model for cafe orders"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    table_number = Column(String(20))
    status = Column(String(20), default='pending')  # pending, preparing, ready, delivered, paid
    total_amount = Column(Float, default=0.0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, total={self.total_amount})>"


class OrderItem(Base):
    """Order item model"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, quantity={self.quantity})>"


class GamingSession(Base):
    """Gaming session model for gamnet"""
    __tablename__ = 'gaming_sessions'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    system_number = Column(String(20), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer)  # in minutes
    rate = Column(Float, nullable=False)  # per hour
    total_amount = Column(Float)
    status = Column(String(20), default='active')  # active, paused, completed
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="gaming_sessions")
    
    def __repr__(self):
        return f"<GamingSession(system='{self.system_number}', status='{self.status}')>"


class Invoice(Base):
    """Invoice model"""
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    invoice_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    subtotal = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    status = Column(String(20), default='unpaid')  # unpaid, partial, paid
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice(number='{self.invoice_number}', total={self.total_amount})>"


class InvoiceItem(Base):
    """Invoice item model"""
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    description = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")
    
    def __repr__(self):
        return f"<InvoiceItem(invoice_id={self.invoice_id}, description='{self.description}')>"


class Supplier(Base):
    """Supplier model"""
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    expenses = relationship("Expense", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier(name='{self.name}')>"


class Expense(Base):
    """Expense model"""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    category = Column(String(50), nullable=False)  # supplies, utilities, rent, etc.
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50))
    receipt_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense(category='{self.category}', amount={self.amount})>"


class Campaign(Base):
    """Campaign model for marketing"""
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50))  # discount, promotion, event
    discount_percentage = Column(Float)
    discount_amount = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    target_audience = Column(String(50))  # all, new, vip
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Campaign(name='{self.name}', is_active={self.is_active})>"


class SmsMessage(Base):
    """SMS message model"""
    __tablename__ = 'sms_messages'
    
    id = Column(Integer, primary_key=True)
    recipient = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default='pending')  # pending, sent, delivered, failed
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    message_id = Column(String(100))  # external API message ID
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SmsMessage(recipient='{self.recipient}', status='{self.status}')>"
