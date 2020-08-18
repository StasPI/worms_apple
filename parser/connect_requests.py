import requests


def go_connect(URL):
    req = requests.get(URL)
    if req.status_code != 200:
        raise ConnectionError('Status Code != 200')
    else:
        req = req.content
        return req