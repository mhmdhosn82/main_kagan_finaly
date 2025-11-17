#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Module - Main window and login dialog with glassmorphism design
Supports RTL layout for Persian language
"""

from PyQt5.QtWidgets import (QMainWindow, QDialog, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QStackedWidget, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

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


class LoginDialog(QDialog):
    """Login dialog with glassmorphism design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ورود به سیستم - Kagan")
        self.setFixedSize(400, 300)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the login UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("سیستم مدیریت کسب و کار کاگان")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Vazir", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("کافه - آرایشگاه - گیم نت")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Vazir", 10))
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("نام کاربری:")
        username_label.setFont(QFont("Vazir", 10))
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont("Vazir", 10))
        self.username_input.setPlaceholderText("نام کاربری خود را وارد کنید")
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("رمز عبور:")
        password_label.setFont(QFont("Vazir", 10))
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Vazir", 10))
        self.password_input.setPlaceholderText("رمز عبور خود را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(10)
        
        # Login button
        login_btn = QPushButton("ورود")
        login_btn.setFont(QFont("Vazir", 12, QFont.Bold))
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Connect Enter key to login
        self.password_input.returnPressed.connect(self.handle_login)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Simple authentication (in production, use proper authentication)
        # For now, accept any non-empty username and password
        if username and password:
            # In production: verify credentials against database
            # For demo: accept "admin" / "admin" or any non-empty credentials
            self.accept()
        else:
            # Show error message
            self.username_input.setStyleSheet("border: 2px solid #e74c3c;")
            self.password_input.setStyleSheet("border: 2px solid #e74c3c;")
    
    def apply_styles(self):
        """Apply glassmorphism styles to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 12px;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 10px;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4);
                border: 2px solid rgba(255, 255, 255, 0.6);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سیستم مدیریت کاگان - Kagan Business Manager")
        self.setMinimumSize(1200, 700)
        self.setLayoutDirection(Qt.RightToLeft)
        
        # Initialize modules
        self.modules = {}
        self.current_module = None
        
        self.setup_ui()
        self.apply_styles()
        
        # Show the first module by default
        self.show_module('salon')
    
    def setup_ui(self):
        """Setup the main window UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create stacked widget for content area
        self.content_stack = QStackedWidget()
        
        # Create sidebar
        sidebar = self.create_sidebar()
        
        # Add to main layout (RTL: content on right, sidebar on left)
        main_layout.addWidget(self.content_stack, 1)
        main_layout.addWidget(sidebar)
        
        central_widget.setLayout(main_layout)
    
    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        # Logo/Title
        title = QLabel("کاگان")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Vazir", 18, QFont.Bold))
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)
        
        subtitle = QLabel("مدیریت کسب و کار")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Vazir", 10))
        subtitle.setObjectName("sidebarSubtitle")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        modules = [
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
        
        # Create scroll area for buttons
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setObjectName("sidebarScroll")
        
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        for module_id, label, module_class in modules:
            btn = QPushButton(label)
            btn.setFont(QFont("Vazir", 11))
            btn.setMinimumHeight(45)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, mid=module_id: self.show_module(mid))
            button_layout.addWidget(btn)
            
            # Initialize module
            self.modules[module_id] = module_class()
            self.content_stack.addWidget(self.modules[module_id])
        
        button_layout.addStretch()
        button_widget.setLayout(button_layout)
        scroll.setWidget(button_widget)
        
        layout.addWidget(scroll)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def show_module(self, module_id):
        """Show the selected module"""
        if module_id in self.modules:
            self.content_stack.setCurrentWidget(self.modules[module_id])
            self.current_module = module_id
    
    def apply_styles(self):
        """Apply glassmorphism styles to the main window"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f7fa, stop:1 #c3cfe2);
            }
            
            #sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(102, 126, 234, 0.9), 
                    stop:1 rgba(118, 75, 162, 0.9));
                border-left: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            #sidebarTitle {
                color: white;
                padding: 10px;
            }
            
            #sidebarSubtitle {
                color: rgba(255, 255, 255, 0.8);
                padding-bottom: 10px;
            }
            
            #sidebarScroll {
                background: transparent;
                border: none;
            }
            
            #navButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: white;
                text-align: right;
                padding: 10px 15px;
            }
            
            #navButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            
            #navButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
