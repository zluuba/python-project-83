from page_analyzer.validator import validate
from psycopg2.extras import NamedTupleCursor
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
app.secret_key = 'super secret key'

database_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(database_url)


@app.route('/')
def main_page():
    return render_template(
        'index.html'
    )


@app.post('/urls')   # Button click
def add_urls():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        return render_template(
            'index.html',
            errors=errors
        ), 422

    with conn.cursor() as cursor:
        current_date = datetime.datetime.now()
        cursor.execute("INSERT INTO urls (name, created_at) VALUES (%(name)s, %(created_at)s);",
                        {'name': url, 'created_at': current_date})
        cursor.execute("SELECT id FROM urls WHERE name = %(name)s;", {'name': url})
        url_id = cursor.fetchone()[0]
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(
            url_for('url_page', id=url_id),
        )


@app.get('/urls/<int:id>')
def url_page(id):
    messages = get_flashed_messages()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        url_data = cursor.fetchone()

    url, date = url_data.name, url_data.created_at.strftime('%Y-%m-%d')
    domain = re.match(r"^[a-z]+://([^/:]+)", url).group(0)

    return render_template(
        'url_page.html',
        messages=messages,
        id=id,
        url=domain,
        date=date
    )


@app.route('/urls', methods=['GET'])   # Header
def urls_list():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls ORDER BY created_at DESC;")
        added_urls = cursor.fetchall()
        return render_template(
            'urls.html',
            urls=added_urls,
        )
