import json


def steam_id_from_discord_username(discord_username: str):
    users = load_users()
    for user in users:
        if user["discord_username"] == discord_username:
            return user["steam_id"]
    return None


def steam_id_from_discord_id(discord_id: str):
    users = load_users()
    for user in users:
        if user["discord_id"] == discord_id:
            return user["steam_id"]
    return None


def load_users():
    f = open('users.json')
    users = json.load(f)
    return users
