# -------- Imports --------
import json
import asyncio

# -------- Json Worker Function --------
async def json_worker(path: str, queue: asyncio.Queue[dict], user_data: dict) -> None:
    # -- Start function
    print("[JSON Worker] Worker starting")
    while True:
        try:
            # -- Get new update
            update = await queue.get()
            try:
                # -- Load the data from the path
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {} # Set to empty if no file found

            account_did = update.get("account_did")
            user_did = update["user_did"]

            # -- Get the update data
            if update.get("type") == "update":
                update_data = {}
                for key, value in update.items():
                    if key not in ["type", "user_did", "account_did"]:
                        update_data[key] = value 
                        
                if user_did not in data[account_did]:
                    data[account_did][user_did] = {} # Set to empty dict if user was not in the file
                data[account_did][user_did].update(update_data)
            
            elif update.get("type") == "remove":
                key = update["setting"]

                if account_did in data and user_did in data[account_did] and key in data[account_did][user_did]:
                    data[account_did][user_did].pop(key, None)
            
            # -- Delete a user's data
            elif update.get("type") == "delete":
                if user_did in data[account_did]:
                    del data[account_did][user_did]

            user_data.clear()
            user_data.update(data)

            # -- Update the file
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[JSON Worker] An error has occured, {e}")
        finally:
            queue.task_done() # Remove task from queue 

