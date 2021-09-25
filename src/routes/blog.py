from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.blog import Blog
from ..database.blog import post_new_blog

blog_post = APIRouter()

# @route   POST /blog_post
# @desc    Post new blog post
# @access  Private


@blog_post.post("/blog_post", status_code=201)
async def prophet_model(blog: Blog, background_tasks: BackgroundTasks):

    # Send blog data to db
    res = await post_new_blog(blog.blog_post())

    # cache_df, errors, valid = await get_data_from_cache(prophet_data.project_name)

    # if not valid:
    #     raise HTTPException(status_code=400, detail=errors)

    # res = await prophet_algorithm(cache_df, forecast_days=prophet_data.forecast_days)

    return res
