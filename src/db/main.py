from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.config import Config
from src.db.models import Book
from sqlmodel import SQLModel


async_engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo=True,
)


async def init_db():
    async with async_engine.begin() as conn:
 
        await conn.run_sync(SQLModel.metadata.create_all)

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,       
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    