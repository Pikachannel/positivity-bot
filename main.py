# -------- Imports --------
from src.jetstream import Websocket
from src.followers import refresh_followers
from src.worker import worker
from src.dm_worker import DmWorker
from src.settings import CommandManager
from src.post import PostManager
from src.filters import Filters
from src.client import login
from src.json_worker import json_worker
import asyncio
import os
import json
from dotenv import load_dotenv

# -------- Variables --------
load_dotenv()

# -- Account info
HANDLES = [os.getenv("HANDLE"), os.getenv("HANDLE_2")]
PASSWORDS = [os.getenv("PASSWORD"), os.getenv("PASSWORD_2")]
ACCOUNT_DIDS = [os.getenv("ACCOUNT_DID"), os.getenv("ACCOUNT_DID_2")]

bots  = {
    ACCOUNT_DIDS[0]: {},
    ACCOUNT_DIDS[1]: {}
}

# -- File paths
MESSAGES_JSON_PATH = "data/messages.json"
USER_DATA_PATH = "data/user_data.json"

# -- Setup followers
followers_set = {
    ACCOUNT_DIDS[0]: set(),
    ACCOUNT_DIDS[1]: set()
}

# -------- Load json files --------
with open(MESSAGES_JSON_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)["messages"]

with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f)

# ------ Main Function --------
async def main() -> None:
    # -- Setup client connection
    queues = []

    for i in range(len(ACCOUNT_DIDS)):
        client = await login(HANDLES[i], PASSWORDS[i])
        if not client:
            input("[Main] Press enter to exit...")
            return
        bots[ACCOUNT_DIDS[i]]["client"] = client

    # -- Create queues
    json_queue = asyncio.Queue(maxsize=50)

    # -- Setup classes
    ws = Websocket()
    command_manager = CommandManager(user_data, json_queue)
    dm_worker = DmWorker(bots, command_manager, json_queue, ACCOUNT_DIDS)

    filters = Filters(client)

    post_manager = PostManager(bots, user_data, ACCOUNT_DIDS, messages, filters)

    # -- Start global workers
    asyncio.create_task(dm_worker.start())
    asyncio.create_task(json_worker(USER_DATA_PATH, json_queue, user_data))

    # -- Start per bot queues and workers
    for i in range(len(ACCOUNT_DIDS)):
        queues.append(asyncio.Queue(maxsize=300))
        asyncio.create_task(refresh_followers(client, followers_set[ACCOUNT_DIDS[i]], ACCOUNT_DIDS[i]))
        asyncio.create_task(worker(bots[ACCOUNT_DIDS[i]]["client"], queues[i], followers_set[ACCOUNT_DIDS[i]], ACCOUNT_DIDS[i], messages, user_data, post_manager))


    # -- Setup websocket connection to the bsky jetstream
    await ws.connect(queues)

