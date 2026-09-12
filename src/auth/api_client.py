# API Client Interface
import requests
from urllib.parse import urljoin

class APIError(Exception):
    pass


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url


    def get(self, endpoint, headers, params=None, timeout=None, tries=None):
        attempts = 0
        url = urljoin(self.base_url, endpoint)

        try:
            resp = requests.get(url=url, headers=headers, params=params, timeout=timeout)
            attempts += 1

            if attempts < tries:
                return "Max attempts exceeded"


            return resp
        except requests.exceptions as err:
            return "error"


    
