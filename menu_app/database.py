import os

import dotenv

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # create_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)  # autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
