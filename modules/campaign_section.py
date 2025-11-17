#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Campaign Section Module
Manages marketing campaigns and promotional activities
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CampaignSection(QWidget):
    """Campaign management section"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the campaign section UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("بخش کمپین ها")
        title.setFont(QFont("Vazir", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("مدیریت کمپین‌های بازاریابی و فعالیت‌های تبلیغاتی")
        description.setFont(QFont("Vazir", 12))
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def apply_styles(self):
        """Apply styles to the campaign section"""
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
