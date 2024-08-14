# The Dreamer is currently a simple utility bot.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Its features are:
- A `teleport` slash command:  
Redirect to a different channel.
- ~~A `!unshort` (alias: `!us`) function:~~ (TODO: Reimplement)    
Reply to a message with this command to repost an unshortened YouTube link.
- ~~A `!reportemojilimit` (alias: `!rem`) function:~~ (TODO: Reimplement)
Sends a message declaring the current emoji limit for the server, and the number of current emojis in the server.  
If the server is close to the emoji limit, it will state so.
- ~~A `!getemojilink` (alias: `!gel`) function:~~ (TODO: Reimplement)  
Sends a message containing a clickable link to the emoji provided.
- ~~A `!emojisteal` (aliases: `!esteal`, `!es`) function:~~ (TODO: Reimplement)    
Usage: `!emojisteal [emoji] desired_emoji_name`  
Will add a note in the audit log saying who added the emoji, using the `reason` field.

- ~~Quote Unrolling (No command, simply link a discord message in the same server):~~  (TODO: Reimplement)  
Sends a message quoting the message found at the link.
