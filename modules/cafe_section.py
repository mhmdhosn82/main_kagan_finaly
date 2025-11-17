#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cafe Section Module
Manages cafe/bar orders, menu, and cafe-specific operations
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database.models import Order, OrderItem, Product, Customer
from database.db_manager import get_db_manager
from utils import Validator, NumberFormatter


class CafeSection(ctk.CTkFrame):
    """Cafe management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.db_manager = get_db_manager()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the cafe section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش کافه",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت سفارشات، منو و عملیات کافه/بار",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
        
        # Create tabbed interface
        self.setup_tabs()
    
    def setup_tabs(self):
        """Setup tabs for different cafe functionalities"""
        # Tab view
        tabview = ctk.CTkTabview(self, width=1000, height=500)
        tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        tabview.add("سفارشات فعال")
        tabview.add("منو")
        tabview.add("گزارش روزانه")
        
        # Setup tabs
        self.setup_orders_tab(tabview.tab("سفارشات فعال"))
        self.setup_menu_tab(tabview.tab("منو"))
        self.setup_daily_report_tab(tabview.tab("گزارش روزانه"))
    
    def setup_orders_tab(self, tab):
        """Setup active orders tab"""
        # Buttons frame
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x")
        
        # New order button
        new_btn = ctk.CTkButton(
            btn_frame,
            text="+ سفارش جدید",
            font=("Vazir", 12, "bold"),
            fg_color="#667eea",
            hover_color="#5568d3",
            command=self.show_new_order_dialog
        )
        new_btn.pack(side="right", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 بروزرسانی",
            font=("Vazir", 12),
            fg_color="#34495e",
            hover_color="#2c3e50",
            command=self.refresh_orders
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Orders list
        self.orders_list_frame = ctk.CTkScrollableFrame(tab, label_text="سفارشات فعال")
        self.orders_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_orders()
    
    def setup_menu_tab(self, tab):
        """Setup menu management tab"""
        # Buttons frame
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x")
        
        # Add product button
        add_btn = ctk.CTkButton(
            btn_frame,
            text="+ محصول جدید",
            font=("Vazir", 12, "bold"),
            fg_color="#667eea",
            hover_color="#5568d3",
            command=self.show_add_product_dialog
        )
        add_btn.pack(side="right", padx=5)
        
        # Menu list
        self.menu_list_frame = ctk.CTkScrollableFrame(tab, label_text="منوی کافه")
        self.menu_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_menu()
    
    def setup_daily_report_tab(self, tab):
        """Setup daily report tab"""
        report_label = ctk.CTkLabel(
            tab,
            text="گزارش فروش روزانه",
            font=("Vazir", 16, "bold")
        )
        report_label.pack(pady=20)
        
        # Report frame
        self.report_frame = ctk.CTkFrame(tab)
        self.report_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.refresh_daily_report()
    
    def refresh_orders(self):
        """Refresh active orders list"""
        # Clear existing items
        for widget in self.orders_list_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                # Get active orders
                orders = session.query(Order).filter(
                    Order.status.in_(['pending', 'preparing', 'ready'])
                ).order_by(Order.created_at.desc()).limit(20).all()
                
                if not orders:
                    no_data_label = ctk.CTkLabel(
                        self.orders_list_frame,
                        text="سفارشی یافت نشد",
                        font=("Vazir", 12),
                        text_color="gray"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for order in orders:
                        self.create_order_item(order)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری سفارشات: {str(e)}")
    
    def create_order_item(self, order):
        """Create order list item"""
        item_frame = ctk.CTkFrame(self.orders_list_frame, fg_color="#f8f9fa", corner_radius=10)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Order info
        table_info = f"میز: {order.table_number}" if order.table_number else "بدون میز"
        total_str = NumberFormatter.format_currency(order.total_amount, "تومان")
        status_map = {
            'pending': 'در انتظار',
            'preparing': 'در حال آماده‌سازی',
            'ready': 'آماده تحویل',
            'delivered': 'تحویل داده شده',
            'paid': 'پرداخت شده'
        }
        status = status_map.get(order.status, order.status)
        
        info_text = f"سفارش #{order.id} - {table_info}\nمبلغ: {total_str} - وضعیت: {status}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=("Vazir", 11),
            anchor="e",
            justify="right"
        )
        info_label.pack(side="right", padx=10, pady=10)
    
    def refresh_menu(self):
        """Refresh menu items"""
        # Clear existing items
        for widget in self.menu_list_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                # Get cafe products
                products = session.query(Product).filter_by(
                    category='cafe',
                    is_active=True
                ).all()
                
                if not products:
                    no_data_label = ctk.CTkLabel(
                        self.menu_list_frame,
                        text="محصولی یافت نشد",
                        font=("Vazir", 12),
                        text_color="gray"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for product in products:
                        self.create_menu_item(product)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری منو: {str(e)}")
    
    def create_menu_item(self, product):
        """Create menu list item"""
        item_frame = ctk.CTkFrame(self.menu_list_frame, fg_color="#f8f9fa", corner_radius=10)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Product info
        price_str = NumberFormatter.format_currency(product.price, "تومان")
        stock_info = f"موجودی: {product.stock_quantity}"
        
        info_text = f"{product.name}\nقیمت: {price_str} - {stock_info}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=("Vazir", 11),
            anchor="e",
            justify="right"
        )
        info_label.pack(side="right", padx=10, pady=10)
    
    def refresh_daily_report(self):
        """Refresh daily sales report"""
        # Clear existing widgets
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                # Get today's orders
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                
                from sqlalchemy import func
                
                # Total orders
                total_orders = session.query(Order).filter(
                    Order.created_at >= today
                ).count()
                
                # Total sales
                total_sales = session.query(func.sum(Order.total_amount)).filter(
                    Order.created_at >= today
                ).scalar() or 0
                
                # Paid orders
                paid_orders = session.query(Order).filter(
                    Order.created_at >= today,
                    Order.status == 'paid'
                ).count()
                
                # Display stats
                sales_str = NumberFormatter.format_currency(total_sales, "تومان")
                stats_text = f"تعداد سفارشات: {total_orders}\nفروش کل: {sales_str}\nپرداخت شده: {paid_orders}"
                
                stats_label = ctk.CTkLabel(
                    self.report_frame,
                    text=stats_text,
                    font=("Vazir", 14),
                    justify="right"
                )
                stats_label.pack(pady=20, padx=20)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.report_frame,
                text=f"خطا در بارگذاری گزارش: {str(e)}",
                font=("Vazir", 12),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def show_new_order_dialog(self):
        """Show dialog to create new order"""
        messagebox.showinfo("در حال توسعه", "امکان افزودن سفارش به زودی اضافه خواهد شد")
    
    def show_add_product_dialog(self):
        """Show dialog to add new product"""
        messagebox.showinfo("در حال توسعه", "امکان افزودن محصول به زودی اضافه خواهد شد")
