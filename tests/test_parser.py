from page_analyzer.parser import get_valid_length_data, get_response, get_parse_data
from page_analyzer.validator import MAX_LENGTH
import responses
import requests


def test_get_valid_length_data(correct_html_data, too_long_data):
    h1, title, description = correct_html_data
    assert get_valid_length_data(h1) == h1
    assert get_valid_length_data(title) == title
    assert get_valid_length_data(description) == description

    assert len(too_long_data) >= MAX_LENGTH

    valid_long_data = get_valid_length_data(too_long_data)
    assert len(valid_long_data) <= MAX_LENGTH


@responses.activate
def test_get_response(url, html_page_data):
    file_path, _ = html_page_data

    with open(file_path, 'rb'):
        responses.add(responses.GET, url, status=200)
        assert get_response(url)

        responses.add(responses.GET, url, status=404)
        assert not get_response(url)


@responses.activate
def test_get_parse_data(url, html_page_data):
    file_path, data = html_page_data

    with open(file_path, 'rb') as file:
        responses.add(responses.GET, url, body=file, status=200)
        response = requests.get(url)
        assert get_parse_data(response) == data
