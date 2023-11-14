from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:12345@localhost/Blog"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

router = FastAPI(debug=True, title="Blog", description="""
    In this Blog,
        Users    
            1. User can SignUp
            2. User can Login to get Access Token
            3. User can Update their details 
        Blogs
            1.User can get all blogs.
            2.User can get a single blog.
            3.User can post a blog.
            4.User can update a blog.
            5.User can delete a blog.
            
""")

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()