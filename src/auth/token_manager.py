# Handles bearer token exchanges
# Spotify token refreshes every 60 minutes

from dotenv import load_dotenv
import os
import requests
import time
import schedule
from src.auth.endpoints import Endpoints

load_dotenv()

# =============================================================

"""
Redo TokenManager to account for Spotify Authorization Flow - https://developer.spotify.com/documentation/web-api/tutorials/code-flow 





"""

class TokenManager:

    """
    Token Manager Class

    Functionality:
        This class exchanges Spotify Client ID and Secret for a Bearer token which can be used for API calls.
        The Bearer token expires in 60 minutes hence the refresh_token method.

    get_token():
        This function exchanges client credentials for bearer token

    refresh_token():
        This function obtains a new refreshed Bearer token and is called every hour using the 'schedule' Python module.

    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        self.token = None


    def get_token(self) -> str:

        bearer = requests.post(url=Endpoints.BEARER_URL, headers=self.headers, params=self.params)
        bearer.raise_for_status()

        self.token = bearer.json()["access_token"]
        return self.token


    def refresh_token(self) -> str | None:

        try: 
            self.get_token()
            print("Token refreshed")
            return self.token
        
        except requests.RequestException as e:
            print(f"Token refreshed failed {e}")
            return None


def main():
    # Get bearer token
    bearer_token = TokenManager(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))
    bearer_token.get_token()

    # Run refresh_token method every hour
    schedule.every(1).hour.do(bearer_token.refresh_token)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()