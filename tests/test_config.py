
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
import webbrowser
load_dotenv()

"""

params: dict = {
    "client_id": os.getenv("CLIENT_ID"),
    "response_type": "code",
    "redirect_uri": "http://127.0.0.1:8888/callback",
    "state": None,
    "scope": "user-read-private user-read-email"
}

auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
#webbrowser.open(auth_url)

"""

from flask import Flask

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"<h1>Hello world!</h1>"