from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import psycopg2
import datetime


load_dotenv()

DATE = datetime.datetime.now()


def connect(app):
    db_url = app.config['DATABASE_URL']
    return psycopg2.connect(db_url)


def get_data_from_id(id, connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        data = cursor.fetchone()
    return data


def get_urls_from_db(connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT MAX(url_checks.created_at) AS created_at, "
                       "urls.id, urls.name, url_checks.status_code "
                       "FROM urls LEFT JOIN url_checks "
                       "ON urls.id = url_checks.url_id "
                       "GROUP BY urls.id, url_checks.status_code "
                       "ORDER BY urls.id DESC;")
        urls = cursor.fetchall()

    return urls


def get_url_from_db(id, connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM url_checks WHERE url_id = %s "
                       "ORDER BY created_at DESC;", (id,))
        checks = cursor.fetchall()

    data = get_data_from_id(id, connection)
    return data, checks


def add_url_check_to_db(id, data, connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("INSERT INTO url_checks "
                       "(url_id, status_code, h1, title, "
                       "description, created_at) "
                       "VALUES (%(url_id)s, %(status_code)s, "
                       "%(h1)s, %(title)s, %(description)s, "
                       "%(created_at)s);",
                       {'url_id': id, 'status_code': data['status_code'],
                        'h1': data['h1'], 'title': data['title'],
                        'description': data['description'],
                        'created_at': DATE})
        connection.commit()


def add_url_to_db(url, connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO urls (name, created_at) "
                           "VALUES (%(name)s, %(created_at)s);",
                           {'name': url, 'created_at': DATE})
            connection.commit()
            is_added = True

        except psycopg2.Error:
            connection.rollback()
            is_added = False

        cursor.execute("SELECT id FROM urls WHERE name = %(name)s;",
                       {'name': url})
        id = cursor.fetchone()[0]

    return is_added, id
