from fastapi import FastAPI
from users import user_router

app = FastAPI(debug=True)

app.include_router(user_router.router)