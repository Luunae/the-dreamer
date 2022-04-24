from discord.ext import commands
from utilities import mark_command_invalid
import re


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


class Teleport(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer = dreamer

    @commands.command(name="teleport", aliases=["tp"])
    async def teleport(self, ctx, arg: str):
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
