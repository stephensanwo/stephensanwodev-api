import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, Cookie, Depends, FastAPI, Query, WebSocket, status, Request
from ..model.gptj import GPTJ
from ..middleware.cache import parse_data_to_cache, get_data_from_cache
from ..middleware.db import post_user_data
from typing import Optional
import uuid
import aioredis

chat = APIRouter()

load_dotenv()
REDIS_AUTH = os.environ['REDIS_AUTH']
REDIS_URL = os.environ['REDIS_URL']
REDIS_PORT = os.environ['REDIS_PORT']

if os.environ["APP_ENV"] == "production":
    connection = f"redis://{REDIS_URL}"
    print("Connection Okay")

else:
    connection = f"redis://{REDIS_URL}"


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return session or token

# @route   POST /token
# @desc    Route generating chat token
# @access  Public


@chat.post("/api/v1/playground/token")
async def token_generator(name: str, request: Request, background_tasks: BackgroundTasks):
    token = str(uuid.uuid4())
    client = request.client.host
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    data = {"name": name, "token": token, "ip": client}

    redis = await aioredis.from_url(url=connection, port=17446, db=0, password=REDIS_AUTH)

    await redis.set(token, str(data))

    # send info data to db
    background_tasks.add_task(post_user_data, data)
    # res = await post_user_data(data)
    await redis.expire(token, 3600)

    return data


# @route   POST /refresh_token
# @desc    Route refreshing token
# @access  Public
@chat.post("/api/v1/playground/refresh_token")
async def refresh_token(token: str):

    redis = await aioredis.from_url(url=connection, port=17446, db=0, password=REDIS_AUTH)

    await redis.delete(token)

    return None


# @route   Websocket Route /chat
# @desc    Route for gallium conversational bots
# @access  Public

@chat.websocket("/api/v1/playground/chat/{id}")
async def websocket_endpoint(websocket: WebSocket = WebSocket, id: str = str, token: Optional[str] = None, cookie_or_token: str = Depends(get_cookie_or_token), background_tasks: BackgroundTasks = BackgroundTasks()):
    await websocket.accept()
    data = await websocket.receive_text()
    await parse_data_to_cache(token=cookie_or_token, data={"Human": f"{data}"})

    history = await get_data_from_cache(token=cookie_or_token)

    context = f"""{history} Bot:"""

    print(context)

    # response = f"GPT-J-6b is currently offline, please try again later {id}"

    response = GPTJ.generate(context=context,
                             token_max_length=128, temperature=1.0, top_probability=0.9)

    await parse_data_to_cache(token=cookie_or_token, data={"Bot": f"{response.strip()}"})

    while True:

        await websocket.send_text(f"GPT-J BOT: {response}")
