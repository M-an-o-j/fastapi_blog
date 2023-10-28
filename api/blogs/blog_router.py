from fastapi import APIRouter, Depends
from api.blogs.blog_schema import blogresponse, postblogresponse
from sqlalchemy.orm import Session
from Database import get_session
from typing import List
from api.blogs.blog_controller import getAllBlogsController, postBlogController, getSingleBlogController, updateBlogController

router = APIRouter()

@router.get("/blogs/", response_model=List[blogresponse], tags=["Blogs"])
async def get_All_Blog(db: Session = Depends(get_session)):
    return getAllBlogsController(db)

@router.get("/update_blog/{blog_id}", response_model=blogresponse, tags=["Blogs"])
async def get_Single_blog(blog_id:int,db: Session = Depends(get_session)):
    return getSingleBlogController(db, blog_id)

@router.post("/post_blog/", response_model=blogresponse, tags=["Blogs"])
async def post_Blog(blog:postblogresponse,token:str ,db: Session = Depends(get_session)):
    return postBlogController(db, blog, token)

@router.put("/update_blog/{blog_id}", response_model=blogresponse, tags=["Blogs"])
async def update_Blog(blog:postblogresponse ,token:str,blog_id:int,db: Session = Depends(get_session)):
    return updateBlogController(db, blog_id, blog, token)
