from fastapi import FastAPI
import uvicorn
from users import router as users_router
from blogposts import router as blogposts_router
from comments import router as comments_router

app = FastAPI()

app.include_router(users_router)
app.include_router(blogposts_router)
app.include_router(comments_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)
