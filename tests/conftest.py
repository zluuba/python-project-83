from page_analyzer.validator import MAX_LENGTH
from string import ascii_lowercase, digits
import random
import pytest
import os


def get_fixture_path(name):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(parent_dir, 'fixtures/', name)


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


@pytest.fixture
def correct_html_data():
    h1 = 'headline'
    title = 'some correct title'
    description = 'not too long correct description'
    return h1, title, description


@pytest.fixture
def too_long_data():
    return ('''Down, down, down. There was nothing else to
            do, so Alice soon began talking again. "Dinah 'll
            miss me very much to-night, I should think !"
            (Dinah was the cat.)" I hope they'll remember
            her saucer of milk at tea-time. Dinah, my dear!
            I wish you were down here with me! There
            are no mice in the air, I'm afraid, but you
            might catch a bat, and that's very like a mouse,
            you know. But do cats eat bats, I wonder?''')


@pytest.fixture
def html_page_data():
    file_path = get_fixture_path('html_page.html')
    h1 = 'Some header'
    title = 'Some title'
    description = 'Some description'
    return file_path, dict(h1=h1, title=title, description=description)


@pytest.fixture
def url():
    return 'http://test.com/'
