from discord.ext.commands import Bot

instance = None


def get_bot() -> Bot:
    return instance
