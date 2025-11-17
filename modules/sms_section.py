#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS Section Module
Manages SMS messaging and notifications interface
"""

import customtkinter as ctk


class SmsSection(ctk.CTkFrame):
    """SMS management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the SMS section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش پیامک",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="ارسال پیامک، مدیریت پیام‌ها و اطلاع‌رسانی",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
