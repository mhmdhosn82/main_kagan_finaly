#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS Section Module
Manages SMS messaging and notifications
Uses sms_service.py for SMS operations
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SmsSection(QWidget):
    """SMS management section"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the SMS section UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("بخش پیامک")
        title.setFont(QFont("Vazir", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("مدیریت پیامک‌ها و اعلان‌ها")
        description.setFont(QFont("Vazir", 12))
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def apply_styles(self):
        """Apply styles to the SMS section"""
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
