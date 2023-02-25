from page_analyzer.common import get_valid_length_data, get_html_data, HIDE_CHARS
from page_analyzer.validator import MAX_LENGTH
from flask import Flask
import responses


app = Flask(__name__)
app.testing = True
client = app.test_client()
app.secret_key = 'test-key'


def test_get_valid_length_data(correct_html_data, too_long_data):
    h1, title, description, empty_data = correct_html_data
    assert get_valid_length_data(h1) == h1
    assert get_valid_length_data(title) == title
    assert get_valid_length_data(description) == description

    valid_long_data = get_valid_length_data(too_long_data)
    assert len(valid_long_data) <= MAX_LENGTH
    assert valid_long_data[-3:] == HIDE_CHARS


@responses.activate
def test_get_html_data(url, status_codes, html_page_data):
    file_path, h1, title, description = html_page_data
    success, error = status_codes

    with open(file_path, 'rb') as file:
        responses.add(responses.GET, url, body=file, status=success)
        assert get_html_data(url) == (success, h1, title, description)

        responses.add(responses.GET, url, body=file, status=error)
        assert get_html_data(url) == (error, None, None, None)
