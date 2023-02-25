from page_analyzer.validator import validate
from flask import Flask


app = Flask(__name__)
app.testing = True
client = app.test_client()
app.secret_key = 'test-key'


def test_validate_wrong_url(wrong_urls, danger_flash_messages):
    too_long_url, wrong_schema, invalid_char, blank_req = wrong_urls
    wrong, empty, too_long = danger_flash_messages

    with app.test_request_context():
        assert validate(too_long_url)[0] == [too_long]
    with app.test_request_context():
        assert validate(wrong_schema)[0] == [wrong]
    with app.test_request_context():
        assert validate(invalid_char)[0] == [wrong]
    with app.test_request_context():
        assert validate(blank_req)[0] == [wrong, empty]


def test_validate_correct_url(correct_urls, correct_urls_short):
    corr1, corr2, corr3 = correct_urls
    short1, short2, short3 = correct_urls_short

    with app.test_request_context():
        assert validate(corr1) == ([], short1)
    with app.test_request_context():
        assert validate(corr2) == ([], short2)
    with app.test_request_context():
        assert validate(corr3) == ([], short3)
