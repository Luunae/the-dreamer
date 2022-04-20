import discord
import validators


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
