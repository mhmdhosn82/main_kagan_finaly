#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Kagan Business Management System
Supports cafe-bar, salon, and gaming net management
"""

import customtkinter as ctk
import logging
from gui import MainWindow, LoginDialog
from database.db_manager import initialize_database, get_db_manager
from database.models import UserRole
from auth import AuthService
from utils import setup_logging


def initialize_app():
    """Initialize application (database, logging, default data)"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Kagan Business Management System")
    
    # Initialize database
    initialize_database()
    logger.info("Database initialized")
    
    # Create default admin user if no users exist
    create_default_admin()
    logger.info("Application initialization complete")


def create_default_admin():
    """Create default admin user if no users exist"""
    logger = logging.getLogger(__name__)
    db_manager = get_db_manager()
    
    with db_manager.session_scope() as session:
        from database.models import User
        
        # Check if any users exist
        user_count = session.query(User).count()
        
        if user_count == 0:
            try:
                # Create default admin user
                AuthService.create_user(
                    username="admin",
                    password="admin123",
                    full_name="مدیر سیستم",
                    role=UserRole.ADMIN,
                    email="admin@kagan.local"
                )
                logger.info("Default admin user created (username: admin, password: admin123)")
            except Exception as e:
                logger.error(f"Failed to create default admin user: {e}")


def main():
    """Main application entry point"""
    # Initialize application
    initialize_app()
    
    # Set appearance mode and color theme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create login window
    login = LoginDialog()
    login.mainloop()
    
    # If login was successful, show main window
    if login.login_successful:
        app = MainWindow(login.current_user)
        app.mainloop()


if __name__ == "__main__":
    main()
