from urllib.parse import urlparse
from flask import flash, get_flashed_messages


def validate(url):
    errors = []

    try:
        result = urlparse(url)
        acceptable_length = 255
        is_valid_url = all([result.scheme, result.netloc]) and \
                       len(url) <= acceptable_length
        if not is_valid_url:
            raise Exception
    except:
        flash('Некорректный URL', 'error')
        if not url:
            flash('URL обязателен', 'error')
        errors = get_flashed_messages()

    return errors
