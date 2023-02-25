from page_analyzer.validator import MAX_LENGTH
from bs4 import BeautifulSoup
import requests


HIDE_CHARS = '...'


def get_valid_length_data(data):
    if data:
        if len(data) > MAX_LENGTH:
            optimal_length = MAX_LENGTH - len(HIDE_CHARS)
            data = data[:optimal_length] + HIDE_CHARS
    return data


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

    h1 = get_valid_length_data(h1)
    title = get_valid_length_data(title)
    description = get_valid_length_data(description)

    return status_code, h1, title, description
