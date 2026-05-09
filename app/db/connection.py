from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(settings.DATABASE_URL,pool_pre_ping=True)
session_local=sessionmaker(autocommit=False,autoflush=False,bind=engine)
class Base(DeclarativeBase):
    pass
def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()