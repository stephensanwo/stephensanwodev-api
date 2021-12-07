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


@blog_post.post("/api/v1/blog/blog_post", status_code=201)
async def blog_post_data(blog: Blog, background_tasks: BackgroundTasks):

    # Validate the Blog Category
    err = await find_category(blog.category)
    if err:
        raise HTTPException(
            status_code=400, detail="Blog category does not exist")

    # Send blog data to db
    res = await post_new_blog(blog.blog_post())

    return res

# @route   GET /blog_post
# @desc    Get single blog post
# @access  Private


@blog_post.get("/api/v1/blog/blog_post", status_code=201, response_model=BlogList)
async def blog_post_item(post_id: Optional[int] = None, post_url: Optional[str] = None):

    if post_url != None:
        # Get all blog items to the blog list
        post = await get_blog_by_url(post_url)
        return {"blog_posts": post, "featured_posts": []}

    else:
        # Get all blog items to the blog list
        post = await get_blog_by_id(post_id)
        return {"blog_posts": post, "featured_posts": []}


# @route   GET /blog_data
# @desc    Get all blog data
# @access  Private

@blog_post.get("/api/v1/blog/blog_data", status_code=201, response_model=BlogList)
async def blog_data_consolidated(category: Optional[str] = None, tag_filter: Optional[str] = None, limit: int = 10, sort_by: Optional[str] = None):

    categories = ["All Categories", "APIs and Software Development", "AI and Deep Learning", "Web Development",
                  "Mobile Development", "Data Structures and Algorithms", "Software Development", "Python", "Blockchain Development", "Developer Guides"]

    if category not in categories:
        raise HTTPException(
            status_code=400, detail="Blog category does not exist")

    if category == "All Categories":
        # Get all blog items to the blog list
        blog_list = await get_all_blogs(limit, -1)
        featured_posts = await get_featured_posts(2, 1)

        return {"blog_posts": blog_list, "featured_posts": featured_posts}

    else:
        blog_list = await get_blog_by_category(limit, category, -1)
        featured_posts = await get_featured_posts_for_category(2, category, -1)

        return {"blog_posts": blog_list, "featured_posts": featured_posts}
