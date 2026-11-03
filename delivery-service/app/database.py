from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

engine = create_async_engine(url=settings.database_url)

Sessionlocal = async_sessionmaker(bind=engine)

async def get_db():
  async with Sessionlocal() as session:
    yield session
