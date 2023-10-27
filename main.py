from fastapi import FastAPI
from users import user_router

app = FastAPI(debug=True, title="Blog", description="""
    In this Blog,
            1. You can create user
            2. You can use login credential to login and get access token
""")

app.include_router(user_router.router, prefix="/users")