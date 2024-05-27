import requests


def random_loadout():
    url = "https://genr8rs.com/api/Content/Tf2/LoadoutGenerator?_sChosenClass=Random"
    response = requests.get(url)
    data = response.json()
    if '_sBuilding' not in data:
        data['_sBuilding'] = None

    return data
