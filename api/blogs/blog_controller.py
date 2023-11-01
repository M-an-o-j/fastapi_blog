from fastapi import HTTPException, status
from api.blogs.blog_model import Blog
from jose import jwt
from typing import List
from api.blogs.blog_service import *
from utills.error import *
from utills.auth_handler import *

secret = SECRET_KEY

service = blog_services

class blog_controller:
    def getAllBlogsController(db, limit, skip):
            return service.getAllBlogsservice(db, limit, skip)
        

    def postBlogController(db, blog, token):
            if blog.title == "" or blog.summary == "" or blog.paragraph == "":
                error(400, "All field are required")

            if len(blog.title) > 20:
                error(400,"Title should not exceed 20 characters")
                
            try:
                user_id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                error(401, "Invalid Token")
            
            return service.postblogservice(db, blog, user_id)

    def getSingleBlogController(db, blog_id):
            db_blog = db.query(Blog).filter(Blog.id == blog_id).first()

            if db_blog is None:
                error(404, "Blog not found")

            return service.getsingleblogservice(db, db_blog)
            
    def getUserBlogsController(db, user_id):
            db_blogs = db.query(Blog).filter(Blog.author_id == user_id).all()
            print(db_blogs)
            if db_blogs == []:
                error(404, "User didn't wrote any blogs")

            return service.getuserblogsservice(db, db_blogs)

    def updateBlogController(db, blog_id, blog, token):
            user_id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            db_blog = db.query(Blog).filter(Blog.id == blog_id).first()

            if db_blog is None:
                error(404, "Blog not found")

            if str(db_blog.author_id) != user_id:
                error(401, "You are not author of this blog. so, you can't edit or update")

            return service.updateblogservice(db, db_blog, blog)

    def deleteBlogController(db, blog_id, token):
            db_blog = db.query(Blog).filter(Blog.id == blog_id).first()

            try:
                user_id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                error(400, "You are not author of this blog. so, you can't edit or update")

            if db_blog is None:
                error(404, "Blog not found")

            if str(db_blog.author_id) != user_id:
                error(401, "You are not a author of this blog. so, you cant edit or update")
        
            return service.deleteblogservice(db, db_blog)
            