#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Module - Main window and login dialog with glassmorphism design
Supports RTL layout for Persian language
"""

import customtkinter as ctk
from tkinter import messagebox

# Import all module sections
from modules.salon_section import SalonSection
from modules.cafe_section import CafeSection
from modules.gamnet_section import GamnetSection
from modules.inventory_section import InventorySection
from modules.invoice_section import InvoiceSection
from modules.customer_section import CustomerSection
from modules.employee_section import EmployeeSection
from modules.reports_section import ReportsSection
from modules.supplier_expense_section import SupplierExpenseSection
from modules.campaign_section import CampaignSection
from modules.sms_section import SmsSection
from modules.settings_section import SettingsSection


class LoginDialog(ctk.CTk):
    """Login dialog with glassmorphism design"""
    
    def __init__(self):
        super().__init__()
        
        self.login_successful = False
        
        # Configure window
        self.title("ورود به سیستم - Kagan")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Setup UI
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the login UI"""
        # Create main frame with padding
        main_frame = ctk.CTkFrame(self, fg_color=("gray95", "gray10"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="سیستم مدیریت کسب و کار کاگان",
            font=("Vazir", 20, "bold"),
            text_color=("#667eea", "#764ba2")
        )
        title_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="کافه - آرایشگاه - گیم نت",
            font=("Vazir", 14),
            text_color=("gray40", "gray60")
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Username label
        username_label = ctk.CTkLabel(
            main_frame,
            text="نام کاربری:",
            font=("Vazir", 12),
            anchor="e"
        )
        username_label.pack(pady=(10, 5), padx=30, anchor="e")
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="نام کاربری خود را وارد کنید",
            font=("Vazir", 12),
            height=40,
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 10), padx=30, fill="x")
        
        # Password label
        password_label = ctk.CTkLabel(
            main_frame,
            text="رمز عبور:",
            font=("Vazir", 12),
            anchor="e"
        )
        password_label.pack(pady=(10, 5), padx=30, anchor="e")
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="رمز عبور خود را وارد کنید",
            font=("Vazir", 12),
            height=40,
            show="*",
            corner_radius=10
        )
        self.password_entry.pack(pady=(0, 30), padx=30, fill="x")
        
        # Login button
        login_button = ctk.CTkButton(
            main_frame,
            text="ورود",
            font=("Vazir", 14, "bold"),
            height=45,
            corner_radius=10,
            command=self.handle_login,
            fg_color=("#667eea", "#764ba2"),
            hover_color=("#5568d3", "#6a3f8f")
        )
        login_button.pack(pady=(0, 20), padx=30, fill="x")
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Simple authentication (in production, use proper authentication)
        if username and password:
            # For demo: accept any non-empty credentials
            self.login_successful = True
            self.destroy()
        else:
            messagebox.showerror(
                "خطا",
                "لطفا نام کاربری و رمز عبور را وارد کنید"
            )


class MainWindow(ctk.CTk):
    """Main application window with sidebar navigation"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("سیستم مدیریت کاگان - Kagan Business Manager")
        self.geometry("1200x700")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize modules dictionary
        self.modules = {}
        self.current_module_frame = None
        
        # Setup UI
        self.setup_ui()
        
        # Show first module
        self.show_module('salon')
    
    def setup_ui(self):
        """Setup the main window UI"""
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=("#667eea", "#764ba2"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(14, weight=1)
        
        # Logo/Title
        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="کاگان",
            font=("Vazir", 24, "bold"),
            text_color="white"
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="مدیریت کسب و کار",
            font=("Vazir", 12),
            text_color="white"
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation buttons
        modules_config = [
            ('salon', 'آرایشگاه', SalonSection),
            ('cafe', 'کافه', CafeSection),
            ('gamnet', 'گیم نت', GamnetSection),
            ('inventory', 'انبار', InventorySection),
            ('invoice', 'فاکتور', InvoiceSection),
            ('customer', 'مشتریان', CustomerSection),
            ('employee', 'کارمندان', EmployeeSection),
            ('reports', 'گزارشات', ReportsSection),
            ('supplier_expense', 'تامین کنندگان', SupplierExpenseSection),
            ('campaign', 'کمپین ها', CampaignSection),
            ('sms', 'پیامک', SmsSection),
            ('settings', 'تنظیمات', SettingsSection),
        ]
        
        row = 2
        for module_id, label, module_class in modules_config:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=label,
                font=("Vazir", 13),
                height=40,
                corner_radius=10,
                fg_color="transparent",
                text_color="white",
                hover_color=("#8a9df0", "#9068c7"),
                border_width=2,
                border_color="#b8c5f7",
                anchor="center",
                command=lambda mid=module_id: self.show_module(mid)
            )
            btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            row += 1
            
            # Initialize module (create instance but don't add to grid yet)
            self.modules[module_id] = module_class(self)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def show_module(self, module_id):
        """Show the selected module"""
        if module_id in self.modules:
            # Hide current module
            if self.current_module_frame:
                self.current_module_frame.grid_forget()
            
            # Show new module
            self.current_module_frame = self.modules[module_id]
            self.current_module_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
