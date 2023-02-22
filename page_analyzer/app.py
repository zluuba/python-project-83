from page_analyzer.validator import validate
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import psycopg2
import datetime
import requests
import os
import re

from flask import (
    Flask, render_template,
    request, redirect,
    flash, get_flashed_messages,
    url_for
)

app = Flask(__name__)

load_dotenv()
app.secret_key = os.urandom(12)

database_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(database_url)


@app.route('/')
def main_page():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        return render_template(
            'index.html',
            errors=errors
        ), 422

    url = url.strip()
    url = re.match(r"^[a-z]+://([^/:]+)", url).group(0)

    with conn.cursor() as cursor:
        try:
            current_date = datetime.datetime.now()
            cursor.execute("INSERT INTO urls (name, created_at) "
                           "VALUES (%(name)s, %(created_at)s);",
                           {'name': url, 'created_at': current_date})
            conn.commit()
            flash('Страница успешно добавлена', 'success')

        except psycopg2.Error:
            conn.rollback()
            flash('Страница уже существует', 'info')

        cursor.execute("SELECT id FROM urls WHERE name = %(name)s;",
                       {'name': url})
        id = cursor.fetchone()[0]

    return redirect(url_for('url_page', id=id))


@app.get('/urls')
def urls_list():
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT MAX(url_checks.created_at) AS created_at, "
                       "urls.id, urls.name, url_checks.status_code "
                       "FROM urls LEFT JOIN url_checks "
                       "ON urls.id = url_checks.url_id "
                       "GROUP BY urls.id, url_checks.status_code "
                       "ORDER BY urls.id DESC;")
        urls = cursor.fetchall()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.get('/urls/<int:id>')
def url_page(id):
    messages = get_flashed_messages(with_categories=True)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        data = cursor.fetchone()

        cursor.execute("SELECT * FROM url_checks WHERE url_id = %s "
                       "ORDER BY created_at DESC;", (id,))
        checks = cursor.fetchall()

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
    try:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT name FROM urls WHERE id = %s;", (id,))
            url = cursor.fetchone()
            status_code = requests.get(url.name).status_code

            current_date = datetime.datetime.now()
            cursor.execute("INSERT INTO url_checks "
                           "(url_id, status_code, created_at) "
                           "VALUES (%(url_id)s, %(status_code)s, "
                           "%(created_at)s);",
                           {'url_id': id, 'status_code': status_code,
                            'created_at': current_date})
            conn.commit()
            flash('Страница успешно проверена', 'success')

    except requests.exceptions.ConnectionError:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_page', id=id))
