import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CONN_STRING = os.environ.get('MONGO_CONN_STRING')


def create_db_connection():
    if os.environ.get('APP_ENV') == "development":
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONN_STRING)
        db = client.ai_playground_chatbot_sandbox
        return db

    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONN_STRING)
        db = client.ai_playground_chatbot
        return db


def close_db_connection(db):
    db.close()


"""
Posts
"""


async def post_user_data(user_data):
    db = create_db_connection()
    user = db.get_collection('user')
    user = await user.insert_one(user_data)
    return user
