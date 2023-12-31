from fastapi import  HTTPException, status
from api.blogs.blog_model import Blog
from api.users.user_model import User
from fastapi.responses import JSONResponse
from utills.handlers import *
import datetime

class blog_services:

    def __init__(self, Blog, User):
        self.blog = Blog
        self.user = User

    def getAllBlogsservice(self,db, limit, skip):
        try:
            db_blogs = db.query(self.blog).all()
            Blogs = db_blogs[skip:skip+limit]
            return Blogs
        except Exception as e:
            errorhandler(400,"INternal server error")

    def postblogservice(self,db, blog, user_id):
        try:
            db_user = filter_items(db, self.user, self.user.id, user_id).first()
            blog.author_id = db_user.id
            db_blog = Blog(**blog.dict(),created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.add(db_blog)
            db.commit()
            db.refresh(db_blog)
            return db_blog
        except Exception as e:
            errorhandler(500, f"Internal server error {e}")


    def getsingleblogservice(self,db, db_blog):
        Author_name = filter_items(db,self.user,self.user.id,db_blog.author_id).first().username
        return JSONResponse({
            "message": "Fetched blog successfully",
            "blog": {
                "title": db_blog.title,
                "summary": db_blog.summary,
                "paragraph": db_blog.paragraph,
                "author": Author_name
            }
        })
    
    def getuserblogsservice(self,db, db_blogs):
         return db_blogs

    def updateblogservice(db, db_blog, blog):
        if blog.title != "" and blog.title != None:
            db_blog.title = blog.title
        if blog.summary != "" and blog.summary != None:
            db_blog.summary = blog.summary
        if blog.paragraph != "" and blog.paragraph != None:
            db_blog.paragraph = blog.paragraph
        db_blog.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.commit()

        return db_blog

    def deleteblogservice(self,db, blog_id):                                                                            
        db_blog = db.query(self.blog).get(blog_id)
        db_blog.title = True    
        db_blog.is_delete = True
        db.commit()
        return JSONResponse({
            "status code":status.HTTP_200_OK,
            "message":"Blog deleted succesfully"
        })
        