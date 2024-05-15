import datetime
import flask
import re
import os
import psycopg2

StatusCodes = {
    'success': 200,
    'bad_request': 400,
    'unauthorized': 401,
    'forbidden': 403,
    'not_found': 404,
    'method_not_allowed': 405,
    'internal_error': 500
}

def db_connect():
    conn = psycopg2.connect(
        dbname='dbproj',
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432'
    )
    return conn, conn.cursor()

def db_close(conn, cursor):
    if conn:
        conn.rollback()
        cursor.close()
        conn.close()


def validate_payload(payload, required_fields):
    received = set(payload.keys())
    difference = list(required_fields.difference(received))
    if len(difference) > 0:
        flask.abort(StatusCodes['bad_request'], 'Missing required fields: {}'.format(difference))


def string_to_int(string):
    try:
        return int(string)
    except ValueError:
        return None
    
def validate_string(string, min_len=1, max_len=None, only_digits = False):
    if isinstance(string, str):
        if only_digits and not string.isdigit():
            return False
        if min_len and not None and len(string) < min_len:
            return False
        if max_len and not None and len(string) > max_len:
            return False
        return True
    return False


def validate_int(integer, min_value=None, max_value=None):
    if isinstance(integer, int):
        if min_value and not None and integer < min_value:
            return False
        if max_value and not None and integer > max_value:
            return False
        return True
    return False


def bool_validade(boolean):
    if isinstance(boolean, bool):
        return True
    return False


def validate_password(password):
    if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$", password):
        return False
    return True

def validate_email(email):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return False
    return True

def validate_datetime(date, format, future = False, past = False):
    try:
        date = datetime.datetime.strptime(date, format)
        if future and past:
            # Allows both future and past dates, always true if valid format
            return True
        if future and date < datetime.datetime.now():
            return False
        if past and date > datetime.datetime.now():
            return False
        return True
    except ValueError:
        return False

    