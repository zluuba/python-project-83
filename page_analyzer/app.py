from page_analyzer.validator import validate
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import psycopg2
import datetime
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
            cursor.execute("INSERT INTO urls (name, created_at)"
                           "VALUES (%(name)s, %(created_at)s);",
                           {'name': url, 'created_at': current_date})
            flash('Страница успешно добавлена', 'success')
            conn.commit()

        except psycopg2.Error:
            conn.rollback()
            flash('Страница уже существует', 'info')

        cursor.execute("SELECT id FROM urls WHERE name = %(name)s;",
                       {'name': url})
        url_id = cursor.fetchone()[0]

    return redirect(url_for('url_page', id=url_id))


@app.get('/urls')
def urls_list():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls ORDER BY created_at DESC;")
        added_urls = cursor.fetchall()
    return render_template(
        'urls.html',
        urls=added_urls,
    )


@app.get('/urls/<int:id>')
def url_page(id):
    messages = get_flashed_messages(with_categories=True)
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        url_data = cursor.fetchone()

    if not url_data:
        return render_template('not_found.html'), 404

    url, date = url_data.name, url_data.created_at.strftime('%Y-%m-%d')
    return render_template(
        'url.html',
        messages=messages,
        id=id,
        url=url,
        date=date
    )


@app.post('/urls/<int:id>/checks')
def checks(id):
    # with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
    #     current_date = datetime.datetime.now()
    #     cursor.execute("INSERT INTO url_checks (url_id, created_at)"
    #                    "VALUES (%(url_id)s, %(created_at)s);",
    #                    {'url_id': id, 'created_at': current_date})
    #
    #     cursor.execute("SELECT * FROM url_checks WHERE url_id = %s;",
    #                    (id,))
    #     check = cursor.fetchone()
    #     flash('Страница успешно проверена', 'success')
    #
    #     # flash('Произошла ошибка при проверке', 'danger')
    # return render_template(
    #     'url.html',
    #     checks=check,
    #     id=id
    # )
    return url_page(id)
