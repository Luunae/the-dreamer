import re
import discord
import validators
from typing import Optional, Union
from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer = dreamer

    @commands.command(name="teleport", aliases=["tp"])
    async def teleport(self, ctx, arg: str):
        """
        Use this command to nudge discussion to a different channel.
        `!tp [channel]`
        (You must use a channel hyperlink of a channel that exists in the server the command is used in.)
        """
        try:
            portal_exit_channel = self.dreamer.get_channel(
                int(re.sub("\D", "", arg))
            )
            if portal_exit_channel == ctx.channel:
                await mark_command_invalid(ctx)
                return
        except ValueError:
            await mark_command_invalid(ctx)
            return
        portal_entrance = await ctx.send(teleport_to(ctx, arg))
        portal_exit = await portal_exit_channel.send(teleport_from(ctx))
        await portal_entrance.edit(
            content=portal_entrance.content + "\n" + portal_exit.jump_url
        )
        await portal_exit.edit(
            content=portal_exit.content + "\n" + portal_entrance.jump_url
        )


def teleport_from(ctx):
    message = (
        "Teleport from: "
        + ctx.message.channel.mention
        + ", cast by "
        + str(ctx.message.author)
        + ":"
    )
    return message


def teleport_to(ctx, arg):
    message = (
        "Teleport to: " + arg + ", cast by " + str(ctx.message.author) + ":"
    )
    return message


class Teleport(commands.Cog, name="Banana"):
    def __init__(self, dreamer):
        self.dreamer = dreamer


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


def url_is_valid(link: str):
    return validators.url(link)


def replace_text_with_quoted_text(message: discord.Message):
    if len(message.content) > 0:
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
