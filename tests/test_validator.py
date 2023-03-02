from page_analyzer.validator import (
    get_validation_errors, get_normalized_url, get_url_parts
)
from flask import Flask


app = Flask(__name__)
app.testing = True
app.secret_key = 'test-key'


def test_get_validation_errors_wrong_url(wrong_urls, danger_flash_messages):
    too_long_url, wrong_schema, invalid_char, blank_req = wrong_urls
    wrong, empty, too_long = danger_flash_messages

    with app.test_request_context():
        assert get_validation_errors(too_long_url) == [too_long]
    with app.test_request_context():
        assert get_validation_errors(wrong_schema) == [wrong]
    with app.test_request_context():
        assert get_validation_errors(invalid_char) == [wrong]
    with app.test_request_context():
        assert get_validation_errors(blank_req) == [wrong, empty]


def test_get_validation_errors_correct_url(correct_urls):
    corr1, corr2, corr3 = correct_urls

    with app.test_request_context():
        assert not get_validation_errors(corr1)
    with app.test_request_context():
        assert not get_validation_errors(corr2)
    with app.test_request_context():
        assert not get_validation_errors(corr3)


def test_get_normalized_url(correct_urls, normalized_urls):
    url1, url2, url3 = correct_urls
    normalized1, normalized2, normalized3 = normalized_urls

    assert get_normalized_url(url1) == normalized1
    assert get_normalized_url(url2) == normalized2
    assert get_normalized_url(url3) == normalized3


def test_get_url_parts(correct_urls, urls_parts):
    url1, url2, url3 = correct_urls
    parts1, parts2, parts3 = urls_parts

    assert get_url_parts(url1) == parts1
    assert get_url_parts(url2) == parts2
    assert get_url_parts(url3) == parts3
