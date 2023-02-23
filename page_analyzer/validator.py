from flask import flash, get_flashed_messages
from urllib.parse import urlparse
import re

MAX_LENGTH = 255


class MaxLengthError(Exception):
    """Raised when the URL have more than MAX_LENGTH characters"""
    pass


class ValidationError(Exception):
    """Raised when the URL isn't valid"""
    pass


def validate(url):
    parse_url, url_length = urlparse(url), len(url)
    scheme, netloc = parse_url.scheme, parse_url.netloc
    valid_netloc = re.match(r"[a-zA-Z]+\.[a-zA-Z]+", netloc)

    try:
        if scheme not in {'http', 'https'}:
            raise ValidationError
        if not netloc or not valid_netloc:
            raise ValidationError
        if url_length > MAX_LENGTH:
            raise MaxLengthError

    except ValidationError:
        flash('Некорректный URL', 'danger')
        if not url:
            flash('URL обязателен', 'danger')

    except MaxLengthError:
        flash(f'URL превышает {MAX_LENGTH} символов', 'danger')

    errors = get_flashed_messages(with_categories=True)
    url = f'{scheme}://{netloc}'
    return errors, url
