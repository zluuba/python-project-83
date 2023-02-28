from page_analyzer.validator import validate
from dotenv import load_dotenv
import os
from page_analyzer.database import (
    add_url_to_db, get_urls_from_db,
    get_url_from_db, add_check_to_db
)
from flask import (
    Flask, render_template,
    request, redirect,
    flash, get_flashed_messages,
    url_for
)

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

app.config.update(
    DATABASE_URL=DATABASE_URL,
    SECRET_KEY=SECRET_KEY
)


@app.route('/')
def main_page():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def add_url():
    raw_url = request.form.get('url')
    errors, url = validate(raw_url)
    if errors:
        return render_template(
            'index.html',
            errors=errors
        ), 422

    is_added, id = add_url_to_db(url)
    if not is_added:
        flash('Страница уже существует', 'info')
    else:
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('url_page', id=id))


@app.get('/urls')
def urls_list():
    urls = get_urls_from_db()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.get('/urls/<int:id>')
def url_page(id):
    messages = get_flashed_messages(with_categories=True)
    data, checks = get_url_from_db(id)

    if not data:
        return render_template('not_found.html'), 404

    return render_template(
        'url.html',
        messages=messages,
        data=data,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def check(id):
    is_added = add_check_to_db(id)
    if is_added:
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_page', id=id))
