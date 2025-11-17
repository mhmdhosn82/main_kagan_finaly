#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager
Handles database connections, initialization, and session management
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager singleton"""
    
    _instance = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def initialize(self, db_url=None):
        """
        Initialize the database connection
        
        Args:
            db_url (str): Database URL. Defaults to SQLite in current directory
        """
        if db_url is None:
            # Default to SQLite database in current directory
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kagan_db.sqlite')
            db_url = f'sqlite:///{db_path}'
        
        logger.info(f"Initializing database: {db_url}")
        
        # Create engine
        self._engine = create_engine(
            db_url,
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True  # Verify connections before using
        )
        
        # Create session factory
        self._session_factory = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=False)
        )
        
        # Create all tables
        Base.metadata.create_all(self._engine)
        logger.info("Database initialized successfully")
    
    def get_session(self):
        """
        Get a database session
        
        Returns:
            Session: SQLAlchemy session object
        """
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._session_factory()
    
    def remove_session(self):
        """Remove the current session"""
        if self._session_factory:
            self._session_factory.remove()
    
    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope for database operations
        
        Usage:
            with db_manager.session_scope() as session:
                session.add(object)
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Create all database tables"""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        Base.metadata.create_all(self._engine)
        logger.info("All tables created")
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        Base.metadata.drop_all(self._engine)
        logger.info("All tables dropped")
    
    def reset_database(self):
        """Reset the database (drop and recreate all tables)"""
        logger.warning("Resetting database - all data will be lost!")
        self.drop_tables()
        self.create_tables()
        logger.info("Database reset complete")


# Global database manager instance
_db_manager = DatabaseManager()


def get_session():
    """
    Convenience function to get a database session
    
    Returns:
        Session: SQLAlchemy session object
    """
    return _db_manager.get_session()


def initialize_database(db_url=None):
    """
    Initialize the database
    
    Args:
        db_url (str): Database URL. Defaults to SQLite in current directory
    """
    _db_manager.initialize(db_url)


def get_db_manager():
    """
    Get the database manager instance
    
    Returns:
        DatabaseManager: The database manager singleton
    """
    return _db_manager
