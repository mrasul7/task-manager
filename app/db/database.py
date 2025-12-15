from collections.abc import AsyncGenerator
from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(url=settings.db_settings.DB_URL, echo=False)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session



            
            


