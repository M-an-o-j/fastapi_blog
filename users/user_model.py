from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , String, Integer, Float

User_Base = declarative_base()

class User(User_Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True)
    
