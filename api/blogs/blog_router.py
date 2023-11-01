from fastapi import APIRouter, Depends, Query
from api.blogs.blog_schema import blogresponse, postblogresponse
from sqlalchemy.orm import Session
from configuration.Database import *
from typing import List
from api.blogs.blog_controller import *

controller = blog_controller

@router.get("/blogs/", response_model=List[blogresponse], summary="you can get all blogs here",tags=["Blogs"])
async def get_All_Blog(db: Session = Depends(get_session),limit: int = Query(10, ge=1, le=5),skip: int = Query(0, ge=0) ):
    return controller.getAllBlogsController(db, limit, skip)

@router.get("/blog/{blog_id}", response_model=blogresponse, summary="You can get single blog here using blog id", tags=["Blogs"])
async def get_Single_blog(blog_id:int,db: Session = Depends(get_session)):
    return controller.getSingleBlogController(db, blog_id)

@router.post("/post_blog/", response_model=blogresponse, tags=["Blogs"], summary="You can post blog here")
async def post_Blog(blog:postblogresponse,token:str ,db: Session = Depends(get_session)):
    return controller.postBlogController(db, blog, token)

@router.put("/update_blog/{blog_id}", response_model=blogresponse, tags=["Blogs"], summary="You can update blog here")
async def update_Blog(blog:postblogresponse ,token:str,blog_id:int,db: Session = Depends(get_session)):
    return controller.updateBlogController(db, blog_id, blog, token)

@router.delete("/delete_blog/{blog_id}", response_model=blogresponse, tags=["Blogs"], summary="You can delete blog here")
async def update_Blog(token:str,blog_id:int,db: Session = Depends(get_session)):
    return controller.deleteBlogController(db, blog_id, token)

@router.get("/user_blogs/{user_id}", response_model=List[blogresponse], tags=["Blogs"], summary="You can delete blog here")
async def update_Blog(user_id:int,db: Session = Depends(get_session)):
    return controller.getUserBlogsController(db, user_id)
