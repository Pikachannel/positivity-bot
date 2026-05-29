# -------- Imports --------
import asyncio

# -------- Command Class --------
class CommandManager:
    def __init__(self, user_data: dict, json_queue: asyncio.Queue) -> None:
        self.user_data = user_data
        self.json_queue = json_queue

    # -------------
    # -- To float
    # Converts a string to a float
    def to_float(self, s: str) -> float | None:
        try:
            return float(s)
        except (TypeError, ValueError):
            return None
        
    # -------------
    # -- Remove setting
    # Removes a specific setting
    async def remove_setting(self, user_did: str, setting: str, account_did: str) -> tuple[bool, str]:
        # -- Add to queue
        payload = {
            "type": "remove",
            "account_did": account_did,
            "user_did": user_did,
            "setting": setting
        }

        await self.json_queue.put(payload)

        return True, f"The setting '{setting}' has been reset to the default value."

    # -------------
    # -- Nickname
    # A string at max 20 characters
    async def update_nickname(self, user_did: str, nickname: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and mormalisation
        if nickname is None:
            return await self.remove_setting(user_did, "nickname", account_did) 

        nickname = nickname.strip()[:20]

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "nickname": nickname
        }
        await self.json_queue.put(payload)

        return True, f"Your nickname has been updated to {nickname}\nYou can change this at any time by sending the same command.\nUse !help at any time to see all commands."

    # -------------
    # -- Chance
    # A float between 0 and 100
    async def chance(self, user_did: str, chance: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and mormalisation
        if chance is None:
            return await self.remove_setting(user_did, "chance", account_did)

        chance_value = self.to_float(chance)
        if chance_value is None:
            return False, "An error occurred while updating your chance setting.\nPlease make sure you only use numbers.\nUse !help at any time to see all commands."

        if chance_value < 0 or chance_value > 100:
            return False, "An error occurred while updating your chance setting.\nPlease make sure your chance is in the range 0-100.\nUse !help at any time to see all commands."

        chance_value = round(chance_value, 2)

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "chance": chance_value
        }

        await self.json_queue.put(payload)

        return True, f"The chance of a reply under your posts has been updated to '{chance_value}%'\nYou can change this at any time by sending the same command.\nUse !help at any time to see all commands."

    # -------------
    # -- Interval
    # A static interval with max time of 3600 seconds
    # A ranged interval between 0 and 3600 seconds
    async def interval(self, user_did: str, interval: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and mormalisation
        if interval is None:
            return await self.remove_setting(user_did, "interval", account_did)
    
        # -- Check if the interval is a range or static value
        intervalSplit = interval.split("-")

        # -- Range
        if len(intervalSplit) == 2:
            interval_value_1 = self.to_float(intervalSplit[0])
            interval_value_2 = self.to_float(intervalSplit[1])

            if interval_value_1 is None or interval_value_2 is None:
                return False, "An error occurred while updating your interval setting.\nPlease make sure you only use numbers.\nUse !help at any time to see all commands."
           
            interval_format_1, interval_format_2 = round(interval_value_1, 2), round(interval_value_2, 2)
         
            if interval_format_1 > interval_format_2:
                return False, "An error occurred while updating your interval setting.\Please make sure your first value is less then your second value.\nUse !help at any time to see all commands."

            if interval_format_1 < 60 or interval_format_2 < 60:
                return False, "An error occurred while updating your interval setting.\Please make sure your interval is in the range '60-3600'.\nUse !help at any time to see all commands."

            if interval_format_2 > 3600:
                return False, "An error occurred while updating your interval setting.\Please make sure your interval is in the range '60-3600'.\nUse !help at any time to see all commands."

            final_value = [interval_format_1, interval_format_2]
            text_value = f"{interval_format_1}-{interval_format_2}"
        
        # -- Static
        else:
            interval_value = self.to_float(interval)

            if interval_value is None:
                return False, "An error occurred while updating your interval setting.\nPlease make sure you only use numbers.\nUse !help at any time to see all commands."

            if interval_value > 3600 or interval_value < 0:
                return False, "An error occurred while updating your interval setting.\nPlease make sure your interval is in the range '0-3600'.\nUse !help at any time to see all commands."

            final_value = [round(interval_value, 2)]
            text_value = round(interval_value, 2)
        
        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "interval": final_value
        }

        await self.json_queue.put(payload)

        return True, f"Your interval has been updated to '{text_value}' seconds\nYou can change this at any time by sending the same command.\nUse !help at any time to see all commands."

    # -------------
    # -- Skip posts
    # A static number of posts the bot will skip, between 0 and 50 posts
    # A ranged interval of posts the bot will skip, between 0 and 50 posts
    async def skip_posts(self, user_did: str, interval: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and mormalisation
        if interval is None:
            return await self.remove_setting(user_did, "skip", account_did)
    
        # -- Check if the interval is a range or static value
        intervalSplit = interval.split("-")

        # -- Range
        if len(intervalSplit) == 2:
            interval_value_1 = self.to_float(intervalSplit[0])
            interval_value_2 = self.to_float(intervalSplit[1])

            if interval_value_1 is None or interval_value_2 is None:
                return False, "An error occurred while updating your interval setting.\nPlease make sure you only use numbers.\nUse !help at any time to see all commands."
           
            interval_format_1, interval_format_2 = int(interval_value_1), int(interval_value_2)
         
            if interval_format_1 > interval_format_2:
                return False, "An error occurred while updating your interval setting.\nPlease make sure your first value is less then your second value.\nUse !help at any time to see all commands."

            if interval_format_1 < 0 or interval_format_2 < 0:
                return False, "An error occurred while updating your interval setting.\nPlease make sure your interval is in the range '0-50'.\nUse !help at any time to see all commands."

            if interval_format_2 > 50:
                return False, "An error occurred while updating your interval setting.\nPlease make sure your interval is in the range '0-50'.\nUse !help at any time to see all commands."

            final_value = [interval_format_1, interval_format_2]
            text_value = f"{interval_format_1}-{interval_format_2}"
        
        # -- Static
        else:
            interval_value = self.to_float(interval)

            if interval_value is None:
                return False, "An error occurred while updating your interval setting.\nPlease make sure you only use numbers.\nUse !help at any time to see all commands."

            if interval_value > 50 or interval_value < 0:
                return False, "An error occurred while updating your interval setting.\nPlease make sure your interval is in the range '0-50'.\nUse !help at any time to see all commands."

            final_value = [int(interval_value)]
            text_value = int(interval_value)
        
        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "skip": final_value
        }

        await self.json_queue.put(payload)

        return True, f"Your interval has been updated to '{text_value}' posts\nYou can change this at any time by sending the same command.\nUse !help at any time to see all commands."
        
    # -------------
    # -- Delete
    # Delete all the users' settings
    async def delete_settings(self, user_did: str, account_did: str) -> tuple[bool, str]:
        # -- Add to queue
        payload = {
            "type": "delete",
            "user_did": user_did,
            "account_did": account_did
        }

        await self.json_queue.put(payload)

        return True, "Your settings have been deleted.\nYour can confirm this by using '!settings'.\nUse !help at any time to see all commands."

    # -------------
    # -- Settings
    # View a users' settings
    async def view_settings(self, user_did: str, account_did: str) -> tuple[bool, str]:
        # -- Settings helper
        def format_value(value):
            if isinstance(value, list):
                return f"{value[0]}-{value[1]}" if len(value) == 2 else value[0]
            return value

        # -- Get settings
        user_settings = self.user_data.get(account_did, {}).get(user_did, {})
      
        if not user_settings:
            return False, "You have no settings configured with the bot.\nUse !help to see options for settings!"
      
        format_settings = "\n".join(
            f"{key.capitalize()}: {format_value(value)}"
            for key, value in user_settings.items()
        )
        return True, f"Your settings can be seen below!\n{format_settings}"

    # -------------
    # -- Sync
    # Sync a users' settings between bots
    async def sync_settings(self, user_did: str, handle: str, bots: dict, account_did: str, other_dids: list) -> tuple[bool, str]:
        # -- Get the bot to sync with
        sync_did = None

        for did, bot in bots.items():
            if f"@{bot['handle']}" == handle:
                sync_did = did
                break
        
        # -- Validation
        if sync_did is None or sync_did not in bots:
            return False, "An error occurred while syncing your settings.\nPlease make sure you entered a valid bot handle.\nUse !help at any time to see all commands."

        # -- Get the users' settings on the sync bot
        sync_settings = self.user_data.get(sync_did, {}).get(user_did, {})

        # -- Sync the settings to the other bot
        if sync_did == account_did:
            for other_did in other_dids:
                payload = {
                    "type": "update",
                    "account_did": other_did,
                    "user_did": user_did,
                    **sync_settings
                }
                asyncio.create_task(self.json_queue.put(payload))

                return True, f"Other bots have been synced with your settings from {bots[account_did]['handle']}!\nUse !settings on your other bots to view your synced settings.\nUse !help at any time to see all commands."
     
        # -- Sync the settings to this bot
        elif sync_did != account_did:
            payload = {
                "type": "update",
                "account_did": account_did,
                "user_did": user_did,
                **sync_settings
            }
            asyncio.create_task(self.json_queue.put(payload))

            return True, f"Your settings have been synced with {bots[sync_did]['handle']}!\nUse !settings to view your synced settings.\nUse !help at any time to see all commands."
        else:
            return False, "An error occurred while syncing your settings.\nPlease make sure you entered a valid bot handle.\nUse !help at any time to see all commands."

    # -------------
    # -- Help
    # Send a help message for the bot
    async def help(self) -> tuple[bool, str, dict]:
        # -- Format help
        text = "Check out the README file for a full list of commands and features."
        link_text = "README file"
        uri = "https://github.com/Pikachannel/reply-bots/blob/main/README.md"
        byte_start = text.encode("utf-8").find(link_text.encode("utf-8"))
        byte_end = byte_start + len(link_text.encode("utf-8"))

        # -- Create the clickable link
        facet = {
            "index": {
                "byteStart": byte_start,
                "byteEnd": byte_end
            },
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#link",
                    "uri": uri
                }
            ]
        }

        return True, text, facet
