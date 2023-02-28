from page_analyzer.parser import get_parse_data
from psycopg2.extras import NamedTupleCursor
import psycopg2
import datetime
import requests
import os


def connect_to_db():
    connection = psycopg2.connect(os.getenv('DATABASE_URL'))
    return connection


def add_url_to_db(url):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        try:
            current_date = datetime.datetime.now()
            cursor.execute("INSERT INTO urls (name, created_at) "
                           "VALUES (%(name)s, %(created_at)s);",
                           {'name': url, 'created_at': current_date})
            connection.commit()
            is_added = True

        except psycopg2.Error:
            connection.rollback()
            is_added = False

        cursor.execute(
            "SELECT id FROM urls WHERE name = %(name)s;",
            {'name': url}
        )
        id = cursor.fetchone()[0]

    return is_added, id


def get_urls_from_db():
    connection = connect_to_db()
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT MAX(url_checks.created_at) AS created_at, "
                       "urls.id, urls.name, url_checks.status_code "
                       "FROM urls LEFT JOIN url_checks "
                       "ON urls.id = url_checks.url_id "
                       "GROUP BY urls.id, url_checks.status_code "
                       "ORDER BY urls.id DESC;")
        urls = cursor.fetchall()

    return urls


def get_url_from_db(id):
    connection = connect_to_db()
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        data = cursor.fetchone()

        cursor.execute("SELECT * FROM url_checks WHERE url_id = %s "
                       "ORDER BY created_at DESC;", (id,))
        checks = cursor.fetchall()

    return data, checks


def add_check_to_db(id):
    connection = connect_to_db()
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        try:
            cursor.execute("SELECT name FROM urls WHERE id = %s;", (id,))
            url = cursor.fetchone()
            response = requests.get(url.name, timeout=10)
            status_code = response.status_code

            if status_code < 100 or status_code > 400:
                raise ConnectionError

            data = get_parse_data(response.content)

            current_date = datetime.datetime.now()
            cursor.execute("INSERT INTO url_checks "
                           "(url_id, status_code, h1, title, "
                           "description, created_at) "
                           "VALUES (%(url_id)s, %(status_code)s, "
                           "%(h1)s, %(title)s, %(description)s, "
                           "%(created_at)s);",
                           {'url_id': id, 'status_code': status_code,
                            'h1': data['h1'], 'title': data['title'],
                            'description': data['description'],
                            'created_at': current_date})
            connection.commit()
            return True

        except requests.exceptions.ConnectionError:
            connection.rollback()
            return False

        except ConnectionError:
            return False
