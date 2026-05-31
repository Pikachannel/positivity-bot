# Bluesky Reply Bots

## Overview
This repository contains all the code for:
- Whimsy Miku Bot (whimsy.pikachannel.xyz)
- Evil Teto Bot (evil.pikachannel.xyz)
--- 

## The Bots!
Whimsy Miku responds to your posts with positive messages!

Evil Teto responds to your posts with funny mean messages!

### Current Features
1. **Randomly chosen preset messages**, including:
   - English messages.
   - Messages that include the user's name.
2. **Content Filtering System**, including:
   - A post filter system
   - Allowing users to delete replies under their posts by replying with "delete"
3. **Custom nicknames**: Users can set a custom nickname instead of using their Bluesky display name.
4. **Post chance**: Users can change the chance of a reply being made under their post.
5. **Post interval**: Users can change the amount of time in between replies being able to be made under their posts. All replies are subject to a minimum 60 second cooldown.
6. **Skip posts**: Users can change the amount of posts in between replies being able to be made under their posts.

### How to use
1. Follow the bot on Bluesky.
   - If you unfollow or block the bot, it may take up to 5 minutes for this to register and for replies to stop.

### Content Filtering System

#### Filter system
The system skips replies when any of the following conditions are met:

**Post content checks:**
1. Detects whether a post contains any predefined keywords  
2. Detects whether a post contains a link or embed

**Account-level checks:**
1. Checks if the poster's account has been flagged by Bluesky moderation

**Post-level checks:**
1. Detects Bluesky post labels, including:
   - self-applied labels
   - Bluesky moderation labels

#### Deleting posts
1. Find a reply made under one of your posts.
2. Reply to it with "delete" and it will be removed instantly.

### Settings
You can configure settings with the bots! You do this by sending the appropriate command in the bots dms, these can be seen below. 
To view all your settings:
1. Send a direct message to the bot in the format:
   - `!settings`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes.

#### Syncing Settings
1. Send a direct message to the bot in the format:
   - **Sync the current bot’s settings with another bot:** `!sync <@other_bot_handle>`
   - **Sync all other bots’ settings with the current bot:** `!sync <@current_bot_handle>`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes.

##### Custom nickname
1. Send a direct message to the bot in the format:  
   - **Setting Nickname:** `!nickname <nickname>` (your nickname can be max 20 characters)
   - **Resetting Nickname:** `!nickname`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes.

#### Post chance 
1. Send a direct message to the bot in the format:
  - **Setting Chance:** `!chance <chance>` (must be a number between 1 and 100)
  - **Resetting Chance:** `!chance`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes.

#### Post interval
1. Send a direct message to the bot in the format:
  - **Setting Static Interval:** `!interval <interval>` (must be a number between 60 and 3600)
  - **Setting Variable Interval:** `!interval <lower_bound-upper_bound>` (both numbers must be between 60 and 3600)
  - **Resetting Interval:** `!interval`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes

#### Skip posts
1. Send a direct message to the bot in the format:
   - **Setting Static Interval:** `!skip <intervaL>` (must be a integer between 0 and 50)
   - **Setting Variable Interval:** `!skip <lower_bound-upper_bound>` (both integers must be between 0 and 50)
   - **Resetting Interval:** `!skip`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes

## Privacy Policy

### Data Collection, Usage, Retention, and Security
The bots collect and make use of the following data:

**Follower Posts:**  
  - The content and metadata of posts from accounts following the bot.  
  - Post information is **never permanently retained** and is only stored temporarily in the bot's cache.

**User Metadata:**  
  - Publicly accessible information such as usernames and profile details.  
  - The only information stored is the user DID (a form of user ID in Bluesky).

**User Settings:**  
  - Settings configured by the user, such as nicknames.
  - This information is stored **against the user's DID**.

**Security and Usage:**  
- None of the data is shared with third parties.  
- None of the data is used by an AI model.

### Data Deletion
If you would like your data deleted from the bot, there are two options:

**Automatic Deletion:**  
1. Send a direct message to the bot in the format:
   - `!delete`
2. Wait for the bot to respond **before** sending a new message.
   - Responses may take up to 5 minutes.

**Manual Deletion:**  
  1. Contact Pikachannel via:  
     - Bluesky: [pikachannel.xyz](https://bsky.app/profile/pikachannel.xyz)  
     - Email: pikachannel.dev@gmail.com  
  2. Await confirmation that your data has been deleted from the bot's storage.

## License
This repository is open source and released using the MIT License.

See [LICENSE](https://github.com/Pikachannel/bluesky-bots/blob/main/LICENSE) for further details.
