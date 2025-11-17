#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory Section Module
Manages inventory, stock levels, and product management
"""

import customtkinter as ctk
from tkinter import messagebox
from database.models import Product
from database.db_manager import get_db_manager
from utils import NumberFormatter, is_stock_low


class InventorySection(ctk.CTkFrame):
    """Inventory management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.db_manager = get_db_manager()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the inventory section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش انبار",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت موجودی، محصولات و عملیات انبار",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
        
        # Create tabbed interface
        self.setup_tabs()
    
    def setup_tabs(self):
        """Setup tabs for inventory management"""
        # Tab view
        tabview = ctk.CTkTabview(self, width=1000, height=500)
        tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        tabview.add("همه محصولات")
        tabview.add("موجودی کم")
        tabview.add("گزارش")
        
        # Setup tabs
        self.setup_all_products_tab(tabview.tab("همه محصولات"))
        self.setup_low_stock_tab(tabview.tab("موجودی کم"))
        self.setup_report_tab(tabview.tab("گزارش"))
    
    def setup_all_products_tab(self, tab):
        """Setup all products tab"""
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
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 بروزرسانی",
            font=("Vazir", 12),
            fg_color="#34495e",
            hover_color="#2c3e50",
            command=self.refresh_all_products
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Products list
        self.all_products_frame = ctk.CTkScrollableFrame(tab, label_text="لیست محصولات")
        self.all_products_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_all_products()
    
    def setup_low_stock_tab(self, tab):
        """Setup low stock alerts tab"""
        # Info label
        info_label = ctk.CTkLabel(
            tab,
            text="محصولاتی که موجودی آنها به حد minimum رسیده است",
            font=("Vazir", 12),
            text_color="orange"
        )
        info_label.pack(pady=10)
        
        # Low stock list
        self.low_stock_frame = ctk.CTkScrollableFrame(tab, label_text="هشدار موجودی کم")
        self.low_stock_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_low_stock()
    
    def setup_report_tab(self, tab):
        """Setup inventory report tab"""
        report_label = ctk.CTkLabel(
            tab,
            text="گزارش کلی انبار",
            font=("Vazir", 16, "bold")
        )
        report_label.pack(pady=20)
        
        # Report frame
        self.report_frame = ctk.CTkFrame(tab)
        self.report_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.refresh_report()
    
    def refresh_all_products(self):
        """Refresh all products list"""
        # Clear existing items
        for widget in self.all_products_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                products = session.query(Product).filter_by(is_active=True).all()
                
                if not products:
                    no_data_label = ctk.CTkLabel(
                        self.all_products_frame,
                        text="محصولی یافت نشد",
                        font=("Vazir", 12),
                        text_color="gray"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for product in products:
                        self.create_product_item(self.all_products_frame, product)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری محصولات: {str(e)}")
    
    def refresh_low_stock(self):
        """Refresh low stock items"""
        # Clear existing items
        for widget in self.low_stock_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                products = session.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity <= Product.min_stock_level
                ).all()
                
                if not products:
                    no_data_label = ctk.CTkLabel(
                        self.low_stock_frame,
                        text="همه محصولات موجودی کافی دارند",
                        font=("Vazir", 12),
                        text_color="green"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for product in products:
                        self.create_product_item(self.low_stock_frame, product, highlight_low=True)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری محصولات: {str(e)}")
    
    def create_product_item(self, parent_frame, product, highlight_low=False):
        """Create product list item"""
        fg_color = "#fff3cd" if highlight_low else "#f8f9fa"
        
        item_frame = ctk.CTkFrame(parent_frame, fg_color=fg_color, corner_radius=10)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Product info
        price_str = NumberFormatter.format_currency(product.price, "تومان")
        stock_status = "⚠️ کم" if is_stock_low(product.stock_quantity, product.min_stock_level) else "✓ کافی"
        category_map = {'cafe': 'کافه', 'salon': 'آرایشگاه', 'general': 'عمومی'}
        category = category_map.get(product.category, product.category or 'عمومی')
        
        info_text = f"{product.name} ({category})\nقیمت: {price_str} - موجودی: {product.stock_quantity} {product.unit or ''} - وضعیت: {stock_status}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=("Vazir", 11),
            anchor="e",
            justify="right"
        )
        info_label.pack(side="right", padx=10, pady=10)
    
    def refresh_report(self):
        """Refresh inventory report"""
        # Clear existing widgets
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                from sqlalchemy import func
                
                # Total products
                total_products = session.query(Product).filter_by(is_active=True).count()
                
                # Low stock count
                low_stock_count = session.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity <= Product.min_stock_level
                ).count()
                
                # Total inventory value
                total_value = session.query(func.sum(Product.price * Product.stock_quantity)).filter_by(
                    is_active=True
                ).scalar() or 0
                
                # Display stats
                value_str = NumberFormatter.format_currency(total_value, "تومان")
                stats_text = f"تعداد کل محصولات: {total_products}\nموجودی کم: {low_stock_count}\nارزش کل انبار: {value_str}"
                
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
    
    def show_add_product_dialog(self):
        """Show dialog to add new product"""
        messagebox.showinfo("در حال توسعه", "امکان افزودن محصول به زودی اضافه خواهد شد")
