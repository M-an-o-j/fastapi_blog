from fastapi import FastAPI
from api.users import user_router
from api.blogs import blog_router

app = FastAPI(debug=True, title="Blog", description="""
    In this Blog,
        Users    
            1. User can SignUp
            2. User can Login to get Access Token
            3. User can Update their details 
        Blogs
            1.User can get all blogs.
            2.User can get a single blog.
            3.User can post a blog.
            4.User can update a blog.
            5.User can delete a blog.
            
""")

app.include_router(user_router.router, prefix="/users")
app.include_router(blog_router.router, prefix="/blogs")