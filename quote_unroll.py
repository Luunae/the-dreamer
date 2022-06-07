import discord
from discord.ext import commands
from utilities import url_is_valid, replace_text_with_quoted_text, get_emojis

UTC_OFFSET = -7 * 3600  # Goddesses I fucking hate this.


def compose_quote(message: discord.Message):
    message = replace_text_with_quoted_text(message)
    # Use the datetime library to convert message.created_at to a integer timestamp in UTC-7.
    created_timestamp = int(message.created_at.timestamp()) + UTC_OFFSET
    quote: str = f"__@{message.author}__ in **#{message.channel}** at <t:{created_timestamp}>:\n"
    quote += message.content
    if message.edited_at:
        edited_timestamp = int(message.edited_at.timestamp()) + UTC_OFFSET
        quote += f"\n\nEdited at <t:{edited_timestamp}>"
    return quote


class QuoteUnroll(commands.Cog):
    def __init__(self, dreamer):
        self.dreamer = dreamer

    # Defines a function that checks if the string passed is a valid discord message URL.
    # The function takes a message and a guild ID as arguments and either returns False or a message object.
    async def get_message_from_url(self, link: str):
        # Split the link on slashes.
        split_link = link.split("/")
        # Get server ID, channel ID, and message ID from the link, and store them as integers.
        server_id = int(split_link[4])
        channel_id = int(split_link[5])
        message_id = int(split_link[6])

        # Use the bot to get the guild object.
        guild: discord.Guild = self.dreamer.get_guild(server_id)
        # Use the bot to get the channel object.
        channel: discord.GuildChannel = guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return False
        # Get the message object from the channel.
        message: discord.Message = await channel.fetch_message(message_id)
        try:
            message_content: str = message.content
        except discord.NotFound:
            return False
        except discord.Forbidden:
            return False
        except discord.HTTPException:
            return False
        return message

    @commands.Cog.listener()
    async def on_message(self, message):
        # If the message is from this bot, ignore it.

        if message.author.id == self.dreamer.user.id:
            return

        # If the message is from a user, and the message starts with the prefix,
        # then run the function.
        if "http" in message.content:
            url = "http" + message.content.split("http")[1].split()[0]
            if url_is_valid(url):
                if ("discord" not in url) and ("channels" not in url):
                    return
                message_from_url = await self.get_message_from_url(
                    "http"
                    + message.clean_content.split("http")[1].split()[0]
                )
                # If message_from_url is from a different guild than message, ignore it.
                if message_from_url.guild != message.guild:
                    return
                # Check if the sender of the original message is in the channel the message_from_url is in.
                # If they are not in the same channel, ignore the message.
                if (
                    message.author
                    not in message_from_url.channel.members
                ):
                    return
                if message_from_url:
                    quote = compose_quote(message_from_url)
                    if len(message_from_url.attachments) > 1:
                        attachments_to_send = []
                        # For each attachment in message_from_url, convert it to a file then add that file to
                        # attachments_to_send.
                        for attachment in message_from_url.attachments:
                            attachments_to_send.append(
                                await attachment.to_file()
                            )
                        await message.channel.send(
                            quote, files=attachments_to_send
                        )
                    elif len(message_from_url.attachments) == 1:
                        # Convert the only attachment from message_from_url to a file, then add that file to
                        # attachment_to_send.
                        attachment_to_send = await message_from_url.attachments[
                            0
                        ].to_file()  # This was done by black. Weird flex but okay.
                        await message.channel.send(
                            quote, file=attachment_to_send
                        )
                    else:
                        await message.channel.send(content=quote)
