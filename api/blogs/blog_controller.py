from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from api.blogs.blog_model import Blog
from api.users.user_model import User
from jose import jwt
from config import SECRET_KEY
from typing import List
from api.blogs.blog_service import getAllBlogsservice, postblogservice, getsingleblogservice, updateblogservice, deleteblogservice

secret = SECRET_KEY


def getAllBlogsController(db):
        return getAllBlogsservice(db)
    

def postBlogController(db, blog, token):
        if blog.title == "" or blog.summary == "" or blog.paragraph == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")
        if len(blog.title) > 20:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title should not exceed 20 characters")
        try:
            username = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
        return postblogservice(db, blog, token, username)

def getSingleBlogController(db, blog_id):
        db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if db_blog is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
        return getsingleblogservice(db, db_blog)

def updateBlogController(db, blog_id, blog, token):
        user_id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
        db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if db_blog is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
        if str(db_blog.author_id) != user_id:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not author of this blog. so, you cant edit or update")
        return updateblogservice(db, db_blog, blog)

def deleteBlogController(db, blog_id, token):
        try:
            user_id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
        except Exception as e:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if db_blog is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
        if str(db_blog.author_id) != user_id:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not author of this blog. so, you cant edit or update")
      
        return deleteblogservice(db, db_blog)
        