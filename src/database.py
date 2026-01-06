from fastapi import Depends, APIRouter
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import Base

router = APIRouter()

engine = create_async_engine("sqlite+aiosqlite:///urls.db") 

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/setupDB")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


