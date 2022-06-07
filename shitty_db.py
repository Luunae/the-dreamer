import discord
from typing import Optional, Union


def get_data_channel(guild: discord.Guild) -> discord.TextChannel:
    return discord.utils.get(guild.channels, name="bot-data")


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
