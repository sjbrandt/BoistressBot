import json


class User:
    def __init__(self, id_or_username: str | int):
        json_object = _get_json_object(id_or_username)
        self.discord_username = json_object["discord_username"]
        self.discord_id = json_object["discord_id"]
        self.discord_mention = f"<@{self.discord_id}>"
        self.steam_id = json_object["steam_id"]
        self._registered_hours = json_object["registered_hours"]

    @property
    def registered_hours(self):
        return self._registered_hours

    @registered_hours.setter
    def registered_hours(self, hours: int):
        self._registered_hours = hours
        self.update_json_attribute("registered_hours", hours)

    def update_json_attribute(self, attribute_name, value):
        users = load_users()
        for user in users:
            if user["discord_username"] == self.discord_username:
                user[attribute_name] = value
        save_users(users)


def _get_json_object(id_or_username: str | int):
    users = load_users()
    for user in users:
        if _id_match(id_or_username, users):
            return user
    return None


def load_users():
    f = open('users.json')
    users = json.load(f)
    return users


def save_users(users: dict[str, any]):
    json_object = json.dumps(users, indent=2)
    with open('users.json', 'w') as file:
        file.write(json_object)


def _id_match(id_or_username: str | int, user: dict[str, any]) -> bool:
    accepted_ids = [
        user['discord_username'],
        user['discord_id'],
        f"<@{user['discord_id']}",  # such that a user can also be identified by discord mention
        user['steam_id']
    ]
    if id_or_username in accepted_ids:
        return True
    return False
