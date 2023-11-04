from api.blogs.blog_service import *
from utills.handlers import *
from utills.auth_handler import *
from utills.validations import *

class blog_controller(Validations,blog_services):

    def __init__(self, model):
          super().__init__(Blog, User)
          self.model = model

    def getAllBlogsController(self,db, limit, skip):
            return super().getAllBlogsservice(db, limit, skip)
        
    def postBlogController(self,db, blog, Auth_head):
            if super().None_validation(blog.title, blog.summary, blog.paragraph, blog.author_id):
                  errorhandler(400, "All field is required")
            if super().empty_validation(blog) == False:
                errorhandler(400, "All field are required")
            if len(blog.title) > 20:
                errorhandler(400,"Title should not exceed 20 characters")
            user_id = decode_token_id(Auth_head)
            
            return super().postblogservice(db, blog, user_id)

    def getSingleBlogController(self,db, blog_id):
            db_blog = filter_items(db, self.model, self.model.id, blog_id).first()
            if db_blog is None:
                errorhandler(404, "Blog not found")

            return super().getsingleblogservice(db, db_blog)
            
    def getUserBlogsController(self,db, Auth_head):
            user_id = decode_token_id(Auth_head,db)
            db_blogs = filter_items(db,self.model,self.model.author_id,user_id).all()
            if db_blogs == []:
                errorhandler(404, "User didn't wrote any blogs")

            return super().getuserblogsservice(db, db_blogs)

    def updateBlogController(self,db, blog_id, blog, Auth_head):
            id = decode_token_id(Auth_head, db)
            db_blog = filter_items(db, self.model, self.model.id, blog_id).first()
            if db_blog is None:
                errorhandler(404, "Blog not found")
            if db_blog.author_id != id:
                errorhandler(401, "You are not the author of this blog. so, you can't edit or update")

            return super().updateblogservice(db, db_blog, blog)

    def deleteBlogController(self,db, blog_id, Auth_head):
            db_blog = filter_items(db,self.model,self.model.id,blog_id).first()
            user_id = decode_token_id(Auth_head,db)
            if db_blog is None:
                errorhandler(404, "Blog not found")
            if db_blog.author_id != user_id:
                errorhandler(401, "You are not the author of this blog. so, you can't delete")
        
            return super().deleteblogservice(db, db_blog.id)
            