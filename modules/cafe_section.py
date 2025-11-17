#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cafe Section Module
Manages cafe/bar orders, menu, and cafe-specific operations
"""

import customtkinter as ctk


class CafeSection(ctk.CTkFrame):
    """Cafe management section"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
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
