from api.users.user_router import *
from api.blogs.blog_router import *
from configuration.Database import *
import uvicorn

Base.metadata.create_all(bind=engine)
router.mount('/api/v1/', router)

if __name__ == "__main__":
    uvicorn.run("main:router",host="localhost",port=5004,reload=True) 
