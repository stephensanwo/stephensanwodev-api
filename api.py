from fastapi import FastAPI
from blog.routes.blog import blog_post
from blog.routes.code import code_post
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from gunicorn.app.base import BaseApplication
import os
from dotenv import load_dotenv
# import multiprocessing
import logging
from fastapi.logger import logger as fastapi_logger
from playground.gptj.routes.chat import chat


load_dotenv()

api = FastAPI()
api.include_router(blog_post)
api.include_router(code_post)
api.include_router(chat)

origins = [
    "http://localhost:3010",
    "http://192.168.0.149:3010",
    "http://localhost:3019",
    "http://192.168.0.149:3019",
    "https://ai.stephensanwo.dev",
    "https://www.stephensanwo.dev",
    "https://stephensanwo.dev"

]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

fastapi_logger.handlers = gunicorn_error_logger.handlers


# def number_of_workers():
#     print((multiprocessing.cpu_count() * 2) + 1)
#     return (multiprocessing.cpu_count() * 2) + 1


# class StandaloneApplication(BaseApplication):
#     """Our Gunicorn application."""

#     def __init__(self, app, options=None):
#         self.options = options or {}
#         self.application = app
#         super().__init__()

#     def load_config(self):
#         config = {
#             key: value for key, value in self.options.items()
#             if key in self.cfg.settings and value is not None
#         }
#         for key, value in config.items():
#             self.cfg.set(key.lower(), value)

#     def load(self):
#         return self.application


@api.get("/test")
async def root():
    return 'Success'


if __name__ == "__main__":
    if os.environ.get('APP_ENV') == "development":
        fastapi_logger.setLevel(logging.DEBUG)
        uvicorn.run("api:api", host="0.0.0.0", port=2304, reload=True)

else:
    fastapi_logger.setLevel(gunicorn_logger.level)

    # else:

    # options = {
    #     "bind": "0.0.0.0:2304",
    #     "workers": number_of_workers(),
    #     "accesslog": "-",
    #     "errorlog": "-",
    #     "worker_class": "uvicorn.workers.UvicornWorker",
    #     "timeout": 0
    # }

    # StandaloneApplication(api, options).run()
