import re
import discord
import validators
import urllib.request
from discord.ext import commands
from discord.ext.commands import Context


class Utilities(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer: commands.Bot = dreamer

    @commands.command(name="Teleport", aliases=["teleport", "tp"])
    async def teleport(self, ctx: Context, arg: str):
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

    @commands.command(name="Unshort", aliases=["unshort", "us"])
    async def unshorten(self, ctx: Context):
        """
        Converts a Youtube Shorts link to a standard Youtube link.
        A Youtube Shorts link looks like: https://youtube.com/shorts/[ID]
        where [ID] is a Youtube Video ID, such as N2EsSCxfjl0
        A standard Youtube link looks like https://www.youtube.com/watch?v=[ID]
        """
        message_to_act_on = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )
        if not url_is_valid(message_to_act_on.content):
            await mark_command_invalid(ctx)
            return
        if "youtube.com/shorts/" in message_to_act_on.content:
            # Get everything in the link after the last slash.
            video_id = message_to_act_on.content.split("/")[-1]
            # If there is a question mark in the video id, remove it and everything after it.
            if "?" in video_id:
                video_id = video_id.split("?")[0]
            message_to_send = "https://www.youtube.com/watch?v=" + video_id

            await ctx.send(message_to_send)
        else:
            await mark_command_invalid(ctx)

    @commands.command(
        name="EmojiSteal", aliases=["emojisteal", "es", "esteal"]
    )
    async def emoji_steal(self, ctx: Context):
        """
        Steals an emoji.
        Usage: !esteal [emoji] [emoji_name]
        You must use a custom emoji.
        """
        if ctx.guild.emojis == ctx.guild.emoji_limit:
            await ctx.send("This server has reached the emoji limit.")
            await mark_command_invalid(ctx)
            return
        else:
            emoji_to_steal = get_emojis(ctx.message.content)[0]
            emoji_to_steal_id = emoji_to_steal.split(":")[-1].split(">")[0]
            if emoji_to_steal[1] == "a":
                emoji_to_steal_url = "https://cdn.discordapp.com/emojis/" + emoji_to_steal_id + ".gif?quality=lossless"
            else:
                emoji_to_steal_url = "https://cdn.discordapp.com/emojis/" + emoji_to_steal_id + ".png?quality=lossless"
            request = urllib.request.Request(url=emoji_to_steal_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'})
            with urllib.request.urlopen(request) as response:
                stolen_emoji = response.read()
            emoji_name = ctx.message.content.split(">")[-1].strip()
            reason = "Stolen By: " + ctx.author.name
            try:
                await ctx.guild.create_custom_emoji(name=emoji_name, image=stolen_emoji, reason=reason)
            except discord.Forbidden:
                await ctx.send(
                    "Missing manage_emojis permission. (Probably)\nIf the bot has this permission, poke Lucid for debugging."
                )
                await mark_command_invalid(ctx)
                return
            if ctx.guild.emojis[-1].animated:
                message_to_send = "<a:" + ctx.guild.emojis[-1].name + ":" + str(ctx.guild.emojis[-1].id) + ">"
            else:
                message_to_send = "<:" + ctx.guild.emojis[-1].name + ":" + str(ctx.guild.emojis[-1].id) + ">"
            await ctx.send(message_to_send)

    @commands.command(
        name="ReportEmojiLimit",
        aliases=["reportemojilimit", "EmojiLimit", "emojilimit", "rel"],
    )
    async def report_emoji_limit(self, ctx: commands.Context):
        """
        Reports the emoji limit of the server.
        """
        if ctx.guild:
            message_to_send = (
                "The emoji limit for this server is "
                + str(ctx.guild.emoji_limit)
                + ".\nThe current number of emojis is "
                + str(len(ctx.guild.emojis))
                + "."
            )
            if ctx.guild.emoji_limit - len(ctx.guild.emojis) < 5:
                message_to_send += (
                    "\n\nYou are approaching the emoji limit for this server.\n Emoji slots left: "
                    + str(ctx.guild.emoji_limit - len(ctx.guild.emojis))
                )
            await ctx.send(message_to_send)
        else:
            await mark_command_invalid(ctx)


def teleport_from(ctx: Context):
    message = (
        "Teleport from: "
        + ctx.message.channel.mention
        + ", cast by "
        + str(ctx.message.author)
        + ":"
    )
    return message


def teleport_to(ctx: Context, arg):
    message = (
        "Teleport to: " + arg + ", cast by " + str(ctx.message.author) + ":"
    )
    return message


class Teleport(commands.Cog, name="Banana"):
    def __init__(self, dreamer):
        self.dreamer = dreamer


def url_is_valid(link: str):
    return validators.url(link)


def replace_text_with_quoted_text(message: discord.Message):
    if len(message.content) > 0:
        message.content = "> " + message.content
        message.content = message.content.replace("\n", "\n> ")
    return message


async def mark_command_invalid(ctx: Context):
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


def get_emojis(string: str) -> list[str]:
    return re.findall(r"<a?:.*?:\d*?>", string)
