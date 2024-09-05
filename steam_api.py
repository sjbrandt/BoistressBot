import os
import requests

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('STEAM_API_KEY')


def get_playtime(steam_id: str | int):
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


def get_stat(steam_id: str | int, stat: str):
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={KEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    data = response.json()

    for stat_object in data['playerstats']['stats']:
        if stat_object['name'] == stat:
            return stat_object['value']

    return None


def generate_stats_list(steam_id: str | int):
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={KEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    data = response.json()

    message = ""
    for stat in data['playerstats']['stats']:
        message += f"{stat['name']}\n"

    with open('stats_list.txt', 'w') as f:
        f.write(message)


def get_achieved_achievements(steam_id: str | int) -> list[str]:
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={KEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    data = response.json()

    achievements_list = []

    achievements = data['playerstats']['achievements']
    for achievement in achievements:
        achievements_list.append(achievement['name'])

    return achievements_list


def get_all_achievements() -> list[dict[str, str]]:
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={KEY}&appid=440"
    response = requests.get(url)
    data = response.json()

    achievements_list = []

    all_achievements = data['game']['availableGameStats']['achievements']
    for achievement in all_achievements:
        achievement_dict = {
            'idName': achievement['name'],
            'displayName': achievement['displayName'],
            'description': achievement['description'],
            'iconUrl': achievement['icon'],
        }
        achievements_list.append(achievement_dict)

    return achievements_list


def get_missing_achievements(steam_id: str | int ) -> list[dict[str, str]]:
    achieved = get_achieved_achievements(steam_id)
    _all = get_all_achievements()

    missing = []

    for achievement in _all:
        if achievement['idName'] not in achieved:
            missing.append(achievement)

    return missing
