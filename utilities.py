from __future__ import unicode_literals
import os
import re
import logging
from datetime import datetime
import discord
import validators
import urllib.request
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
import youtube_dl


class Utilities(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer: commands.Bot = dreamer

    @app_commands.command(name="teleport", description="Teleport to another channel")
    @app_commands.describe(destination_channel="The channel to teleport to")
    async def teleport(
        self, interaction: discord.Interaction, destination_channel: discord.TextChannel
    ):
        source_channel = interaction.channel
        user = interaction.user

        # Send initial message in the source channel
        source_message = await source_channel.send(
            f"Teleporting to {destination_channel.mention} on behalf of {user.mention}."
        )

        # Send message in the destination channel
        destination_message = await destination_channel.send(
            f"Teleport from {source_channel.mention} on behalf of {user.mention}, at {source_message.jump_url}."
        )

        # Edit the initial message in the source channel
        await source_message.edit(
            content=f"Teleport to {destination_channel.mention} on behalf of {user.mention}, exit: {destination_message.jump_url}."
        )
        await interaction.response.send_message(
            "Teleportation succeeded.", ephemeral=True
        )

    @app_commands.command(
        name="ytdl", description="use the ytdl library on a provided link"
    )
    @app_commands.describe(link="The link to download")
    async def ytdl(self, interaction: discord.Interaction, link: str):
        if not url_is_valid(link):
            await interaction.response.send_message("Invalid link.", ephemeral=True)
            return

        # Download the video
        ydl_opts = {
            "outtmpl": "video.mp4",
            "format": "best[filesize<25M]",  # Discord limit. Can probably do shenanigans for boosted guilds.
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except Exception as e:
            await interaction.response.send_message(
                "Error downloading video.", ephemeral=True
            )
            return

        # Send the video
        await interaction.response.send_message(
            content=f"Interaction complete.",
            file=discord.File("video.mp4"),
            ephemeral=True,
        )
        # Delete the video
        os.remove("video.mp4")


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


def get_emoji_link(ctx: Context) -> str:
    emoji_to_get = get_emojis(ctx.message.content)[0]
    emoji_id = emoji_to_get.split(":")[-1].split(">")[0]
    if emoji_to_get[1] == "a":
        return "https://cdn.discordapp.com/emojis/" + emoji_id + ".gif?quality=lossless"
    else:
        return "https://cdn.discordapp.com/emojis/" + emoji_id + ".png?quality=lossless"
