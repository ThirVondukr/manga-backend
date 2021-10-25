from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import settings

engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    future=True,
    pool_size=20,
)
Base = declarative_base()
Session = sessionmaker(future=True, class_=AsyncSession, bind=engine)
