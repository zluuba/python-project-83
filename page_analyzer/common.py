from bs4 import BeautifulSoup
import requests


def get_html_data(url):
    response = requests.get(url)
    status_code = response.status_code

    html = BeautifulSoup(response.content, 'html.parser')

    h1 = html.h1.string if html.h1 else None
    title = html.title.string if html.title else None
    description = [
        tag.get('content') for tag in html.find_all('meta') if
        tag.get('name') == 'description'
    ]
    description = description[0] if description else None

    return status_code, h1, title, description
