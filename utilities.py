import discord
import validators
from typing import Optional, Union
from discord.ext import commands
from bot import get_bot


def isnt_me(message: discord.Message):
    dreamer = get_bot()
    if message.author.id != dreamer.user.id:
        return False
    else:
        return True


def get_data_channel(guild: discord.Guild) -> discord.TextChannel:
    return discord.utils.get(guild.channels, name="bot-data")


@commands.bot_has_permissions(manage_messages=True)
async def clear_data_channel(channel: discord.TextChannel):
    # I can't really prevent others from using this channel, but I can at least clear out their shit.
    try:
        await channel.purge(limit=100, check=isnt_me)
    except discord.Forbidden:
        pass


async def upsert_shitty_db(
    source: Union[discord.User, discord.TextChannel], data: tuple
):
    shitty_db = get_shitty_db(source)
    if shitty_db is None:
        # Create a new shitty user db.
        shitty_db = [data]
    elif data[0] in [x[0] for x in shitty_db]:
        # Update the shitty user db.
        shitty_db = [x for x in shitty_db if x[0] != data[0]]
        shitty_db.append(data)
    else:
        # Append to the shitty user db.
        shitty_db.append(data)
    # Convert the shitty user db to a string and send it to the user in a DM.
    message = convert_shitty_db_to_message(shitty_db)
    if isinstance(source, discord.User):
        await source.dm_channel.send(message)
    elif isinstance(source, discord.TextChannel):
        await source.send(message)
    else:
        return


def get_shitty_db(
    source: Union[discord.User, discord.TextChannel]
) -> Optional[list[tuple]]:
    own_content = None
    if isinstance(source, discord.User):
        if source.dm_channel is None:
            return
        message_history = source.dm_channel.history(
            oldest_first=True
        ).flatten()
        for message in message_history:
            if message.author != source:
                own_content = message
                break
    elif isinstance(source, discord.TextChannel):
        message_history = source.history(oldest_first=True).flatten()
        for message in message_history:
            if message.author != source.guild.me:
                own_content = message
                break
    else:
        return
    if own_content is None:
        return
    own_content = own_content.content.split("\n")
    shitty_database: list[tuple] = []
    for line in own_content:
        shitty_database.append(tuple(line.split(" ", 1)))
    return shitty_database


def convert_shitty_db_to_message(shitty_db: list[tuple]) -> str:
    message = ""
    for line in shitty_db:
        message += f"{line}" + "\n"
    return message


def url_is_valid(link: str):
    return validators.url(link)


def replace_text_with_quoted_text(message: discord.Message):
    message.content = "> " + message.content
    message.content = message.content.replace("\n", "\n> ")
    return message


async def mark_command_invalid(ctx):
    try:
        # Reminder to actually use unicode emoji rather than a text representation.
        await ctx.message.add_reaction("❌")
    except discord.HTTPException as e:
        # print(f"HTTPException {e}")
        # # print the information about the error.
        # print(f"HTTPException: {ctx.message.content}")
        pass
    except discord.InvalidArgument:
        pass
