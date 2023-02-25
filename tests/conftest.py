from page_analyzer.validator import MAX_LENGTH
from string import ascii_lowercase, digits
import random
import pytest
# import os

#
# def get_fixture_path(name):
#     return os.path.join('tests/fixtures/', name)


def get_too_long_url(length):
    string = random.choices(ascii_lowercase + digits, k=length)
    return 'https://toolongurl.en/' + ''.join(string)


@pytest.fixture
def correct_urls():
    url1 = 'https://www.google.com/search?q=correct&oq=correct'
    url2 = 'https://correct.rl.com/correct'
    url3 = 'http://correct-url.org'
    return url1, url2, url3


@pytest.fixture
def correct_urls_short():
    url1 = 'https://www.google.com'
    url2 = 'https://correct.rl.com'
    url3 = 'http://correct-url.org'
    return url1, url2, url3


@pytest.fixture
def wrong_urls():
    url1 = get_too_long_url(MAX_LENGTH)
    url2 = 'htttps://wrong.com'
    url3 = 'http://wrong@org'
    url4 = ''
    return url1, url2, url3, url4


@pytest.fixture
def danger_flash_messages():
    wrong = ('danger', 'Некорректный URL')
    empty = ('danger', 'URL обязателен')
    too_long = ('danger', f'URL превышает {MAX_LENGTH} символов')
    return wrong, empty, too_long
