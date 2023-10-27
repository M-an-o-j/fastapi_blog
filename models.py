from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    active = Column(Boolean, default=False)
    email = Column(String, unique=True)

    blogs = relationship("Blog", back_populates="author")

# class Blog(Base):
#     __tablename__ = "blogs"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, unique=True)
#     summary = Column(String)
#     paragraph = Column(String)
#     author_id = Column(Integer, ForeignKey("Users.id"))

#     author = relationship(User, back_populates="blogs")

