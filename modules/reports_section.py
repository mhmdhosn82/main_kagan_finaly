#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports Section Module
Manages financial and managerial reports with filters
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from database.models import Order, Appointment, Invoice, Expense
from database.db_manager import get_db_manager
from utils import NumberFormatter, DateFormatter


class ReportsSection(ctk.CTkFrame):
    """Reports management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.db_manager = get_db_manager()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the reports section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش گزارشات",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="گزارشات مالی، مدیریتی و تحلیلی با فیلترهای متنوع",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
        
        # Create tabbed interface
        self.setup_tabs()
    
    def setup_tabs(self):
        """Setup tabs for different reports"""
        # Tab view
        tabview = ctk.CTkTabview(self, width=1000, height=500)
        tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        tabview.add("گزارش فروش")
        tabview.add("گزارش مالی")
        tabview.add("گزارش کلی")
        
        # Setup tabs
        self.setup_sales_report_tab(tabview.tab("گزارش فروش"))
        self.setup_financial_report_tab(tabview.tab("گزارش مالی"))
        self.setup_overview_tab(tabview.tab("گزارش کلی"))
    
    def setup_sales_report_tab(self, tab):
        """Setup sales report tab"""
        # Filters frame
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(pady=10, fill="x")
        
        # Date range selection
        ctk.CTkLabel(filter_frame, text="بازه زمانی:", font=("Vazir", 12)).pack(side="right", padx=5)
        
        self.date_range_var = ctk.StringVar(value="امروز")
        date_range_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["امروز", "هفته جاری", "ماه جاری", "همه"],
            variable=self.date_range_var,
            command=self.refresh_sales_report
        )
        date_range_menu.pack(side="right", padx=5)
        
        # Report display frame
        self.sales_report_frame = ctk.CTkScrollableFrame(tab, label_text="گزارش فروش")
        self.sales_report_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_sales_report()
    
    def setup_financial_report_tab(self, tab):
        """Setup financial report tab"""
        # Report display frame
        self.financial_report_frame = ctk.CTkFrame(tab)
        self.financial_report_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.refresh_financial_report()
    
    def setup_overview_tab(self, tab):
        """Setup overview dashboard tab"""
        # Create dashboard cards
        cards_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cards_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Configure grid
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        cards_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Store card frames for refresh
        self.overview_cards = {}
        
        # Card titles
        card_titles = [
            ("فروش امروز", "sales_today"),
            ("مشتریان امروز", "customers_today"),
            ("نوبت‌های امروز", "appointments_today"),
            ("درآمد هفته", "weekly_revenue"),
            ("سفارشات فعال", "active_orders"),
            ("موجودی کم", "low_stock")
        ]
        
        # Create cards
        row = 0
        col = 0
        for title, key in card_titles:
            card = self.create_dashboard_card(cards_frame, title)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.overview_cards[key] = card
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        self.refresh_overview()
    
    def create_dashboard_card(self, parent, title):
        """Create a dashboard card widget"""
        card = ctk.CTkFrame(parent, fg_color="#f8f9fa", corner_radius=15)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Vazir", 14, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=(15, 5))
        
        # Value label (will be updated)
        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=("Vazir", 24, "bold"),
            text_color="#667eea"
        )
        value_label.pack(pady=(5, 15))
        
        # Store reference to value label
        card.value_label = value_label
        
        return card
    
    def refresh_sales_report(self, *args):
        """Refresh sales report based on selected date range"""
        # Clear existing widgets
        for widget in self.sales_report_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get date range
            date_range = self.date_range_var.get()
            start_date = self.get_start_date_for_range(date_range)
            
            with self.db_manager.session_scope() as session:
                from sqlalchemy import func
                
                # Get orders in date range
                orders = session.query(Order).filter(
                    Order.created_at >= start_date
                ).all()
                
                # Calculate statistics
                total_orders = len(orders)
                total_revenue = sum(order.total_amount for order in orders)
                paid_orders = len([o for o in orders if o.status == 'paid'])
                
                # Display statistics
                stats_text = f"""
                بازه زمانی: {date_range}
                تعداد کل سفارشات: {total_orders}
                درآمد کل: {NumberFormatter.format_currency(total_revenue, "تومان")}
                سفارشات پرداخت شده: {paid_orders}
                میانگین سفارش: {NumberFormatter.format_currency(total_revenue / total_orders if total_orders > 0 else 0, "تومان")}
                """
                
                stats_label = ctk.CTkLabel(
                    self.sales_report_frame,
                    text=stats_text,
                    font=("Vazir", 13),
                    justify="right"
                )
                stats_label.pack(pady=20, padx=20)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.sales_report_frame,
                text=f"خطا در بارگذاری گزارش: {str(e)}",
                font=("Vazir", 12),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def refresh_financial_report(self):
        """Refresh financial report"""
        # Clear existing widgets
        for widget in self.financial_report_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                from sqlalchemy import func
                
                # Get this month's data
                start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                
                # Calculate revenue (from orders and invoices)
                order_revenue = session.query(func.sum(Order.total_amount)).filter(
                    Order.created_at >= start_of_month,
                    Order.status == 'paid'
                ).scalar() or 0
                
                invoice_revenue = session.query(func.sum(Invoice.paid_amount)).filter(
                    Invoice.invoice_date >= start_of_month
                ).scalar() or 0
                
                total_revenue = order_revenue + invoice_revenue
                
                # Calculate expenses
                total_expenses = session.query(func.sum(Expense.amount)).filter(
                    Expense.expense_date >= start_of_month
                ).scalar() or 0
                
                # Net profit
                net_profit = total_revenue - total_expenses
                
                # Display financial summary
                report_text = f"""
                گزارش مالی ماه جاری
                ────────────────────────────
                
                درآمد کل: {NumberFormatter.format_currency(total_revenue, "تومان")}
                  - از سفارشات کافه: {NumberFormatter.format_currency(order_revenue, "تومان")}
                  - از فاکتورها: {NumberFormatter.format_currency(invoice_revenue, "تومان")}
                
                هزینه‌های کل: {NumberFormatter.format_currency(total_expenses, "تومان")}
                
                سود خالص: {NumberFormatter.format_currency(net_profit, "تومان")}
                """
                
                report_label = ctk.CTkLabel(
                    self.financial_report_frame,
                    text=report_text,
                    font=("Vazir", 14),
                    justify="right"
                )
                report_label.pack(pady=30, padx=30)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.financial_report_frame,
                text=f"خطا در بارگذاری گزارش: {str(e)}",
                font=("Vazir", 12),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def refresh_overview(self):
        """Refresh overview dashboard"""
        try:
            with self.db_manager.session_scope() as session:
                from sqlalchemy import func
                from database.models import Customer, Product
                
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                week_ago = today - timedelta(days=7)
                
                # Sales today
                sales_today = session.query(func.sum(Order.total_amount)).filter(
                    Order.created_at >= today,
                    Order.status == 'paid'
                ).scalar() or 0
                self.overview_cards['sales_today'].value_label.configure(
                    text=NumberFormatter.format_currency(sales_today, "تومان")
                )
                
                # Customers today
                customers_today = session.query(Customer).filter(
                    Customer.created_at >= today
                ).count()
                self.overview_cards['customers_today'].value_label.configure(text=str(customers_today))
                
                # Appointments today
                appointments_today = session.query(Appointment).filter(
                    Appointment.appointment_date >= today
                ).count()
                self.overview_cards['appointments_today'].value_label.configure(text=str(appointments_today))
                
                # Weekly revenue
                weekly_revenue = session.query(func.sum(Order.total_amount)).filter(
                    Order.created_at >= week_ago,
                    Order.status == 'paid'
                ).scalar() or 0
                self.overview_cards['weekly_revenue'].value_label.configure(
                    text=NumberFormatter.format_currency(weekly_revenue, "تومان")
                )
                
                # Active orders
                active_orders = session.query(Order).filter(
                    Order.status.in_(['pending', 'preparing', 'ready'])
                ).count()
                self.overview_cards['active_orders'].value_label.configure(text=str(active_orders))
                
                # Low stock items
                low_stock = session.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity <= Product.min_stock_level
                ).count()
                self.overview_cards['low_stock'].value_label.configure(text=str(low_stock))
                
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری داشبورد: {str(e)}")
    
    def get_start_date_for_range(self, date_range):
        """Get start date for the selected date range"""
        now = datetime.now()
        
        if date_range == "امروز":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == "هفته جاری":
            return now - timedelta(days=now.weekday())
        elif date_range == "ماه جاری":
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:  # همه
            return datetime(2000, 1, 1)
