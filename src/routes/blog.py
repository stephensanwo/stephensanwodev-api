from bson import ObjectId
from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.blog import Blog, BlogCategory, BlogList
from ..database.blog import *
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


blog_post = APIRouter()


# @route   POST /blog_post
# @desc    Post new blog post
# @access  Private


@blog_post.post("/blog_post", status_code=201)
async def blog_post_data(blog: Blog, background_tasks: BackgroundTasks):

    # Validate the Blog Category
    err = await find_category(blog.category)
    if err:
        raise HTTPException(
            status_code=400, detail="Blog category does not exist")

    # Validate Series ID
    if blog.series_id:
        error = await validate_series_id(blog.series_id)
        if error:
            raise HTTPException(
                status_code=400, detail="Series does not exist")

    # Send blog data to db
    res = await post_new_blog(blog.blog_post())

    return res

# @route   GET /blog_post
# @desc    Get single blog post
# @access  Private


@blog_post.get("/blog_post/{post_id}", status_code=201, response_model=Blog)
async def blog_post_item(post_id: str):

    # Get all blog items to the blog list
    post = await get_blog_by_id(post_id)

    # # Get suggested next reads from series
    # suggested = await get_all_categories()

    # # Get all featured articles to the blog list
    # featured_posts = await get_featured_posts(limit)

    # result = {"blog_posts": blog_list, "featured_posts": featured_posts,
    #           "categories": blog_categories, "top_posts": []}

    return post


# @route   GET /blog_data
# @desc    Get all blog data
# @access  Private

@blog_post.get("/blog_data", status_code=201, response_model=BlogList)
async def blog_data_consolidated(query_category: Optional[str] = None, tag_filter: Optional[str] = None, limit: int = 10, sort_by: Optional[str] = None):
    # Check data in cache

    # Get all blog items to the blog list
    blog_list = await get_all_blogs(limit)

    # Get all blog topics
    blog_categories = await get_all_categories()

    # Get all featured articles to the blog list
    featured_posts = await get_featured_posts(limit)

    result = {"blog_posts": blog_list, "featured_posts": featured_posts,
              "categories": blog_categories, "top_posts": []}

    return result
