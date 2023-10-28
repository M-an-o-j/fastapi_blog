from Database import Base
from sqlalchemy import Column , String, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    active = Column(Boolean, default=False)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    blogs = relationship("Blog", back_populates="author")