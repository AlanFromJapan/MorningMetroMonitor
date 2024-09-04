import requests

def get_web_page_content(url):
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

