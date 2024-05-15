import flask
import psycopg2
import datetime
import hashlib
import secrets
import jwt
import os
import functools
import utils

app = flask.Flask(__name__)


@app.route('/dbproj/register/patient', methods=['POST'])
def register_patient():
    print('register_patient')
    payload = flask.request.json
    required_fields = {'username', 'email', 'password'}
    utils.validate_payload(payload, required_fields)
    name = payload['username']
    email = payload['email']
    password = payload['password']

    if not utils.validate_string(name, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid name')
    if not utils.validate_string(email, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    if not utils.validate_string(password, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')

    #verify password
    if not utils.validate_password(password):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_email(email):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    
    conn, cursor = utils.db_connect()

    #statement to add a new patient
    statement = 'INSERT INTO pacientes (username, email, password) VALUES (%s, %s, %s) RETURNING id_pac'

    values = (name, email, password)

    try:
        cursor.execute(statement, values)
        conn.commit()
        patient_id = cursor.fetchone()[0]
        response = {'results': f"Patient added with id {patient_id}"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flask.abort(utils.StatusCodes['bad_request'], 'Email already in use')
    except psycopg2.DatabaseError as e:
        print(e)
        conn.rollback()
        flask.abort(utils.StatusCodes['internal_error'], 'Database error')
    finally:
        utils.db_close(conn, cursor)
    return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])


@app.route('/dbproj/register/assistant', methods=['POST'])
def register_assistant():
    print('register_assistant')
    payload = flask.request.json
    required_fields = {'username', 'email', 'password', 'dur_contrato', 'salary', 'seccao'}
    utils.validate_payload(payload, required_fields)
    name = payload['username']
    email = payload['email']
    password = payload['password']
    dur_contrato = payload['dur_contrato']
    salary = payload['salary']
    seccao = payload['seccao']

    if not utils.validate_string(name, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid name')
    if not utils.validate_string(email, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    if not utils.validate_string(password, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_int(dur_contrato, min_value=1, max_value=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid dur_contrato')
    if not utils.validate_int(salary, min_value=1, max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid salary')
    if not utils.validate_string(seccao, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid seccao')
    

    #verify password
    if not utils.validate_password(password):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_email(email):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    
    conn, cursor = utils.db_connect()

    #statement to add a new assistant to the table Trabalhadores e Assistente
    statement1 = 'INSERT INTO trabalhadores (username, email, password, dur_contrato, salary) VALUES (%s, %s, %s, %s, %s) RETURNING id_trab'
    values = (name, email, password, dur_contrato, salary)

    try:
        cursor.execute(statement1, values)
        conn.commit()
        assistant_id = cursor.fetchone()[0]
        print(assistant_id)

        statement2 = 'INSERT INTO assistente (seccao, trabalhadores_id_trab) VALUES (%s, %s)'
        values2 = (seccao, assistant_id)
        try:
            cursor.execute(statement2, values2)
            conn.commit()
            response = {'results': f"Assistant added with id {assistant_id}"}
        except:
            conn.rollback()
            flask.abort(utils.StatusCodes['bad_request'], 'Error adding assistant')
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flask.abort(utils.StatusCodes['bad_request'], 'Email already in use')
    except psycopg2.DatabaseError as e:
        print(e)
        conn.rollback()
        flask.abort(utils.StatusCodes['internal_error'], 'Database error')
    finally:
        utils.db_close(conn, cursor)
    return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])

@app.route('/dbproj/register/nurse', methods=['POST'])
def register_nurse():
    print('register_nurse')
    payload = flask.request.json
    required_fields = {'username', 'email', 'password', 'dur_contrato', 'salary', 'role', 'categoria'}
    utils.validate_payload(payload, required_fields)
    name = payload['username']
    email = payload['email']
    password = payload['password']
    dur_contrato = payload['dur_contrato']
    salary = payload['salary']
    role = payload['role']
    categoria = payload['categoria']

    if not utils.validate_string(name, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid name')
    if not utils.validate_string(email, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    if not utils.validate_string(password, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_int(dur_contrato, min_value=1, max_value=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid dur_contrato')
    if not utils.validate_int(salary, min_value=1, max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid salary')
    if not utils.validate_string(role, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid role')
    if not utils.validate_string(categoria, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid categoria')

    

    #verify password
    if not utils.validate_password(password):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_email(email):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    
    conn, cursor = utils.db_connect()

    #statement to add a new nurse to the table Trabalhadores e Enfermeiro
    statement1 = 'INSERT INTO trabalhadores (username, email, password, dur_contrato, salary) VALUES (%s, %s, %s, %s, %s) RETURNING id_trab'
    values = (name, email, password, dur_contrato, salary)

    try:
        cursor.execute(statement1, values)
        conn.commit()
        nurse_id = cursor.fetchone()[0]
        print(nurse_id)

        statement2 = 'INSERT INTO enfermeiro (role, categoria, trabalhadores_id_trab) VALUES (%s, %s, %s)'
        values2 = (role, categoria, nurse_id)
        try:
            cursor.execute(statement2, values2)
            conn.commit()
            response = {'results': f"Nurse added with id {nurse_id}"}
        except:
            conn.rollback()
            flask.abort(utils.StatusCodes['bad_request'], 'Error adding nurse')
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flask.abort(utils.StatusCodes['bad_request'], 'Email already in use')
    except psycopg2.DatabaseError as e:
        print(e)
        conn.rollback()
        flask.abort(utils.StatusCodes['internal_error'], 'Database error')
    finally:
        utils.db_close(conn, cursor)
    return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])





if __name__ == '__main__':
    host='127.0.0.1'
    port= 8080
    app.run(host=host, port=port, debug=True, threaded=True)