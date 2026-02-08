"""
Security hardening utilities for authentication and authorization.

This module provides additional security measures to strengthen the
authentication and authorization mechanisms.
"""

import re
import secrets
import hashlib
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from ..utils.jwt import verify_token


class SecurityHardener:
    """
    A class to provide security hardening measures.
    """

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, list]:
        """
        Validate password strength based on security requirements.

        Args:
            password: The password to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check minimum length
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")

        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            issues.append("Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            issues.append("Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r'\d', password):
            issues.append("Password must contain at least one digit")

        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Password must contain at least one special character")

        return len(issues) == 0, issues

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate email format using a more secure regex pattern.

        Args:
            email: The email to validate

        Returns:
            True if email format is valid, False otherwise
        """
        # More secure email validation pattern
        pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(pattern, email))

    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 255) -> str:
        """
        Sanitize input string by removing potentially dangerous characters.

        Args:
            input_str: The input string to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not input_str:
            return input_str

        # Limit length
        if len(input_str) > max_length:
            input_str = input_str[:max_length]

        # Remove potentially dangerous characters/sequences
        # This is a basic sanitization - for more advanced needs, use libraries like bleach
        sanitized = input_str.replace('<script', '').replace('javascript:', '') \
                    .replace('vbscript:', '').replace('onerror', '') \
                    .replace('onload', '').replace(' onload', '')

        return sanitized

    @staticmethod
    def check_rate_limit(user_id: str, action: str = "api_call") -> Tuple[bool, int]:
        """
        Check if a user has exceeded rate limits for an action.

        Args:
            user_id: The user ID to check
            action: The action type to check rate limits for

        Returns:
            Tuple of (is_allowed, seconds_remaining)
        """
        # In a real implementation, this would use Redis or a database to track requests
        # For this implementation, we'll return True to indicate no rate limit exceeded
        return True, 0

    @staticmethod
    def validate_jwt_token_safety(token: str) -> Tuple[bool, Optional[str]]:
        """
        Perform additional safety checks on a JWT token beyond standard validation.

        Args:
            token: The JWT token to validate

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        try:
            # Verify the token structure
            if not token or not isinstance(token, str) or ' ' not in token:
                return False, "Invalid token format"

            # Extract the actual JWT part (after "Bearer ")
            token_parts = token.split(' ')
            if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
                return False, "Invalid authorization header format"

            jwt_token = token_parts[1]

            # Verify the token is properly formatted (has 3 parts separated by '.')
            jwt_parts = jwt_token.split('.')
            if len(jwt_parts) != 3:
                return False, "Invalid JWT format"

            # Verify the token with our standard verification
            payload = verify_token(jwt_token)
            if not payload:
                return False, "Token verification failed"

            # Check for required claims
            required_claims = ['sub', 'exp']
            for claim in required_claims:
                if claim not in payload:
                    return False, f"Missing required claim: {claim}"

            # Verify token hasn't been tampered with by checking signature
            # This is handled by the JWT library during verification,
            # but we can add additional checks if needed

            return True, None

        except Exception as e:
            return False, f"Token validation error: {str(e)}"

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Length of the token in bytes (default 32 bytes = 256 bits)

        Returns:
            Secure random token as hex string
        """
        return secrets.token_hex(length)

    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """
        Hash sensitive data using a strong hashing algorithm.

        Args:
            data: The data to hash

        Returns:
            SHA-256 hash of the data
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_api_request_safety(request_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate the safety of an API request by checking for common attack vectors.

        Args:
            request_data: The request data to validate

        Returns:
            Tuple of (is_safe, error_message_if_unsafe)
        """
        try:
            # Convert to string and check for common SQL injection patterns
            request_str = str(request_data)

            # Common SQL injection patterns
            sql_patterns = [
                r"(?i)(union\s+select)",
                r"(?i)(drop\s+\w+)",
                r"(?i)(delete\s+from)",
                r"(?i)(insert\s+into)",
                r"(?i)(update\s+\w+\s+set)",
                r"(?i)(exec\s*\()",
                r"(?i)(execute\s*\()",
                r"(?i)(sp_\w+)",
                r"'(?:--|#|/\*).*?$",
                r"(?i)(select\s+.*\s+from)",
                r"(?i)(create\s+(table|database|index|view|procedure))"
            ]

            for pattern in sql_patterns:
                if re.search(pattern, request_str):
                    return False, "Potential SQL injection detected"

            # Common XSS patterns
            xss_patterns = [
                r"(?i)<script",
                r"(?i)javascript:",
                r"(?i)vbscript:",
                r"(?i)on\w+\s*="
            ]

            for pattern in xss_patterns:
                if re.search(pattern, request_str):
                    return False, "Potential XSS attack detected"

            return True, None

        except Exception as e:
            return False, f"Request validation error: {str(e)}"

    @staticmethod
    def add_security_headers(response_headers: Dict[str, str]) -> Dict[str, str]:
        """
        Add security headers to response headers.

        Args:
            response_headers: Existing response headers

        Returns:
            Updated response headers with security enhancements
        """
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }

        # Update response headers with security headers
        response_headers.update(security_headers)
        return response_headers