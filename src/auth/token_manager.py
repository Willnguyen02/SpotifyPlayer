# Handles bearer token exchanges
# Spotify token refreshes every 60 minutes

from dotenv import load_dotenv
import os
import requests
from src.auth.endpoints import Endpoints

load_dotenv()

bearer_url = "https://accounts.spotify.com/api/token"


bearer_headers: dict = {
    "Content-Type": "application/x-www-form-urlencoded"
}

bearer_params: dict = {
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "grant_type": "client_credentials"
}

resp = requests.post(url=bearer_url, headers=bearer_headers, params=bearer_params)
data = resp.json()

bearer_token = data["access_token"]


# =============================================================



class TokenManager:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret


    def get_token(self):
        bearer_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        bearer_params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        bearer = requests.post(url=Endpoints.BEARER_URL, headers=bearer_headers, params=bearer_params)
        bearer.raise_for_status()

        bearer = bearer.json()
        return bearer["access_token"]


x = TokenManager(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))
print(x.get_token())