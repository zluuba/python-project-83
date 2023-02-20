from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for
from datetime import date
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'super secret key'

try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
except:
    print('Can`t establish connection to database')


def validate(url):
    return True


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.post('/urls')   # Button click
def add_urls():
    url = request.form.get('url')
    # if not url:
    #     flash('URL обязателен', 'error')
    #     return redirect('/')

    # url_errors = validate(url)
    # if url_errors:
    #     for error in url_errors:
    #           flash(error, 'error')
    #     return render_template(
    #         'index.html',
    #         search=url
    #     ), 422

    current_date = date.today()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name, created_at) VALUES (%(name)s, %(created_at)s)", {'name': url, 'created_at': current_date})
        cursor.execute("SELECT id FROM urls WHERE name = %(name)s", {'name': url})
        url_id = cursor.fetchone()[0]
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(
            url_for('url_page',
            id=url_id)
        )


@app.get('/urls/<id>')
def url_page(id):
    return render_template(
        'url_page.html'
    )


@app.route('/urls', methods=['GET'])   # Header
def urls_list():
    return render_template(
        'urls.html'
    )
