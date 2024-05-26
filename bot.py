# bot.py
import os
import discord
from discord import app_commands

from dotenv import load_dotenv

# Load .env
load_dotenv()

# Load Guild ID
GUILD_ID = os.getenv("GUILD_ID")

# Load intents
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)

# Create command tree
tree = app_commands.CommandTree(client)


# Commands
@tree.command(
    name="hello",
    description="Social convention of acknowledgement",
    guild=discord.Object(id=GUILD_ID)  # Remove this eventually. It just has to sit for a while when you do.
)
async def hello_command(interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")


@tree.command(
    name="github",
    description="Gives link to my GitHub repository!",
    guild=discord.Object(id=GUILD_ID)
)
async def github_command(interaction):
    await interaction.response.send_message("Here ya go!\nhttps://github.com/sofusbrandt/BoistressBot")


# Events
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f'{client.user} has connected to Discord!')


# Run
# Taken from line 28-42 of https://replit.com/@replit/Python-Discord-Bot#main.py
try:
    token = os.getenv("DISCORD_TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
