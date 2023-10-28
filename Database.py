from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:12345@localhost/Blog"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()