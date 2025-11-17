#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Salon Section Module
Manages salon services, appointments, and salon-specific operations
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from database.models import Appointment, Service, Customer, Employee
from database.db_manager import get_db_manager
from utils import Validator, DateFormatter, NumberFormatter


class SalonSection(ctk.CTkFrame):
    """Salon management section"""
    
    def __init__(self, parent, current_user):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.current_user = current_user
        self.db_manager = get_db_manager()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the salon section UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="بخش آرایشگاه",
            font=("Vazir", 28, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(40, 10))
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="مدیریت خدمات آرایشگاه، نوبت‌ها و عملیات مرتبط",
            font=("Vazir", 14),
            text_color="#7f8c8d"
        )
        description.pack(pady=(0, 20))
        
        # Create tabbed interface
        self.setup_tabs()
    
    def setup_tabs(self):
        """Setup tabs for different salon functionalities"""
        # Tab view
        tabview = ctk.CTkTabview(self, width=1000, height=500)
        tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        tabview.add("نوبت‌ها")
        tabview.add("خدمات")
        tabview.add("گزارش")
        
        # Setup appointment tab
        self.setup_appointments_tab(tabview.tab("نوبت‌ها"))
        
        # Setup services tab
        self.setup_services_tab(tabview.tab("خدمات"))
        
        # Setup report tab
        self.setup_report_tab(tabview.tab("گزارش"))
    
    def setup_appointments_tab(self, tab):
        """Setup appointments management tab"""
        # Buttons frame
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x")
        
        # Add appointment button
        add_btn = ctk.CTkButton(
            btn_frame,
            text="+ نوبت جدید",
            font=("Vazir", 12, "bold"),
            fg_color="#667eea",
            hover_color="#5568d3",
            command=self.show_add_appointment_dialog
        )
        add_btn.pack(side="right", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 بروزرسانی",
            font=("Vazir", 12),
            fg_color="#34495e",
            hover_color="#2c3e50",
            command=self.refresh_appointments
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Appointments list frame with scrollbar
        list_frame = ctk.CTkScrollableFrame(tab, label_text="لیست نوبت‌ها")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.appointments_list_frame = list_frame
        self.refresh_appointments()
    
    def setup_services_tab(self, tab):
        """Setup services management tab"""
        # Buttons frame
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x")
        
        # Add service button
        add_btn = ctk.CTkButton(
            btn_frame,
            text="+ خدمت جدید",
            font=("Vazir", 12, "bold"),
            fg_color="#667eea",
            hover_color="#5568d3",
            command=self.show_add_service_dialog
        )
        add_btn.pack(side="right", padx=5)
        
        # Services list frame
        list_frame = ctk.CTkScrollableFrame(tab, label_text="لیست خدمات")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.services_list_frame = list_frame
        self.refresh_services()
    
    def setup_report_tab(self, tab):
        """Setup report tab"""
        report_label = ctk.CTkLabel(
            tab,
            text="گزارش نوبت‌های امروز",
            font=("Vazir", 16, "bold")
        )
        report_label.pack(pady=20)
        
        # Report frame
        self.report_frame = ctk.CTkFrame(tab)
        self.report_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.refresh_report()
    
    def refresh_appointments(self):
        """Refresh appointments list"""
        # Clear existing items
        for widget in self.appointments_list_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                # Get appointments for today and future
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                appointments = session.query(Appointment).filter(
                    Appointment.appointment_date >= today
                ).order_by(Appointment.appointment_date).limit(20).all()
                
                if not appointments:
                    no_data_label = ctk.CTkLabel(
                        self.appointments_list_frame,
                        text="نوبتی یافت نشد",
                        font=("Vazir", 12),
                        text_color="gray"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for appointment in appointments:
                        self.create_appointment_item(appointment)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری نوبت‌ها: {str(e)}")
    
    def create_appointment_item(self, appointment):
        """Create appointment list item"""
        item_frame = ctk.CTkFrame(self.appointments_list_frame, fg_color="#f8f9fa", corner_radius=10)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Get customer name
        customer_name = appointment.customer.name if appointment.customer else "نامشخص"
        service_name = appointment.service.name if appointment.service else "نامشخص"
        stylist_name = appointment.stylist.name if appointment.stylist else "نامشخص"
        
        # Date and time
        date_str = DateFormatter.format_datetime(appointment.appointment_date)
        
        # Info label
        info_text = f"{customer_name} - {service_name} - {stylist_name}\n{date_str} - وضعیت: {appointment.status}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=("Vazir", 11),
            anchor="e",
            justify="right"
        )
        info_label.pack(side="right", padx=10, pady=10)
    
    def refresh_services(self):
        """Refresh services list"""
        # Clear existing items
        for widget in self.services_list_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                services = session.query(Service).filter_by(is_active=True).all()
                
                if not services:
                    no_data_label = ctk.CTkLabel(
                        self.services_list_frame,
                        text="خدمتی یافت نشد",
                        font=("Vazir", 12),
                        text_color="gray"
                    )
                    no_data_label.pack(pady=20)
                else:
                    for service in services:
                        self.create_service_item(service)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری خدمات: {str(e)}")
    
    def create_service_item(self, service):
        """Create service list item"""
        item_frame = ctk.CTkFrame(self.services_list_frame, fg_color="#f8f9fa", corner_radius=10)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Service info
        price_str = NumberFormatter.format_currency(service.price, "تومان")
        duration_str = f"{service.duration} دقیقه" if service.duration else "نامشخص"
        
        info_text = f"{service.name}\nقیمت: {price_str} - مدت: {duration_str}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=("Vazir", 11),
            anchor="e",
            justify="right"
        )
        info_label.pack(side="right", padx=10, pady=10)
    
    def refresh_report(self):
        """Refresh daily report"""
        # Clear existing widgets
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        try:
            with self.db_manager.session_scope() as session:
                # Get today's appointments
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                tomorrow = today + timedelta(days=1)
                
                total_appointments = session.query(Appointment).filter(
                    Appointment.appointment_date >= today,
                    Appointment.appointment_date < tomorrow
                ).count()
                
                completed = session.query(Appointment).filter(
                    Appointment.appointment_date >= today,
                    Appointment.appointment_date < tomorrow,
                    Appointment.status == 'completed'
                ).count()
                
                # Display stats
                stats_text = f"تعداد کل نوبت‌ها: {total_appointments}\nتکمیل شده: {completed}\nباقیمانده: {total_appointments - completed}"
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
    
    def show_add_appointment_dialog(self):
        """Show dialog to add new appointment"""
        messagebox.showinfo("در حال توسعه", "امکان افزودن نوبت به زودی اضافه خواهد شد")
    
    def show_add_service_dialog(self):
        """Show dialog to add new service"""
        messagebox.showinfo("در حال توسعه", "امکان افزودن خدمت به زودی اضافه خواهد شد")
