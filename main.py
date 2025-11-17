#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Kagan Business Management System
Supports cafe-bar, salon, and gaming net management
"""

import customtkinter as ctk
from gui import MainWindow, LoginDialog


def main():
    """Main application entry point"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create login window
    login = LoginDialog()
    login.mainloop()
    
    # If login was successful, show main window
    if login.login_successful:
        app = MainWindow()
        app.mainloop()


if __name__ == "__main__":
    main()
