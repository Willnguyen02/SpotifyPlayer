from dotenv import load_dotenv
import os
import requests

from src.auth.token_manager import TokenManager

"""
token_manager = TokenManager(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

bearer_token = token_manager.get_token()


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

"""

from dotenv import load_dotenv
from urllib.parse import urlencode
import webbrowser
load_dotenv()


params: dict = {
    "client_id": os.getenv("CLIENT_ID"),
    "response_type": "code",
    "redirect_uri": "http://127.0.0.1:8888/callback",
    "state": None,
    "scope": "user-read-private user-read-email"
}

auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
#webbrowser.open(auth_url)



# ==========================================================

# SAMPLE: Recreate this from scratch
# Store in TokenManager

# ==========================================================

import os
import secrets
import requests
import base64
from dotenv import load_dotenv
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8888/callback"

auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = parse_qs(urlparse(self.path).query)
        auth_code = query.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Authorized! You can close this tab.</h1>")

        # Shut down the server after handling the request
        threading.Thread(target=self.server.shutdown).start()

def get_auth_code():
    server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)

    state = secrets.token_hex(16)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": "user-read-private user-read-email"
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    webbrowser.open(auth_url)

    server.serve_forever()  # blocks until shutdown() is called above
    return auth_code

code = get_auth_code()
print("Authorization code:", code)

# Exchange the code for an access token
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

token_response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {b64_auth_str}"},
    data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
)

token_data = token_response.json()
access_token = token_data.get("access_token")
print("Access token:", access_token)