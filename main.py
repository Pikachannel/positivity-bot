# -------- Imports --------
from src.jetstream import Websocket
from src.followers import refresh_followers
from src.worker import worker
from src.dm_worker import DmWorker
from src.settings import CommandManager
from src.post import PostManager
from src.client import login
from src.json_worker import json_worker
import asyncio
import os
import json
from dotenv import load_dotenv

# -------- Variables --------
load_dotenv()

# -- Account info
HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT_DID = os.getenv("ACCOUNT_DID")

# -- File paths
MESSAGES_JSON_PATH = "data/messages.json"
USER_DATA_PATH = "data/user_data.json"

# -- Setup followers
followers_set = set()

# -------- Load json files --------
with open(MESSAGES_JSON_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)["messages"]

with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f)

# ------ Main Function --------
async def main() -> None:
    # -- Setup client connection
    client = await login(HANDLE, PASSWORD)
    if not client:
        input("[Main] Press enter to exit...")
        return

    # -- Create queues
    queue = asyncio.Queue()
    json_queue = asyncio.Queue()

    # -- Setup classes
    ws = Websocket()
    command_manager = CommandManager(user_data, json_queue)
    dm_worker = DmWorker(client, command_manager, json_queue, ACCOUNT_DID)
    post_manager = PostManager()

    # -- Start all functions as background tasks
    asyncio.create_task(refresh_followers(client, followers_set, ACCOUNT_DID))
    asyncio.create_task(dm_worker.start())
    for _ in range(3):
        asyncio.create_task(worker(client, queue, followers_set, ACCOUNT_DID, messages, user_data, post_manager))
    
    asyncio.create_task(json_worker(USER_DATA_PATH, json_queue, user_data))

    # -- Setup websocket connection to the bsky jetstream
    await ws.connect(queue)
