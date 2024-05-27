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
