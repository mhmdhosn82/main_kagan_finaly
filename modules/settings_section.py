#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Section Module
Manages application settings and configuration
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import shutil
from datetime import datetime
from database.db_manager import get_db_manager
from auth import AuthService


class SettingsSection(ctk.CTkFrame):
    """Settings management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.parent_window = parent
        self.db_manager = get_db_manager()
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
        
        # Create tabbed interface
        self.setup_tabs()
    
    def setup_tabs(self):
        """Setup tabs for different settings"""
        # Tab view
        tabview = ctk.CTkTabview(self, width=1000, height=500)
        tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        tabview.add("ظاهر")
        tabview.add("حساب کاربری")
        tabview.add("پشتیبان‌گیری")
        
        # Setup tabs
        self.setup_appearance_tab(tabview.tab("ظاهر"))
        self.setup_account_tab(tabview.tab("حساب کاربری"))
        self.setup_backup_tab(tabview.tab("پشتیبان‌گیری"))
    
    def setup_appearance_tab(self, tab):
        """Setup appearance settings tab"""
        # Theme section
        theme_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        theme_frame.pack(pady=20, padx=20, fill="x")
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="تم رنگی",
            font=("Vazir", 16, "bold")
        )
        theme_label.pack(pady=15, anchor="e", padx=20)
        
        # Theme selection
        theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        
        light_btn = ctk.CTkRadioButton(
            theme_frame,
            text="روشن (Light)",
            variable=theme_var,
            value="Light",
            font=("Vazir", 12),
            command=lambda: self.change_theme("light")
        )
        light_btn.pack(pady=5, anchor="e", padx=40)
        
        dark_btn = ctk.CTkRadioButton(
            theme_frame,
            text="تیره (Dark)",
            variable=theme_var,
            value="Dark",
            font=("Vazir", 12),
            command=lambda: self.change_theme("dark")
        )
        dark_btn.pack(pady=5, anchor="e", padx=40)
        
        system_btn = ctk.CTkRadioButton(
            theme_frame,
            text="سیستم (System)",
            variable=theme_var,
            value="System",
            font=("Vazir", 12),
            command=lambda: self.change_theme("system")
        )
        system_btn.pack(pady=5, anchor="e", padx=40)
        
        # Color theme section
        color_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        color_frame.pack(pady=20, padx=20, fill="x")
        
        color_label = ctk.CTkLabel(
            color_frame,
            text="رنگ اصلی",
            font=("Vazir", 16, "bold")
        )
        color_label.pack(pady=15, anchor="e", padx=20)
        
        color_info = ctk.CTkLabel(
            color_frame,
            text="تغییر رنگ اصلی پس از راه‌اندازی مجدد اعمال می‌شود",
            font=("Vazir", 11),
            text_color="gray"
        )
        color_info.pack(pady=5, padx=20)
    
    def setup_account_tab(self, tab):
        """Setup account settings tab"""
        # User info section
        info_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        info_frame.pack(pady=20, padx=20, fill="x")
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="اطلاعات کاربری",
            font=("Vazir", 16, "bold")
        )
        info_label.pack(pady=15, anchor="e", padx=20)
        
        # Display user info
        user_info_text = f"""
        نام کاربری: {self.current_user.username}
        نام کامل: {self.current_user.full_name}
        نقش: {self.current_user.role.value}
        ایمیل: {self.current_user.email or 'تعریف نشده'}
        تلفن: {self.current_user.phone or 'تعریف نشده'}
        """
        
        user_info_label = ctk.CTkLabel(
            info_frame,
            text=user_info_text,
            font=("Vazir", 12),
            justify="right"
        )
        user_info_label.pack(pady=10, padx=40, anchor="e")
        
        # Change password section
        password_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        password_frame.pack(pady=20, padx=20, fill="x")
        
        password_label = ctk.CTkLabel(
            password_frame,
            text="تغییر رمز عبور",
            font=("Vazir", 16, "bold")
        )
        password_label.pack(pady=15, anchor="e", padx=20)
        
        # Old password
        ctk.CTkLabel(
            password_frame,
            text="رمز عبور فعلی:",
            font=("Vazir", 12)
        ).pack(pady=5, anchor="e", padx=40)
        
        self.old_password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="رمز عبور فعلی",
            show="*",
            width=250
        )
        self.old_password_entry.pack(pady=5, padx=40, anchor="e")
        
        # New password
        ctk.CTkLabel(
            password_frame,
            text="رمز عبور جدید:",
            font=("Vazir", 12)
        ).pack(pady=5, anchor="e", padx=40)
        
        self.new_password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="رمز عبور جدید",
            show="*",
            width=250
        )
        self.new_password_entry.pack(pady=5, padx=40, anchor="e")
        
        # Confirm password
        ctk.CTkLabel(
            password_frame,
            text="تکرار رمز عبور جدید:",
            font=("Vazir", 12)
        ).pack(pady=5, anchor="e", padx=40)
        
        self.confirm_password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="تکرار رمز عبور جدید",
            show="*",
            width=250
        )
        self.confirm_password_entry.pack(pady=5, padx=40, anchor="e")
        
        # Change password button
        change_password_btn = ctk.CTkButton(
            password_frame,
            text="تغییر رمز عبور",
            font=("Vazir", 12, "bold"),
            fg_color="#667eea",
            hover_color="#5568d3",
            command=self.change_password
        )
        change_password_btn.pack(pady=15, padx=40)
    
    def setup_backup_tab(self, tab):
        """Setup backup/restore tab"""
        # Backup section
        backup_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        backup_frame.pack(pady=20, padx=20, fill="x")
        
        backup_label = ctk.CTkLabel(
            backup_frame,
            text="پشتیبان‌گیری از اطلاعات",
            font=("Vazir", 16, "bold")
        )
        backup_label.pack(pady=15, anchor="e", padx=20)
        
        backup_info = ctk.CTkLabel(
            backup_frame,
            text="پشتیبان‌گیری از پایگاه داده شامل تمام اطلاعات سیستم است",
            font=("Vazir", 11),
            text_color="gray"
        )
        backup_info.pack(pady=5, padx=20)
        
        backup_btn = ctk.CTkButton(
            backup_frame,
            text="📥 ایجاد نسخه پشتیبان",
            font=("Vazir", 12, "bold"),
            fg_color="#27ae60",
            hover_color="#229954",
            command=self.create_backup
        )
        backup_btn.pack(pady=15, padx=20)
        
        # Restore section
        restore_frame = ctk.CTkFrame(tab, fg_color="#f8f9fa", corner_radius=15)
        restore_frame.pack(pady=20, padx=20, fill="x")
        
        restore_label = ctk.CTkLabel(
            restore_frame,
            text="بازیابی اطلاعات",
            font=("Vazir", 16, "bold")
        )
        restore_label.pack(pady=15, anchor="e", padx=20)
        
        restore_info = ctk.CTkLabel(
            restore_frame,
            text="⚠️ بازیابی از نسخه پشتیبان تمام اطلاعات فعلی را جایگزین می‌کند",
            font=("Vazir", 11),
            text_color="orange"
        )
        restore_info.pack(pady=5, padx=20)
        
        restore_btn = ctk.CTkButton(
            restore_frame,
            text="📤 بازیابی از نسخه پشتیبان",
            font=("Vazir", 12, "bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.restore_backup
        )
        restore_btn.pack(pady=15, padx=20)
    
    def change_theme(self, mode):
        """Change application theme"""
        ctk.set_appearance_mode(mode)
        messagebox.showinfo("موفق", f"تم به {mode} تغییر یافت")
    
    def change_password(self):
        """Change user password"""
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate inputs
        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("خطا", "لطفا تمام فیلدها را پر کنید")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("خطا", "رمز عبور جدید و تکرار آن یکسان نیست")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("خطا", "رمز عبور باید حداقل 6 کاراکتر باشد")
            return
        
        try:
            AuthService.change_password(
                self.current_user.id,
                old_password,
                new_password
            )
            
            # Clear entries
            self.old_password_entry.delete(0, 'end')
            self.new_password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            
            messagebox.showinfo("موفق", "رمز عبور با موفقیت تغییر یافت")
            
        except Exception as e:
            messagebox.showerror("خطا", str(e))
    
    def create_backup(self):
        """Create database backup"""
        try:
            # Ask user for backup location
            backup_file = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db *.sqlite"), ("All files", "*.*")],
                initialfile=f"kagan_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            
            if backup_file:
                # Get database file path
                db_file = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'kagan_db.sqlite'
                )
                
                # Copy database file
                shutil.copy2(db_file, backup_file)
                
                messagebox.showinfo(
                    "موفق",
                    f"نسخه پشتیبان با موفقیت ایجاد شد:\n{backup_file}"
                )
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ایجاد نسخه پشتیبان:\n{str(e)}")
    
    def restore_backup(self):
        """Restore database from backup"""
        # Confirm action
        if not messagebox.askyesno(
            "تأیید",
            "آیا مطمئن هستید؟ این عملیات تمام اطلاعات فعلی را جایگزین می‌کند."
        ):
            return
        
        try:
            # Ask user for backup file
            backup_file = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db *.sqlite"), ("All files", "*.*")]
            )
            
            if backup_file:
                # Get database file path
                db_file = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'kagan_db.sqlite'
                )
                
                # Copy backup file to database location
                shutil.copy2(backup_file, db_file)
                
                messagebox.showinfo(
                    "موفق",
                    "بازیابی با موفقیت انجام شد. لطفا برنامه را مجددا راه‌اندازی کنید."
                )
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بازیابی:\n{str(e)}")
