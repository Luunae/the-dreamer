import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import requests
import ssl

load_dotenv(verbose=True)
TEST_SERVER_ID = int(os.getenv("TEST_SERVER_ID"))
DEVELOPER_USER_ID = int(os.getenv("DEVELOPER_USER_ID"))

class Idleon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fetch_idleonefficiency")
    @app_commands.describe(username="Username of a public idleonefficiency profile.")
    @app_commands.guilds(TEST_SERVER_ID)
    async def fetch_idleonefficiency(self, interaction: discord.Interaction, username: str):
        # replace spaces with underscores
        username = username.replace(" ", "_")
        try:
            url = f"https://cdn2.idleonefficiency.com/profiles/{username}.json"
            headers = {"Content-Type": "text/json", "method": "GET"}
            response = requests.get(url, headers=headers)
            print("just did requests.get")

            if response.status_code == 403:
                print("403")
                await interaction.response.send_message("Error 403: Forbidden.")
                return
            print("saving response.json as account_data")
            account_data = response.json()
            print("saved response.json as account_data")
            if not account_data:
                print("no data found")
                await interaction.response.send_message("No data found.")
                return
            print("writing to file")
            print(type(account_data), len(account_data))
            with open(f"./saves/{username}.json", "w") as f:
                json.dump(account_data, f)
            print("written to file")
            await interaction.response.send_message(f"Data saved to saves/{username}.json")
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"Error retrieving data from IE:\n{e.request.url}\n{e}")
            return
