# -------- Imports --------
import random
from atproto import Client, client_utils
import time
from typing import Any

# -------- Post Manager Class --------
class PostManager:
    def __init__(self, client: Client, user_data: dict, account_did: str, messages: dict, filters: Any) -> None:
        self.client = client
        self.user_data = user_data
        self.account_did = account_did
        self.messages = messages

        self.post_times: dict[str, float] = {}
        self.post_numbers: dict[str, int] = {}

        self.filters = filters



    # -------------
    # -- Interval (time) check
    def interval_time_check(self, user_did: str) -> bool:
        intervals = self.user_data.get(user_did, {}).get("interval", [])

        now = time.time()
        next_allowed = self.post_times.get(user_did, 0)

        if now < next_allowed:
            remaining = next_allowed - now
            print(f"[Post] Skipping post for {user_did} ({remaining:.2f}s remaining)")
            return False

        if len(intervals) != 0:
            interval = intervals[0] if len(intervals) == 1 else random.uniform(intervals[0], intervals[1])
        else:
            interval = 0
        if interval < 60:
            interval = 60
        self.post_times[user_did] = now + interval
        return True

    # -------------
    # -- SKip post check
    def skip_posts_check(self, user_did: str) -> bool:
        intervals = self.user_data.get(user_did, {}).get("skip", [])
        if not intervals:
            return True

        # -- Setup posts counter
        if user_did not in self.post_numbers:
            skip = intervals[0] if len(intervals) == 1 else random.randint(intervals[0], intervals[1])
            self.post_numbers[user_did] = skip

        # -- Check if the post should be skipped
        if self.post_numbers[user_did] > 0:
            self.post_numbers[user_did] -= 1
            print(f"[Post] Skipping post for {user_did} ({self.post_numbers[user_did]} posts remaining)")
            return False

        # -- Reset counter
        skip = intervals[0] if len(intervals) == 1 else random.randint(intervals[0], intervals[1])
        self.post_numbers[user_did] = skip

        return True        

    # -------------
    # -- Chance check
    def chance_check(self, user_did: str) -> bool:
        post_chance = self.user_data.get(user_did, {}).get("chance", 100)
        if random.uniform(0, 100) > post_chance:
            print(f"[Post] Skipping post for {user_did} due to post chance ({post_chance}%)")
            return False
        return True

    # -------------
    # -- Filters check
    def filters_check(self, message: dict, user_did: str) -> bool:
        if self.filters.keywords(message):
            print(f"[Post] Skipping post for {user_did} due to keywords")
            return False

        if self.filters.links(message):
            print(f"[Post] Skipping post for {user_did} due to links")
            return False

        if self.filters.account_flags(user_did):
            print(f"[Post] Skipping post for {user_did} due to account flags")
            return False

        if self.filters.post_flags(message.get("commit", {}).get("record", {}).get("uri", "")):
            print(f"[Post] Skipping post for {user_did} due to post flags")
            return False

        return True

    # -------------
    # -- Get nickname
    def get_nickname(self, user_did: str) -> str:
        nickname = self.user_data.get(user_did, {}).get("nickname")

        if nickname:
            return nickname

        profile = self.client.get_profile(user_did)
        return (
            profile.display_name
            or profile.handle.split(".")[0]
        )

    # -------------
    # -- Make post
    async def make_post(self, message: dict, post_cid: str, post_uri: str, user_did: str, post_text: str, lang: str = "en") -> None:
        messages = self.messages[lang]

        # -- Check if the post can be made
        if not self.interval_time_check(user_did):
            return

        if not self.filters_check(message, user_did):
            return

        if not self.skip_posts_check(user_did):
            return

        if not self.chance_check(user_did):
            return



        # -- Buld the post
        nickname = self.get_nickname(user_did)

        random_message = random.choice(messages)
        formatted_message = random_message.format(display_name=nickname)

        builder = client_utils.TextBuilder()
        builder.text(formatted_message)

        # -- Make the post
        post = self.client.send_post(
            builder,
            reply_to={
                "parent": {"cid": post_cid, "uri": post_uri},
                "root": {"cid": post_cid, "uri": post_uri}
            }
        )

        print(f"[Post] Post made ({post.uri})")

    # -------------
    # -- First reply post
    async def first_reply(self, post_cid: str, post_uri: str, user_did: str, lang: str = "en"):
        # -- Format reply
        builder = client_utils.TextBuilder()
        
        builder.text("Thank you for following!\nSee the bots ")
        builder.link(
            "github",
            "https://github.com/Pikachannel/positivity-bot/blob/main/README.md"
        )
        builder.text(" for a full list of settings you can configure with me.")

        # -- Make the post
        post = self.client.send_post(
            builder,
            reply_to={
                "parent": {"cid": post_cid, "uri": post_uri},
                "root": {"cid": post_cid, "uri": post_uri}
            }
        )

        print(f"[Post] Post made ({post.uri})")
        
    # -------------
    # -- Delete post
    async def delete_post(self, message: dict, user_did: str) -> None:
        # -- Get all post information 
        commit = message.get("commit", {})
        record = commit.get("record", {})
        reply = record.get("reply", {})
        parent = reply.get("parent", {})
        root = reply.get("root", {})

        # -- Get the orignal posts key and psoters did and the replies
        rootDID, rootKEY = root.get("uri", "").split('at://')[1].split('/app.bsky.feed.post/')
        parentDID, parentKEY = parent.get("uri", "").split('at://')[1].split('/app.bsky.feed.post/')

        # -- Check if the original post belongs to the user and the reply belongs to the bot
        if user_did == rootDID and self.account_did == parentDID:
            if record.get("text", "").lower() == "delete":
                self.client.delete_post(parent.get("uri", "")) # Delete the post
                print(f"[Delete] Post deleted from {user_did}")
