from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , String, Integer, Float, Boolean, ForeignKey, DateTime
from Database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from api.users.user_model import User

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    summary = Column(String)
    paragraph = Column(String)
    author_id = Column(Integer, ForeignKey("Users.id"))
    created_at = Column(DateTime, default=datetime.now())
    

    author = relationship(User, back_populates="blogs")