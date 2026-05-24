# -------- Imports --------
import requests
import time

# -------- Filters Class --------
class Filters:
    def __init__(self):
        self.cache = {} # user_did: (labels, timestamp)
        self.session = requests.Session()

        # -- Load keyword list
        with open("data/blocklist.txt", "r") as f:
            self.keyword_list = {line.strip().lower() for line in f}

    # -- Flag keywords
    def keywords(self, message):
        text = message.get("commit", {}).get("record", {}).get("text", "").lower()
        return any(keyword in text for keyword in self.keyword_list)

    # -- Flag links
    def links(self, message):
        embed = message.get("commit", {}).get("record", {}).get("embed", {})
        facets = message.get("commit", {}).get("record", {}).get("facets", [])

        # -- Check for links
        has_link = any(
            feature.get("$type") == "app.bsky.richtext.facet#link"
            for facet in facets
            for feature in facet.get("features", [])
)
        return embed.get("$type") == "app.bsky.embed.external" or has_link

    # -- Flag accounts with Bsky labels
    def account_flags(self, user_did):

        # -- Check for cached flags
        if user_did in self.cache:
            flagged, timestamp = self.cache[user_did]
            if time.time() - timestamp < 3600:
                return flagged

        # -- Check Bsky API for labels
        url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile"

        response = self.session.get(url, params={"actor": user_did}, timeout=5)

        if response.status_code != 200:
            return False

        data = response.json()
        labels = data.get("labels", [])

        flagged = len(labels) > 0  

        self.cache[user_did] = (flagged, time.time())

        return flagged
    
    # -- Flag posts with Bsky labels
    def post_flags(self, message, post_uri):
        # -- Check message for self labels
        post_labels = message.get("commit", {}).get("record", {}).get("labels", {}).get("$type", "")
        if post_labels == "com.atproto.label.defs#selfLabels":
            return True

        # -- Check Bsky API for labels
        url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts"

        response = self.session.get(url, params={"uris": post_uri}, timeout=5)

        if response.status_code != 200:
            return False

        data = response.json()

        posts = data.get("posts", [])
        if not posts:
            return False

        post = posts[0]
        labels = post.get("labels", [])

        flagged = len(labels) > 0 

        return flagged