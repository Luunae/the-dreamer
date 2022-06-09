from pprint import pprint
import pickle
import discord
from discord.ext import commands
from discord.ext.commands import Context
from typing import Optional, Union
from utilities import mark_command_invalid


class ShittyDatabase(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer: commands.Bot = dreamer
        # Create a dictionary mapping guild IDs to each guild's database.
        # Guild_ID:[bot-data channel ID]
        # Get the data channel ID from get_data_channel(), by passing in the guild ID as the only parameter.
        self.guild_data_channels = {}

    @commands.Cog.listener(name="on_ready")
    async def post_ready_init(self):
        for guild in self.dreamer.guilds:
            maybe_data_channel = get_data_channel(guild)
            if maybe_data_channel is not None:
                self.guild_data_channels[guild.id] = maybe_data_channel
        pprint(self.guild_data_channels)

    @commands.command(name="ReportChannels", aliases=["reportchannels", "rc"])
    async def report_channels(self, ctx: Context):
        """
        Reports the channels in the server.
        """
        if ctx.guild:
            # Pretty Print (pprint) the list of guild channels containing the attribute name="bot-data".
            pprint(
                [
                    channel
                    for channel in ctx.guild.channels
                    if channel.name == "bot-data"
                ]
            )
        else:
            await mark_command_invalid(ctx)

    async def send_shitty_db(self, ctx: Context, data):
        """
        Sends the shitty database to the data channel.
        """
        if ctx.guild:
            if ctx.guild.id in self.guild_data_channels:
                data_channel = self.guild_data_channels[ctx.guild.id]
                await data_channel.send(file=data)
            else:  # The guild doesn't have a data channel. Something has gone wrong.
                await ctx.send(
                    "The guild doesn't have a data channel or something has gone wrong. (send_shitty_db)"
                )
        else:  # If the command was not sent in a guild, then it is a DM.
            await ctx.send(file=data)

    async def get_shitty_db(self, ctx: Context):
        # If the command was sent in a guild, then get the data channel from the guild.
        if ctx.guild:
            if ctx.guild.id in self.guild_data_channels:
                data_channel = self.guild_data_channels[ctx.guild.id]
                # Get the most recent message in the data channel from the bot.
                message_history = ctx.history(oldest_first=False).flatten()
                for message in message_history:
                    if message.author == self.dreamer.user:
                        # Return the message's attachment.
                        return message.attachments[0]
            else:
                await ctx.send(
                    "The guild doesn't have a data channel or something has gone wrong. (get_shitty_db)"
                )
        else:
            # The ctx.guild returned None, so it is a DM.
            pass


def get_data_channel(guild: discord.Guild) -> Optional[discord.TextChannel]:
    list_contains_bot_data = []
    for channel in guild.channels:
        if channel.name == "bot-data":
            list_contains_bot_data.append(channel)
    if len(list_contains_bot_data) == 1:
        return list_contains_bot_data[0]
