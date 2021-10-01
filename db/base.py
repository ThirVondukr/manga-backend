from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import database_settings

engine = create_async_engine(
    database_settings.database_url,
    echo=database_settings.echo,
    future=True,
    pool_size=20,
)
Base: type = declarative_base(bind=engine)
Session = sessionmaker(future=True, class_=AsyncSession, bind=engine)
