from fastapi import APIRouter, HTTPException, status
from api.blogs.blog_model import Blog
from jose import jwt
from api.users.user_model import User
from config import SECRET_KEY
from fastapi.responses import JSONResponse

secret = SECRET_KEY


def getAllBlogsservice(db):
    try:
        db_blogs = db.query(Blog).all()
        print(db_blogs)
        return db_blogs
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Internal server error")


def postblogservice(db, blog, token, username):
    # username = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
    db_user = db.query(User).filter(User.username == username).first()
    blog.author_id = db_user.id
    db_blog = Blog(**blog.dict())
    author_name = db.query(User).filter(User.id == db_blog.author_id).first()
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)

    return JSONResponse({
        "message": "successfully posted blog",
        "blog": {
            "title": db_blog.title,
            "summary": db_blog.summary,
            "paragraph": db_blog.paragraph,
            "author": author_name.username
        }
    })


def getsingleblogservice(db, db_blog):
    author_name = db.query(User).filter(
        User.id == db_blog.author_id).first().username
    return JSONResponse({
        "message": "Fetched blog successfully",
        "blog": {
            "title": db_blog.title,
            "summary": db_blog.summary,
            "paragraph": db_blog.paragraph,
            "author": author_name
        }
    })

def updateblogservice(db, db_blog, blog):
    if blog.title != "":
        db_blog.title = blog.title
    if blog.summary != "":
        db_blog.summary = blog.summary
    if blog.paragraph != "":
        db_blog.paragraph = blog.paragraph
    db.commit()

    return db_blog

def deleteblogservice():
    return