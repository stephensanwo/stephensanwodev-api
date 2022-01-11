from bson import ObjectId
from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.code import Code, CodeList
from ..database.code import *
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


code_post = APIRouter()


# @route   POST /code_post
# @desc    Post new code snippet post
# @access  Private

@code_post.post("/api/v1/blog/code_post", status_code=201)
async def code_post_data(code: Code, background_tasks: BackgroundTasks):

    # Validate the Code Category
    categories = ["Python", "JavaScript", "Tensorflow",
                  "Redis", "Go", "MongoDB", "SQL", "React"]

    if code.category not in categories:
        raise HTTPException(
            status_code=400, detail="Code category does not exist")

    # Send code data to db
    res = await post_new_code(code.code_post())

    return res

# @route   GET /code_post
# @desc    Get single blog post
# @access  Private


@code_post.get("/api/v1/blog/code_post", status_code=200, response_model=CodeList)
async def code_post_item(code_id: Optional[int] = None, code_url: Optional[str] = None):

    if code_url != None:
        # Get all blog items to the blog list
        res = await get_code_by_url(code_url)
        return {"code_posts": res}

    else:
        # Get all code items to the blog list
        res = await get_code_by_id(code_id)
        return {"code_posts": res}


# @route   GET /code_data
# @desc    Get all code data
# @access  Private

@code_post.get("/api/v1/blog/code_data", status_code=200, response_model=CodeList)
async def code_data_consolidated(filter: Optional[str] = None, limit: int = 10):

    categories = ["All Code Snippets", "Python", "JavaScript", "Tensorflow",
                  "Redis", "Go", "MongoDB", "SQL", "React"]

    if filter not in categories:
        raise HTTPException(
            status_code=400, detail="Code category does not exist")

    if filter == "All Code Snippets":
        # Get all code items to the code list
        code_list = await get_all_code(limit, -1)
        return {"code_posts": code_list}

    else:
        code_list = await get_code_by_category(limit, filter, -1)

        return {"code_posts": code_list}
