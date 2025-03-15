import os
import requests

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('TEAMWORK_TF_API_KEY')

def get_comp_activity():
    url = f"https://teamwork.tf/api/v1/competitive/provider/valve-mm/stats?key={KEY}"
    response = requests.get(url)
    data = response.json()

    return data
