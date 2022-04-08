# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv('DISCORD_TOKEN'))

description = (
    """A simple bot that pastes the contents of the linked message to the channel."""
)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


# Up next is a function that takes a link to a message and sends the contents of the message. The contents that
# should be sent are the message contents and the message author, and the message timestamp. The message timestamp
# uses the format <t:TIMESTAMP> where TIMESTAMP is the message timestamp in epoch seconds. The function also posts
# the original channel the message was sent in.


@bot.command()
async def message_quote(ctx, link):
    """
    Sends the contents of a message to the channel.
    """
    # The link is split into the message ID and the channel ID.
    link = link.split("/")
    message_id = link[-1]
    channel_id = link[-2]
    # The message is retrieved from the message ID and channel ID.
    message = await bot.get_channel(int(channel_id)).fetch_message(int(message_id))
    # The message contents are retrieved from the message.
    message_contents = message.content
    # Turn message_contents into a quote, by adding a right angle bracket and a space after each newline.
    message_contents = message_contents.replace("\n", "\n> ")
    # The message author is retrieved from the message.
    message_author = message.author
    # The message timestamp is retrieved from the message.
    message_timestamp = message.created_at
    # The message timestamp is converted to epoch seconds.
    message_timestamp = message_timestamp.timestamp()
    # The message timestamp is converted to a string.
    message_timestamp = str(message_timestamp)
    # The message timestamp is formatted as <t:TIMESTAMP> where TIMESTAMP is the message timestamp in epoch seconds.
    message_timestamp = "<t:" + message_timestamp + ">"
    # message_to_send is the message that will be sent to the channel.
    # The first line of the contents of message_to_send is:
    # @<AUTHOR> in #<CHANNEL>, at message_timestamp:
    # Where @<AUTHOR> is the username of the message author, #<CHANNEL> is the name of the channel the message was
    # sent in, and message_timestamp is the discord-formatted message timestamp.
    message_to_send = "@" + message_author.name + " in #" + message.channel.name + ", at " + message_timestamp + ":\n"
    # The message_to_send is then appended with the contents of the message.
    message_to_send = message_to_send + message_contents
    # The message_to_send is then sent to the channel the message was sent in.
    await ctx.send(message_to_send)


