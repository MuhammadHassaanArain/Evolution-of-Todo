from passlib.context import CryptContext


# Create password context for hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the provided password
    """
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength requirements
    """
    # At least 8 characters
    if len(password) < 8:
        return False

    # Contains at least one uppercase, one lowercase, one digit
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit