import re
import os

from dotenv import load_dotenv

import discord
from discord import app_commands

import users
import steam_api
import gener8rs_api


# Settings
REFER_TO_OTHER_USERS_BY_MENTION = False

# Initialize
load_dotenv()
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


# Commands
@tree.command(
    name="hello",
    description="Social convention of acknowledgement",
    guild=discord.Object(id=GUILD_ID)
)
async def hello_command(interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")


@tree.command(
    name="github",
    description="Give link to my GitHub repository!",
    guild=discord.Object(id=GUILD_ID)
)
async def github_command(interaction):
    await interaction.response.send_message("Here ya go!\nhttps://github.com/sofusbrandt/BoistressBot")


@tree.command(
    name="playtime",
    description="Give the playtime for yourself or the given player",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(playername="Discord username or @mention of the player. Leave blank to use yourself.")
async def playtime(interaction, playername: str = None):
    if playername is None:
        playername = interaction.user.name

    if re.compile("<@[0-9]+>").match(playername):  # mention is used instead of username
        member = await interaction.guild.fetch_member(playername[2:-1])
        playername = member.name

    steam_id = users.steam_id_from_discord_username(playername)

    if steam_id is None:
        await interaction.response.send_message(f"User {playername} not found")
        return

    hours = int(steam_api.get_playtime(steam_id))

    player_reference = f"<@{playername}>" if REFER_TO_OTHER_USERS_BY_MENTION else playername
    await interaction.response.send_message(f"Player {player_reference} has played Team Fortress 2 for {hours} hours!")


@tree.command(
    name="loadouts",
    description="Generate random loadouts for random classes",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(count="Amount of loadouts to generate. Leave blank for 6 named loadouts.")
async def loadouts(interaction, count: int = None):
    persons = ['Sofus', 'Adrian', 'Gustav', 'Philip', 'Thorvald', 'Mathias']
    message = "## Random loadouts\n"
    use_names = False

    if count is None:
        use_names = True
        count = 6

    for i in range(0, count):
        loadout = gener8rs_api.random_loadout()  # No idea why I have to name the file here

        _class = loadout['_sChosenClass']
        primary = loadout['_sPrimary']
        secondary = loadout['_sSecondary']
        melee = loadout['_sMelee']
        building = loadout['_sBuilding']

        if use_names:
            message += f"__{persons[i]}__: **{_class}**\n"
        else:
            message += f"{i + 1}: **{_class}**\n"
        message += f"{primary}\n"
        message += f"{secondary}\n"
        message += f"{melee}\n"
        if building is not None:
            message += f"{building}\n"
        message += "\n"

    await interaction.response.send_message(message)


# Events
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"{client.user} has connected to Discord!")


# Run
# Taken from line 28-42 of https://replit.com/@replit/Python-Discord-Bot#main.py
try:
    token = os.getenv('DISCORD_TOKEN') or ''
    if token == '':
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/"
            + "in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
