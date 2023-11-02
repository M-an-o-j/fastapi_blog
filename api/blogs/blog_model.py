from sqlalchemy import Column , String, Integer,ForeignKey, DateTime, Boolean
from configuration.Database import Base
from sqlalchemy.orm import relationship
from api.users.user_model import User

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    summary = Column(String)
    paragraph = Column(String)
    is_deleted = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("Users.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    author = relationship("User", back_populates="blogs")