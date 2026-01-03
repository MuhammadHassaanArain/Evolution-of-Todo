from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to provide database session
    """
    with Session(engine) as session:
        yield session