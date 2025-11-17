#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Kagan Business Management System
Supports cafe-bar, salon, and gaming net management
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui import MainWindow, LoginDialog


def main():
    """Main application entry point"""
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Kagan Business Manager")
    app.setOrganizationName("Kagan")
    app.setOrganizationDomain("kagan.local")
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Show login dialog first
    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        # If login successful, show main window
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        # If login cancelled or failed, exit
        sys.exit(0)


if __name__ == "__main__":
    main()
