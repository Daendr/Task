import requests


class ApiUtils:
    @staticmethod
    def post(base_url, url_parts):
        response = requests.post(base_url+url_parts)
        return response
