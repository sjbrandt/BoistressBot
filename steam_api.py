import os
import requests

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('STEAM_API_KEY')


def get_playtime(steam_id: str):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    args = f"?key={KEY}&steamid={steam_id}&format=json&include_appinfo=true&include_played_free_games=true"
    response = requests.get(url + args)
    data = response.json()

    games = data['response']['games']
    for game in games:
        if game['appid'] == 440:
            playtime = game['playtime_forever'] / 60
            return playtime

    return None


def generate_stats_list(steam_id: str):
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={KEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    data = response.json()

    message = ""
    for stat in data['playerstats']['stats']:
        message += f"{stat['name']}\n"

    with open('stats_list.txt', 'w') as f:
        f.write(message)
