import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AuthValidator:
    """Authentication-specific validation utilities"""
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, Any]:
        """
        Validate password strength
        Returns a dict with 'valid' flag and 'errors' list
        """
        errors = []
        
        # Check minimum length
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        # Check for at least one special character
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
        if not any(c in special_chars for c in password):
            errors.append("Password must contain at least one special character")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """
        Validate email format
        Returns a dict with 'valid' flag and 'errors' list
        """
        errors = []
        
        # Basic email pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            errors.append("Invalid email format")
        
        # Check for common disposable email domains
        disposable_domains = [
            "mailinator.com", "tempmail.com", "throwawaymail.com", 
            "fakeinbox.com", "yopmail.com", "guerrillamail.com"
        ]
        
        domain = email.split('@')[-1].lower()
        if domain in disposable_domains:
            errors.append("Disposable email addresses are not allowed")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Any]:
        """
        Validate username format
        Returns a dict with 'valid' flag and 'errors' list
        """
        errors = []
        
        # Check length
        if len(username) < 4:
            errors.append("Username must be at least 4 characters long")
        
        if len(username) > 32:
            errors.append("Username must be at most 32 characters long")
        
        # Check for valid characters (alphanumeric, underscore, hyphen)
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append("Username can only contain letters, numbers, underscores, and hyphens")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }