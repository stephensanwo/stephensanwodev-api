import motor.motor_asyncio
from pydantic import EmailStr


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
