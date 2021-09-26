import motor.motor_asyncio
from pydantic import EmailStr
from bson.objectid import ObjectId


def create_db_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.stephensanwodev
    return db


def close_db_connection(db):
    db.close()


async def post_new_blog(blog_data):
    db = create_db_connection()
    blog = db.get_collection('blog')
    blog = await blog.insert_one(blog_data)
    result = {"blog_id": str(blog.inserted_id)}
    return result


async def get_all_blogs(length):
    db = create_db_connection()
    blog = db.get_collection('blog')
    blogs = await blog.find().to_list(length=length)

    return blogs


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


async def add_post_to_series(series_id):
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
