import motor.motor_asyncio
from pydantic import EmailStr
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CONN_STRING = os.environ.get('MONGO_CONN_STRING')


def create_db_connection():
    if os.environ.get('APP_ENV') == "development":
        #client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONN_STRING)
        db = client.blog_db
        return db

    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONN_STRING)
        db = client.blog_db
        return db


def close_db_connection(db):
    db.close()


"""
Posts
"""


async def post_new_blog(blog_data):
    db = create_db_connection()
    blog = db.get_collection('blog')
    blog = await blog.insert_one(blog_data)
    result = {"blog_id": str(blog.inserted_id)}
    return result


async def get_all_blogs(length, sort_order):
    db = create_db_connection()
    blog = db.get_collection('blog')
    blogs = await blog.find().sort("post_id", sort_order).to_list(length=length)

    return blogs


async def get_blog_by_category(length, category, sort_order):
    db = create_db_connection()
    blog = db.get_collection('blog')
    blogs = await blog.find({'category': category}).sort("post_id", sort_order).to_list(length=length)
    return blogs


async def get_blog_by_id(post_id):
    db = create_db_connection()
    blog = db.get_collection('blog')
    post = await blog.find({"post_id": {"$gte": str(post_id), "$lt": str(post_id + 3)}}).to_list(length=4)

    return post


async def get_blog_by_title(title):
    db = create_db_connection()
    blog = db.get_collection('blog')
    post = await blog.find_one({"title": title})

    post_id = int(post["post_id"])

    posts = await blog.find({"post_id": {"$gte": str(post_id), "$lt": str(post_id + 3)}}).to_list(length=4)

    return posts


"""
Categories/ Topics /
 
"""


async def post_new_category(category_data):
    db = create_db_connection()
    category = db.get_collection('blog_category')

    # Check if record already exists in the db
    if await category.find_one({"category_name": category_data['category_name']}) is None:
        category = await category.insert_one(category_data)
        result = {"category_id": str(category.inserted_id)}
        error = False
        return result, error

    else:
        error = True
        return "Blog category record already exists", error


async def find_category(category_name):
    db = create_db_connection()
    category = db.get_collection('blog_category')

    # Check if category exists in the db
    if await category.find_one({"category_name": category_name}) is None:
        return True
    else:
        return False


async def get_all_categories():
    db = create_db_connection()
    category = db.get_collection('blog_category')

    categories = await category.find().to_list(length=1000)

    return categories


"""
Featured Posts
 
"""


async def get_featured_posts(length, sort_order):
    db = create_db_connection()
    blog = db.get_collection('blog')

    featured = await blog.find({'featured_post': {"$in": ["null", True]}}).sort("post_id", sort_order).to_list(length=length)
    return featured


async def get_featured_posts_for_category(length, category, sort_order):
    db = create_db_connection()
    blog = db.get_collection('blog')

    featured = await blog.find({'category': category, 'featured_post': {"$in": ["null", True]}}).sort("post_id", sort_order).to_list(length=length)

    return featured


"""
Series
"""


async def post_new_series(series_data):
    db = create_db_connection()
    series = db.get_collection('blog_series')

    # Check if record already exists in the db
    if await series.find_one({"series_name": series_data['series_name']}) is None:
        series = await series.insert_one(series_data)
        result = {"series_id": str(series.inserted_id)}
        error = False
        return result, error

    else:
        error = True
        return "Series record already exists", error


async def validate_series_id(series_id):
    db = create_db_connection()
    series = db.get_collection('blog_series')

    # Check if series exists in the db
    if await series.find_one({"_id": ObjectId(series_id)}) is None:
        return True

    else:
        return False


"""
Top Posts
"""


async def add_post_to_top_post(series_id):
    db = create_db_connection()
    series = db.get_collection('blog_series')
    # Check if series exists in the db
    if await series.find_one({"_id": ObjectId(series_id)}) is None:
        error = True
        return "Series does not exist", error

    # Check if series id exists in the series posts
    if series.find({"series_post": ObjectId(series_id)}) is not None:
        error = True
        return "Blog post already in series", error

    else:
        series_data = await series.find_one({"_id": ObjectId(series_id)})

        series_update = await series.update_one({"_id": ObjectId(series_id)}, {'$push': {'series_posts': series_id}})

        result = {"series_data": str(series_update)}
        error = False

        return result, error
