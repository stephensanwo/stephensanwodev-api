import asyncio
import aioredis
import json
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_AUTH = os.environ['REDIS_AUTH']
REDIS_URL = os.environ['REDIS_URL']
REDIS_PORT = os.environ['REDIS_PORT']

if os.environ["APP_ENV"] == "production":
    connection = f"redis://{REDIS_URL}"

else:
    connection = f"redis://{REDIS_URL}"


async def parse_data_to_cache(token, data):

    redis = await aioredis.from_url(url=connection, port=17446, db=0, password=REDIS_AUTH)

    token_exists = await redis.exists(token)

    if token_exists == 0:
        await redis.rpush(token, json.dumps(data))

    else:
        await redis.rpush(token, json.dumps(data))

    await redis.expire(token, 3600)

    return token_exists


def parse_to_str(x):

    output = "".join(str(list(json.loads(x).keys())
                         [0])) + ": " + str(list(json.loads(x).values())[0])

    return output


async def get_data_from_cache(token):

    redis = await aioredis.from_url(url=connection, port=17446, db=0, password=REDIS_AUTH)

    token_exists = await redis.exists(token)

    if token_exists == 0:
        res = []
        pass

    else:
        res = await redis.lrange(token, start=0, end=-1)
        res = map(parse_to_str, res)

    res = " ".join(res)

    return res
