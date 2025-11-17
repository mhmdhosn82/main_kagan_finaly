#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Supplier & Expense Section Module
Manages suppliers, procurement, and expense tracking
"""

import customtkinter as ctk


class SupplierExpenseSection(ctk.CTkFrame):
    """Supplier and expense management section"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the supplier expense section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش تامین کنندگان",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت تامین کنندگان، خرید و هزینه‌ها",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
