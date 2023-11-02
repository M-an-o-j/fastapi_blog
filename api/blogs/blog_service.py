from fastapi import  HTTPException, status
from api.blogs.blog_model import Blog
from api.users.user_model import User
from fastapi.responses import JSONResponse
from utills.handlers import *

class blog_services:
    def getAllBlogsservice(db, limit, skip):
        try:
            db_blogs = db.query(Blog).all()
            Blogs = db_blogs[skip:skip+limit]
            return Blogs
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Internal server error")


    def postblogservice(db, blog, user_id):
        try:
            db_user = filter_items(db, User, User.id, user_id).first()
            blog.author_id = db_user.id
            db_blog = Blog(**blog.dict())
            db.add(db_blog)
            db.commit()
            db.refresh(db_blog)
            return db_blog
        except Exception as e:
            errorhandler(500, "Internal server error")


    def getsingleblogservice(db, db_blog):
        Author_name = filter_items(db,User,User.id,db_blog.author_id).first().username
        return JSONResponse({
            "message": "Fetched blog successfully",
            "blog": {
                "title": db_blog.title,
                "summary": db_blog.summary,
                "paragraph": db_blog.paragraph,
                "author": Author_name
            }
        })
    
    def getuserblogsservice(db, db_blogs):
         return db_blogs

    def updateblogservice(db, db_blog, blog):
        if blog.title != "":
            db_blog.title = blog.title
        if blog.summary != "":
            db_blog.summary = blog.summary
        if blog.paragraph != "":
            db_blog.paragraph = blog.paragraph
        db.commit()

        return db_blog

    def deleteblogservice(db, db_blog):
        db.delete(db_blog)
        db.commit()
        return JSONResponse({
            "status code":status.HTTP_200_OK,
            "message":"Blog deleted succesfully"
        })
        