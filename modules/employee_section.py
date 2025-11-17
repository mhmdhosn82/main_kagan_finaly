#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Employee Section Module
Manages employee information, HR, and employee operations
"""

import customtkinter as ctk


class EmployeeSection(ctk.CTkFrame):
    """Employee management section"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the employee section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش کارمندان",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت کارمندان، منابع انسانی و پرسنل",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
