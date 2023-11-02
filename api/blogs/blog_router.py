from fastapi import APIRouter, Depends, Query
from api.blogs.blog_schema import blogresponse, postblogresponse
from sqlalchemy.orm import Session
from configuration.Database import *
from typing import List
from api.blogs.blog_controller import *
from utills.auth_bearer import *

controller = blog_controller
httpbearer = AdminJWT()

@router.get("/blogs/", response_model=List[blogresponse], summary="you can get all blogs here",tags=["Blogs"])
async def get_All_Blog(db: Session = Depends(get_session),limit: int = Query(10, ge=1, le=5),skip: int = Query(0, ge=0) ):
    return controller.getAllBlogsController(db, limit, skip)

@router.get("/blog/{blog_id}", response_model=blogresponse, summary="You can get single blog here using blog id", tags=["Blogs"])
async def get_Single_blog(blog_id:int,db: Session = Depends(get_session)):
    return controller.getSingleBlogController(db, blog_id)

@router.post("/post_blog/", response_model=blogresponse,dependencies = [Depends(httpbearer)], tags=["Blogs"], summary="You can post blog here")
async def post_Blog(blog:postblogresponse,Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return controller.postBlogController(db, blog, Auth_head)

@router.put("/update_blog/{blog_id}", response_model=blogresponse,dependencies = [Depends(httpbearer)], tags=["Blogs"], summary="You can update blog here")
async def update_Blog(blog:postblogresponse,blog_id:int,Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return controller.updateBlogController(db, blog_id, blog, Auth_head)

@router.delete("/delete_blog/{blog_id}", response_model=blogresponse,dependencies = [Depends(httpbearer)], tags=["Blogs"], summary="You can delete blog here")
async def update_Blog(blog_id:int,Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return controller.deleteBlogController(db, blog_id, Auth_head)

@router.get("/user_blogs/", response_model=List[blogresponse],dependencies = [Depends(httpbearer)], tags=["Blogs"], summary="You can delete blog here")
async def update_Blog(user_id:int,Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return controller.getUserBlogsController(db, user_id)
