from configuration.Database import *
from sqlalchemy import Column , String, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    blogs = relationship("Blog", back_populates="author")
    logs = relationship("Signin_logs", back_populates="User_log" )

class Signin_logs(Base):
    __tablename__ = "Signin_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    logged_in = Column(DateTime)
    logged_out = Column(DateTime)


    User_log = relationship(User, back_populates="logs")