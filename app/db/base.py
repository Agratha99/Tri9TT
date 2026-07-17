from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Future database models should inherit from this class so they share
    the same SQLAlchemy metadata.
    """