from fastapi import FastAPI
from src.routes.blog import blog_post
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()
api.include_router(blog_post)

origins = [
    "http://localhost:3010",
    "http://192.168.0.149:3010"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/test")
async def root():
    return 'Success'


if __name__ == "__main__":
    uvicorn.run("api:api", host="0.0.0.0", port=2304, reload=True)
