from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Better Auth Configuration (if using Better Auth framework)
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")

# Security settings
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "your-salt-change-in-production")

# Token expiration settings
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Rate limiting (if needed)
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
RATE_LIMIT_WINDOW_MINUTES = int(os.getenv("RATE_LIMIT_WINDOW_MINUTES", "60"))


class AuthSettings:
    """
    Authentication settings for the application.
    """

    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS
        self.security_password_hash = SECURITY_PASSWORD_HASH
        self.security_password_salt = SECURITY_PASSWORD_SALT
        self.rate_limit_max_requests = RATE_LIMIT_MAX_REQUESTS
        self.rate_limit_window_minutes = RATE_LIMIT_WINDOW_MINUTES

    def get_access_token_expires_delta(self) -> timedelta:
        """
        Get the timedelta for access token expiration.
        """
        return timedelta(minutes=self.access_token_expire_minutes)

    def get_refresh_token_expires_delta(self) -> timedelta:
        """
        Get the timedelta for refresh token expiration.
        """
        return timedelta(days=self.refresh_token_expire_days)


# Create a single instance of auth settings
auth_settings = AuthSettings()


def verify_secret_key() -> bool:
    """
    Verify that the secret key is properly configured.
    """
    return len(SECRET_KEY) >= 32  # Good practice to have at least 32 characters


def get_security_headers() -> dict:
    """
    Get recommended security headers for API responses.
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }