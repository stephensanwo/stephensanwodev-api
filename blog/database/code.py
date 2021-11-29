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
Code
"""


async def post_new_code(code_data):
    db = create_db_connection()
    code = db.get_collection('code')
    code = await code.insert_one(code_data)
    result = {"code_id": str(code.inserted_id)}
    return result


async def get_all_code(length):
    db = create_db_connection()
    code = db.get_collection('code')
    codes = await code.find().to_list(length=length)

    return codes


async def get_code_by_category(length, category):
    db = create_db_connection()
    code = db.get_collection('code')
    codes = await code.find({'category': category}).to_list(length=length)

    return codes


async def get_code_by_id(code_id):
    db = create_db_connection()
    code = db.get_collection('code')
    post = await code.find({"code_id": {"$gte": str(code_id), "$lt": str(code_id + 4)}}).to_list(length=4)

    return post
