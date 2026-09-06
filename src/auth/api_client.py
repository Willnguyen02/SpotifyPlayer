# API Client Interface
import requests

class APIError(Exception):
    pass


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url

    
