#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authentication Module
User authentication and password management with bcrypt
"""

import bcrypt
import logging
from database.models import User, UserRole
from database.db_manager import get_db_manager

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Exception raised for authentication failures"""
    pass


class AuthService:
    """Authentication service for user login and password management"""
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using bcrypt
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """
        Verify a password against its hash
        
        Args:
            password (str): Plain text password to verify
            password_hash (str): Hashed password from database
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate a user with username and password
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            User: User object if authentication successful
            
        Raises:
            AuthenticationError: If authentication fails
        """
        db_manager = get_db_manager()
        
        with db_manager.session_scope() as session:
            # Find user by username
            user = session.query(User).filter_by(username=username).first()
            
            if user is None:
                logger.warning(f"Authentication failed: User '{username}' not found")
                raise AuthenticationError("نام کاربری یا رمز عبور اشتباه است")
            
            if not user.is_active:
                logger.warning(f"Authentication failed: User '{username}' is inactive")
                raise AuthenticationError("حساب کاربری غیرفعال است")
            
            # Verify password
            if not AuthService.verify_password(password, user.password_hash):
                logger.warning(f"Authentication failed: Invalid password for user '{username}'")
                raise AuthenticationError("نام کاربری یا رمز عبور اشتباه است")
            
            logger.info(f"User '{username}' authenticated successfully")
            return user
    
    @staticmethod
    def create_user(username, password, full_name, role=UserRole.STAFF, email=None, phone=None):
        """
        Create a new user
        
        Args:
            username (str): Username (must be unique)
            password (str): Plain text password (will be hashed)
            full_name (str): User's full name
            role (UserRole): User role
            email (str): Email address
            phone (str): Phone number
            
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If username already exists
        """
        db_manager = get_db_manager()
        
        with db_manager.session_scope() as session:
            # Check if username already exists
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                raise ValueError(f"نام کاربری '{username}' قبلا استفاده شده است")
            
            # Hash password
            password_hash = AuthService.hash_password(password)
            
            # Create user
            user = User(
                username=username,
                password_hash=password_hash,
                full_name=full_name,
                role=role,
                email=email,
                phone=phone
            )
            
            session.add(user)
            session.flush()  # Ensure user is added to session
            
            logger.info(f"User '{username}' created successfully")
            return user
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Change a user's password
        
        Args:
            user_id (int): User ID
            old_password (str): Current password
            new_password (str): New password
            
        Raises:
            AuthenticationError: If old password is incorrect
            ValueError: If user not found
        """
        db_manager = get_db_manager()
        
        with db_manager.session_scope() as session:
            user = session.query(User).filter_by(id=user_id).first()
            
            if user is None:
                raise ValueError("کاربر یافت نشد")
            
            # Verify old password
            if not AuthService.verify_password(old_password, user.password_hash):
                raise AuthenticationError("رمز عبور فعلی اشتباه است")
            
            # Hash and set new password
            user.password_hash = AuthService.hash_password(new_password)
            
            logger.info(f"Password changed for user '{user.username}'")
    
    @staticmethod
    def reset_password(user_id, new_password):
        """
        Reset a user's password (admin function)
        
        Args:
            user_id (int): User ID
            new_password (str): New password
            
        Raises:
            ValueError: If user not found
        """
        db_manager = get_db_manager()
        
        with db_manager.session_scope() as session:
            user = session.query(User).filter_by(id=user_id).first()
            
            if user is None:
                raise ValueError("کاربر یافت نشد")
            
            # Hash and set new password
            user.password_hash = AuthService.hash_password(new_password)
            
            logger.info(f"Password reset for user '{user.username}'")


class PermissionChecker:
    """Check user permissions based on roles"""
    
    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return user.role == UserRole.ADMIN
    
    @staticmethod
    def is_manager_or_above(user):
        """Check if user is a manager or admin"""
        return user.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    @staticmethod
    def can_edit_users(user):
        """Check if user can edit other users"""
        return user.role == UserRole.ADMIN
    
    @staticmethod
    def can_view_reports(user):
        """Check if user can view financial reports"""
        return user.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    @staticmethod
    def can_manage_inventory(user):
        """Check if user can manage inventory"""
        return user.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    @staticmethod
    def can_process_payments(user):
        """Check if user can process payments"""
        return user.role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF]
