import reflex as rx
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def get_session():
    """Provide a transactional scope around a series of operations."""
    config = rx.config.get_config()
    db_url = config.db_url
    if not db_url.startswith("sqlite+aiosqlite") and db_url.startswith("sqlite"):
        db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    engine = create_async_engine(db_url)
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logging.exception(f"Error during database session: {e}")
            await session.rollback()
            raise