#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Section Module
Manages customer information, CRM, and customer relationships
"""

import customtkinter as ctk


class CustomerSection(ctk.CTkFrame):
    """Customer management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the customer section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش مشتریان",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت اطلاعات مشتریان و ارتباطات",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
