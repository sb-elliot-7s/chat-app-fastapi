from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from settings import get_settings

db_url = get_settings().db_url

engine = create_async_engine(db_url, future=True, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()


async def get_db_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
