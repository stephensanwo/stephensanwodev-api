from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.blog import Blog, BlogCategory, Series
from ..database.blog import post_new_category, post_new_series


blog_metadata = APIRouter()

# @route   [POST] /blog_category
# @desc    Post new blog post
# @access  Private


@blog_metadata.post("/api/v1/blog/blog_category", status_code=201)
async def create_blog_category(category: BlogCategory):
    # Send blog category data to db
    res, error = await post_new_category(category.category_data())
    if error:
        raise HTTPException(status_code=400, detail={"msg": res})
    else:
        return res


# @route   [POST] /blog_series
# @desc    Post new blog series
# @access  Private
@blog_metadata.post("/api/v1/blog/blog_series", status_code=201)
async def create_blog_series(series: Series):
    # Send blog series data to db
    res, error = await post_new_series(series.series_data())
    if error:
        raise HTTPException(status_code=400, detail={"msg": res})
    else:
        return res


# @route   [POST] /top_posts
# @desc    Post blog post to top recommended posts
# @access  Private
@blog_metadata.post("/top_posts", status_code=201)
async def create_top_post(series: Series):
    # Send blog series data to db
    res, error = await add(series.series_data())
    if error:
        raise HTTPException(status_code=400, detail={"msg": res})
    else:
        return res
