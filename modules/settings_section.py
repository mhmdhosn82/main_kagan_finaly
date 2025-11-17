#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Section Module
Manages application settings and configuration
"""

import customtkinter as ctk


class SettingsSection(ctk.CTkFrame):
    """Settings management section"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the settings section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش تنظیمات",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="تنظیمات برنامه، پیکربندی و سفارشی‌سازی",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
