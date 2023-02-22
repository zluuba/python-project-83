from urllib.parse import urlparse
from flask import flash, get_flashed_messages

MAX_LENGTH = 255


class MaxLengthError(Exception):
    """Raised when the URL have more than MAX_LENGTH characters"""
    pass


def validate(url):
    try:
        result, url_length = urlparse(url), len(url)
        if not all([result.scheme, result.netloc]):
            raise AttributeError
        if url_length > MAX_LENGTH:
            raise MaxLengthError

    except AttributeError:
        flash('Некорректный URL', 'danger')
        if not url:
            flash('URL обязателен', 'danger')

    except MaxLengthError:
        flash('URL превышает 255 символов', 'danger')

    errors = get_flashed_messages(with_categories=True)
    return errors
