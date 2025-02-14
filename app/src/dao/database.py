from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db.POSTGRES_USER}:{settings.db.POSTGRES_PASSWORD}@{settings.db.POSTGRES_HOST}:{settings.db.POSTGRES_PORT}/{settings.db.POSTGRES_DB}" 

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session