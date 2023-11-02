from fastapi import HTTPException, status
from api.blogs.blog_model import Blog
from jose import jwt
from typing import List
from api.blogs.blog_service import *
from utills.handlers import *
from utills.auth_handler import *
from utills.validations import *

secret = SECRET_KEY

service = blog_services
validation = validations.User_validations()

class blog_controller:
    def getAllBlogsController(db, limit, skip):
            return service.getAllBlogsservice(db, limit, skip)
        

    def postBlogController(db, blog, Auth_head):
            if validation.empty_validation(blog) == False:
                errorhandler(400, "All field are required")
            if len(blog.title) > 20:
                errorhandler(400,"Title should not exceed 20 characters")
            user_id = decode_token_id(Auth_head)
            
            return service.postblogservice(db, blog, user_id)

    def getSingleBlogController(db, blog_id):
            db_blog = filter_items(db, Blog, Blog.id, blog_id).first()
            if db_blog is None:
                errorhandler(404, "Blog not found")

            return service.getsingleblogservice(db, db_blog)
            
    def getUserBlogsController(db, user_id):
            db_blogs = db.query(Blog).filter(Blog.author_id == user_id).all()
            if db_blogs == []:
                errorhandler(404, "User didn't wrote any blogs")

            return service.getuserblogsservice(db, db_blogs)

    def updateBlogController(db, blog_id, blog, Auth_head):
            id = decode_token_id(Auth_head)
            db_blog = filter_items(db, Blog, Blog.id, blog_id)
            if db_blog is None:
                errorhandler(404, "Blog not found")
            if db_blog.author_id != id:
                errorhandler(401, "You are not the author of this blog. so, you can't edit or update")

            return service.updateblogservice(db, db_blog, blog)

    def deleteBlogController(db, blog_id, Auth_head):
            db_blog = filter_items(db,Blog,Blog.id,blog_id).first()
            user_id = decode_token_id(Auth_head)
            if db_blog is None:
                errorhandler(404, "Blog not found")
            if db_blog.author_id != user_id:
                errorhandler(401, "You are not the author of this blog. so, you can't delete")
        
            return service.deleteblogservice(db, db_blog)
            