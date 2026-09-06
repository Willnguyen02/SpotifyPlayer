from dotenv import load_dotenv
import os
import requests


from .auth.token_manager import bearer_token

load_dotenv()

base_url = "https://api.spotify.com/v1/me"

url = "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb"


headers: dict = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

resp = requests.get(url=base_url, headers=headers)
print(resp.status_code)
print(resp.json())