#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed Data Script
Populate database with sample data for demonstration
"""

import logging
from datetime import datetime, timedelta
from database.db_manager import initialize_database, get_db_manager
from database.models import (
    User, UserRole, Customer, Employee, Service, Product, 
    Appointment, Order, OrderItem, GamingSession, Supplier, 
    Expense, Campaign, Invoice, InvoiceItem
)
from auth import AuthService
from utils import setup_logging, generate_invoice_number

logger = logging.getLogger(__name__)


def seed_users():
    """Create sample users"""
    logger.info("Seeding users...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        # Check if users already exist
        if session.query(User).count() > 0:
            logger.info("Users already exist, skipping...")
            return
        
        # Create admin
        AuthService.create_user(
            username="admin",
            password="admin123",
            full_name="مدیر سیستم",
            role=UserRole.ADMIN,
            email="admin@kagan.local",
            phone="09121234567"
        )
        
        # Create manager
        AuthService.create_user(
            username="manager",
            password="manager123",
            full_name="مدیر اجرایی",
            role=UserRole.MANAGER,
            email="manager@kagan.local",
            phone="09121234568"
        )
        
        # Create staff
        AuthService.create_user(
            username="staff",
            password="staff123",
            full_name="کارمند",
            role=UserRole.STAFF,
            email="staff@kagan.local",
            phone="09121234569"
        )
        
        logger.info("Users created successfully")


def seed_customers():
    """Create sample customers"""
    logger.info("Seeding customers...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Customer).count() > 0:
            logger.info("Customers already exist, skipping...")
            return
        
        customers_data = [
            {"name": "علی احمدی", "phone": "09121111111", "email": "ali@example.com", "loyalty_points": 100},
            {"name": "سارا محمدی", "phone": "09122222222", "email": "sara@example.com", "loyalty_points": 50},
            {"name": "رضا کریمی", "phone": "09123333333", "email": "reza@example.com", "loyalty_points": 75},
            {"name": "فاطمه حسینی", "phone": "09124444444", "email": "fateme@example.com", "loyalty_points": 120},
            {"name": "محمد رضایی", "phone": "09125555555", "email": "mohammad@example.com", "loyalty_points": 80},
        ]
        
        for data in customers_data:
            customer = Customer(**data)
            session.add(customer)
        
        logger.info(f"Created {len(customers_data)} customers")


def seed_employees():
    """Create sample employees"""
    logger.info("Seeding employees...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Employee).count() > 0:
            logger.info("Employees already exist, skipping...")
            return
        
        employees_data = [
            {"name": "حسن آرایشگر", "position": "آرایشگر", "phone": "09131111111", "salary": 15000000},
            {"name": "زهرا منشی", "position": "منشی", "phone": "09132222222", "salary": 10000000},
            {"name": "امیر بارista", "position": "باریستا", "phone": "09133333333", "salary": 12000000},
        ]
        
        for data in employees_data:
            employee = Employee(**data, hire_date=datetime.now() - timedelta(days=365))
            session.add(employee)
        
        logger.info(f"Created {len(employees_data)} employees")


def seed_services():
    """Create sample salon services"""
    logger.info("Seeding services...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Service).count() > 0:
            logger.info("Services already exist, skipping...")
            return
        
        services_data = [
            {"name": "کوتاهی مو", "description": "کوتاهی و آرایش مو", "price": 500000, "duration": 45},
            {"name": "رنگ مو", "description": "رنگ و هایلایت", "price": 1500000, "duration": 120},
            {"name": "اصلاح صورت", "description": "اصلاح و آرایش صورت", "price": 300000, "duration": 30},
            {"name": "ماساژ سر", "description": "ماساژ و درمان مو", "price": 400000, "duration": 40},
        ]
        
        for data in services_data:
            service = Service(**data)
            session.add(service)
        
        logger.info(f"Created {len(services_data)} services")


def seed_products():
    """Create sample products"""
    logger.info("Seeding products...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Product).count() > 0:
            logger.info("Products already exist, skipping...")
            return
        
        products_data = [
            # Cafe products
            {"name": "قهوه اسپرسو", "category": "cafe", "price": 50000, "cost": 20000, "stock_quantity": 100, "unit": "فنجان"},
            {"name": "کاپوچینو", "category": "cafe", "price": 70000, "cost": 30000, "stock_quantity": 80, "unit": "فنجان"},
            {"name": "چای", "category": "cafe", "price": 30000, "cost": 10000, "stock_quantity": 150, "unit": "لیوان"},
            {"name": "کیک شکلاتی", "category": "cafe", "price": 120000, "cost": 50000, "stock_quantity": 25, "unit": "تکه"},
            {"name": "ساندویچ", "category": "cafe", "price": 150000, "cost": 70000, "stock_quantity": 30, "unit": "عدد"},
            
            # Salon products
            {"name": "شامپو", "category": "salon", "price": 200000, "cost": 100000, "stock_quantity": 50, "unit": "بطری"},
            {"name": "رنگ مو", "category": "salon", "price": 350000, "cost": 180000, "stock_quantity": 20, "unit": "بسته"},
            {"name": "کرم مو", "category": "salon", "price": 150000, "cost": 70000, "stock_quantity": 35, "unit": "بطری"},
            
            # General products
            {"name": "دستمال کاغذی", "category": "general", "price": 50000, "cost": 25000, "stock_quantity": 100, "unit": "بسته"},
            {"name": "مایع دستشویی", "category": "general", "price": 80000, "cost": 40000, "stock_quantity": 5, "min_stock_level": 10, "unit": "بطری"},
        ]
        
        for data in products_data:
            product = Product(**data)
            session.add(product)
        
        logger.info(f"Created {len(products_data)} products")


def seed_appointments():
    """Create sample appointments"""
    logger.info("Seeding appointments...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Appointment).count() > 0:
            logger.info("Appointments already exist, skipping...")
            return
        
        customers = session.query(Customer).limit(3).all()
        services = session.query(Service).limit(3).all()
        employees = session.query(Employee).filter_by(position="آرایشگر").first()
        
        if not customers or not services:
            logger.warning("No customers or services found, skipping appointments")
            return
        
        # Create appointments for today and tomorrow
        base_date = datetime.now()
        for i in range(5):
            appointment = Appointment(
                customer_id=customers[i % len(customers)].id,
                service_id=services[i % len(services)].id,
                stylist_id=employees.id if employees else None,
                appointment_date=base_date + timedelta(hours=i*2),
                status='scheduled' if i > 0 else 'completed'
            )
            session.add(appointment)
        
        logger.info("Created sample appointments")


def seed_orders():
    """Create sample cafe orders"""
    logger.info("Seeding orders...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Order).count() > 0:
            logger.info("Orders already exist, skipping...")
            return
        
        customers = session.query(Customer).limit(3).all()
        cafe_products = session.query(Product).filter_by(category='cafe').all()
        
        if not customers or not cafe_products:
            logger.warning("No customers or cafe products found, skipping orders")
            return
        
        # Create 5 sample orders
        for i in range(5):
            order = Order(
                customer_id=customers[i % len(customers)].id if i % 2 == 0 else None,
                table_number=f"میز {i+1}",
                status=['pending', 'preparing', 'ready', 'paid'][i % 4],
                total_amount=0
            )
            session.add(order)
            session.flush()
            
            # Add 2-3 items to each order
            total = 0
            for j in range(2 + (i % 2)):
                product = cafe_products[j % len(cafe_products)]
                quantity = 1 + (i % 3)
                subtotal = product.price * quantity
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price,
                    subtotal=subtotal
                )
                session.add(order_item)
                total += subtotal
            
            order.total_amount = total
        
        logger.info("Created sample orders")


def seed_suppliers():
    """Create sample suppliers"""
    logger.info("Seeding suppliers...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Supplier).count() > 0:
            logger.info("Suppliers already exist, skipping...")
            return
        
        suppliers_data = [
            {"name": "تامین کننده قهوه", "contact_person": "آقای رضایی", "phone": "02133334444"},
            {"name": "تامین کننده لوازم آرایشی", "contact_person": "خانم احمدی", "phone": "02133335555"},
            {"name": "تامین کننده مواد غذایی", "contact_person": "آقای محمدی", "phone": "02133336666"},
        ]
        
        for data in suppliers_data:
            supplier = Supplier(**data)
            session.add(supplier)
        
        logger.info(f"Created {len(suppliers_data)} suppliers")


def seed_campaigns():
    """Create sample campaigns"""
    logger.info("Seeding campaigns...")
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        if session.query(Campaign).count() > 0:
            logger.info("Campaigns already exist, skipping...")
            return
        
        campaigns_data = [
            {
                "name": "تخفیف عید",
                "description": "تخفیف ویژه عید نوروز",
                "campaign_type": "discount",
                "discount_percentage": 20,
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(days=30),
                "is_active": True
            },
            {
                "name": "مشتریان VIP",
                "description": "پاداش ویژه مشتریان VIP",
                "campaign_type": "promotion",
                "discount_percentage": 15,
                "target_audience": "vip",
                "is_active": True
            }
        ]
        
        for data in campaigns_data:
            campaign = Campaign(**data)
            session.add(campaign)
        
        logger.info(f"Created {len(campaigns_data)} campaigns")


def main():
    """Main seeding function"""
    setup_logging()
    logger.info("Starting database seeding...")
    
    # Initialize database
    initialize_database()
    
    # Seed all tables
    seed_users()
    seed_customers()
    seed_employees()
    seed_services()
    seed_products()
    seed_suppliers()
    seed_campaigns()
    seed_appointments()
    seed_orders()
    
    logger.info("Database seeding completed successfully!")
    print("\n✓ Database seeded successfully!")
    print("\nDefault users:")
    print("  Admin    - username: admin    password: admin123")
    print("  Manager  - username: manager  password: manager123")
    print("  Staff    - username: staff    password: staff123")


if __name__ == "__main__":
    main()
