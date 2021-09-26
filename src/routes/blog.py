from bson import ObjectId
from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.blog import Blog, BlogCategory
from ..database.blog import post_new_blog, add_post_to_series, get_all_blogs
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


blog_post = APIRouter()


# @route   POST /blog_post
# @desc    Post new blog post
# @access  Private


@blog_post.post("/blog_post", status_code=201)
async def blog_post_data(blog: Blog, background_tasks: BackgroundTasks):

    # Add article to caegory ID

    # If its a featured post - Add article to featured posts

    # Send blog data to db
    res = await post_new_blog(blog.blog_post())

    # Add blog post to series if series_id is available
    if blog.series_id:
        series, error = await add_post_to_series(blog.series_id)

        print(series)

    # cache_df, errors, valid = await get_data_from_cache(prophet_data.project_name)

    # if not valid:
    #     raise HTTPException(status_code=400, detail=errors)

    # res = await prophet_algorithm(cache_df, forecast_days=prophet_data.forecast_days)

    # test

    return res


# @route   GET /blog_data
# @desc    Get all blog data
# @access  Private

@blog_post.get("/blog_data", status_code=201, response_model=List[Blog])
async def blog_data_consolidated(q: Optional[str] = None, ):
    # Check data in cache

    # Get all blog items to the blog list
    result = await get_all_blogs(100)

    # result = jsonable_encoder(result)

    # Get all featured articles to the blog list

    # res = {"blog_list": result, "featured_articles": [],
    #        "topics": [], "top_posts": []}

    return result
