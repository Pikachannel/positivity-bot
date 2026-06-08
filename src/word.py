# -------- Imports --------
import asyncio
from datetime import datetime, timedelta
from wonderwords import RandomWord

# -------- Functions --------

# -- Post a random word --
async def post_random_word(client, blocked_words):
    # -- Get a random word
    r = RandomWord()
    word = None
    while word is None or word in blocked_words:
        word = r.word()
        print(word)

    # -- Make the post
    post = client.send_post(f"TETO WORD OF THE DAY: {word}")

# -- Post a random word every day at 3 PM --
async def word_of_the_day(client, blocked_words):
    # -- Check the time every hour (in case the bot is restarted)
    await post_random_word(client, blocked_words)

    while True:
        current_time = datetime.now()
        if current_time.hour == 15:
            await post_random_word(client, blocked_words)
        await asyncio.sleep(3600)