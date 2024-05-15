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

@app.route('/dbproj/register/doctor', methods=['POST'])
def register_doctor():
    print('register_doctor')
    payload = flask.request.json
    required_fields = {'username', 'email', 'password', 'dur_contrato', 'salary', 'licenca', 'especializacao'}
    utils.validate_payload(payload, required_fields)
    name = payload['username']
    email = payload['email']
    password = payload['password']
    dur_contrato = payload['dur_contrato']
    salary = payload['salary']
    licenca = payload['licenca']
    especializacao= payload['especializacao']

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
    if not utils.validate_int(licenca, min_value=1, max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid licence')
    if not utils.validate_string(especializacao, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid especialidade')

    

    #verify password
    if not utils.validate_password(password):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
    if not utils.validate_email(email):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    
    conn, cursor = utils.db_connect()

    #statement to add a new doctor to the table Trabalhadores e Medico
    statement1 = 'INSERT INTO trabalhadores (username, email, password, dur_contrato, salary) VALUES (%s, %s, %s, %s, %s) RETURNING id_trab'
    values = (name, email, password, dur_contrato, salary)

    try:
        cursor.execute(statement1, values)
        conn.commit()
        doctor_id = cursor.fetchone()[0]
        print(doctor_id)

        statement2 = 'INSERT INTO medico (licenca, trabalhadores_id_trab) VALUES (%s, %s)'
        values2 = (licenca, doctor_id)
        try:
            cursor.execute(statement2, values2)
            conn.commit()

            statement3 = 'INSERT INTO especializacao (especializacao, id_medico) VALUES (%s, %s)'
            values3 = (especializacao, doctor_id)
            try:
                cursor.execute(statement3, values3)
                conn.commit()
                response = {'results': f"Doctor added with id {doctor_id}"}
            except:
                conn.rollback()
                flask.abort(utils.StatusCodes['bad_request'], 'Error adding doctor specialization')
        except:
            conn.rollback()
            flask.abort(utils.StatusCodes['bad_request'], 'Error adding doctor')
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


@app.route('/dbproj/user', methods=['POST'])
def login():

    print('login')
    payload = flask.request.json
    required_fields = {'email', 'password'}
    utils.validate_payload(payload, required_fields)
    email = payload['email']
    password = payload['password']

    if not utils.validate_string(email, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    if not utils.validate_string(password, min_len=1, max_len=100):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')


    if not utils.validate_email(email):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    if not utils.validate_password(password):
        flask.abort(utils.StatusCodes['unauthorized'], 'Wrong password')

    try:
        conn, cursor = utils.db_connect()

        #need to check if the user is a patient, assistant, nurse or doctor
        statement = f"SELECT id_pac, username, password FROM pacientes WHERE email LIKE '{email}'"
        values = (email)
        try:
            cursor.execute(statement)
            patient = cursor.fetchone()
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        if patient:
            if patient[2] == password:
                #generate jwt token for patient with patient info
                token = jwt.encode({'id': patient[0], 'name': patient[1], 'type': 'patient'}, key=os.environ.get("KEY"), algorithm='HS256')

                response = {'results': f"Patient {patient[1]} logged in", 'token': token}
                return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])
            else:
                flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
        else:
            statement = f"SELECT id_trab, username, password FROM trabalhadores WHERE email LIKE '{email}'"
            values = (email)
            try:
                cursor.execute(statement)
                worker = cursor.fetchone()
            except psycopg2.DatabaseError as e:
                print(e)
                conn.rollback()
                flask.abort(utils.StatusCodes['internal_error'], 'Database error')
            if worker:
                if worker[2] == password:
                    #check if the worker is an assistant, nurse or doctor
                    statement = f"SELECT seccao FROM assistente WHERE trabalhadores_id_trab = '{worker[0]}'"
                    values = (worker[0])
                    try:
                        cursor.execute(statement)
                        assistant = cursor.fetchone()
                    except psycopg2.DatabaseError as e:
                        print(e)
                        conn.rollback()
                        flask.abort(utils.StatusCodes['internal_error'], 'Database error')
                    if assistant:
                        #generate jwt token for assistant with assistant info
                        token = jwt.encode({'id': worker[0], 'name': worker[1], 'type': 'assistant', 'section': assistant[0]}, key=os.environ.get("KEY"), algorithm='HS256')

                        response = {'results': f"Assistant {worker[1]} logged in", 'token': token}
                        return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])
                    else:
                        statement = f"SELECT role, categoria FROM enfermeiro WHERE trabalhadores_id_trab = '{worker[0]}'"
                        values = (worker[0])
                        try:
                            cursor.execute(statement)
                            nurse = cursor.fetchone()
                        except psycopg2.DatabaseError as e:
                            print(e)
                            conn.rollback()
                            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
                        if nurse:
                            #generate jwt token for nurse with nurse info
                            token = jwt.encode({'id': worker[0], 'name': worker[1], 'type': 'nurse', 'role': nurse[0], 'category': nurse[1]}, key=os.environ.get("KEY"), algorithm='HS256')

                            response = {'results': f"Nurse {worker[1]} logged in", 'token': token}
                            return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])
                        else:
                            statement = f"SELECT licenca FROM medico WHERE trabalhadores_id_trab = '{worker[0]}'"
                            values = (worker[0])
                            try:
                                cursor.execute(statement)
                                doctor = cursor.fetchone()
                            except psycopg2.DatabaseError as e:
                                print(e)
                                conn.rollback()
                                flask.abort(utils.StatusCodes['internal_error'], 'Database error')
                            if doctor:
                                #generate jwt token for doctor with doctor info
                                print(doctor)
                                token = jwt.encode({'id': worker[0], 'name': worker[1], 'type': 'doctor', 'licence': doctor[0]}, key=os.environ.get("KEY") , algorithm='HS256')

                                #add token to the response

                                response = {'results': f"Doctor {worker[1]} logged in", 'token': token}
                                return flask.make_response(flask.jsonify(response), utils.StatusCodes['success'])
                            else:
                                conn.rollback()
                                flask.abort(utils.StatusCodes['internal_error'], 'Database error')
                else:
                    flask.abort(utils.StatusCodes['bad_request'], 'Invalid password')
            else:
                conn.rollback()
                flask.abort(utils.StatusCodes['bad_request'], 'Invalid email')
    finally:
        utils.db_close(conn, cursor)

@app.route('/dbproj/surgery/<hospitalization_id>', methods=['POST'])
#@app.route('/dbproj/surgery', methods=['POST'])
def schedule_surgery(hospitalization_id=None):
    print('schedule_surgery')
    #receive the token from the header
    token = flask.request.headers.get('Authorization')
    

    #remove the 'Bearer ' from the token
    token = token.split(' ')[1] if token else None

    
    if not token:
        flask.abort(utils.StatusCodes['unauthorized'], 'Missing token')
    try:
        #decode the token
        decoded = jwt.decode(token, key=os.environ.get("KEY"), algorithms='HS256')
    except jwt.ExpiredSignatureError:
        flask.abort(utils.StatusCodes['unauthorized'], 'Expired token')
    

    #check if the user is a doctor
    if decoded['type'] != 'assistant':
        flask.abort(utils.StatusCodes['forbidden'], 'Forbidden')

    assistant_id = decoded['id']

    #verify the payload
    payload = flask.request.json
    required_fields = {'patient_id', 'doctor', 'nurses', 'date', 'time', 'enf_responsavel'}
    utils.validate_payload(payload, required_fields)

    patient_id = payload['patient_id']
    doctor = payload['doctor']
    nurses = payload['nurses']
    date = payload['date']
    time = payload['time']
    enf_responsavel = payload['enf_responsavel']

    if not utils.validate_int(patient_id, min_value=1, max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid patient_id')
    if not utils.validate_int(doctor, min_value=1,max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid doctor name')
    if not utils.validate_list(nurses, min_len=1, max_len=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid nurses list')
    if not utils.validate_datetime(date, '%Y-%m-%d'):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid date')
    if not utils.validate_int(enf_responsavel, min_value=1, max_value=None):
        flask.abort(utils.StatusCodes['bad_request'], 'Invalid enf_responsavel')

    if hospitalization_id:
        '''
        if not utils.validate_int(hospitalization_id, min_value=1, max_value=None):
            flask.abort(utils.StatusCodes['bad_request'], 'Invalid hospitalization_id')
        '''
        #check if the hospitalization exists
        conn, cursor = utils.db_connect()
        statement = f"SELECT id_inter FROM internamento WHERE id_inter = '{hospitalization_id}'"

        try:
            cursor.execute(statement)
            hospitalization = cursor.fetchone()

            if not hospitalization:
                conn.rollback()
                flask.abort(utils.StatusCodes['not_found'], 'Hospitalization not found')

            
            #create the surgery for the hospitalization
            statement = 'INSERT INTO cirurgia (internamento_id_inter, medico_trabalhadores_id_trab) VALUES (%s, %s) RETURNING id_cirur'
            values = (hospitalization_id, doctor)

            try:
                cursor.execute(statement, values)
                conn.commit()
                surgery_id = cursor.fetchone()[0]

                print("SURGERY CREATED")

                #add the nurses to the surgery
                for nurse in nurses:
                    statement = 'INSERT INTO cirurgia_enfermeiro (cirurgia_id_cirur, enfermeiro_trabalhadores_id_trab) VALUES (%s, %s)'
                    values = (surgery_id, nurse[0])
                    try:
                        cursor.execute(statement, values)
                        conn.commit()

                        print("NURSE ADDED")
                    except psycopg2.DatabaseError as e:
                        print(e)
                        conn.rollback()
                        flask.abort(utils.StatusCodes['internal_error'], 'Database error')

                    #update the bill for the hospitalization with the surgery cost
                    statement = f"SELECT fatura_id_fatura FROM internamento WHERE id_inter = '{hospitalization_id}'"
                    try:
                        cursor.execute(statement)
                        invoice_id = cursor.fetchone()[0]

                        print(invoice_id)

                        statement = f"UPDATE fatura SET valor_total = valor_total + 150 WHERE id_fatura = '{invoice_id}'"
                        try:
                            cursor.execute(statement)
                            conn.commit()

                            print('INVOICE UPDATED')

                            response = {'results': f"Surgery scheduled for hospitalization {hospitalization_id}"}
                            return flask.make_response(flask.jsonify(response), utils.StatusCodes['success']) 
                        
                        except psycopg2.DatabaseError as e:
                            print(e)
                            conn.rollback()
                            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
                    except psycopg2.DatabaseError as e:
                        print(e)
                        conn.rollback()
                        flask.abort(utils.StatusCodes['internal_error'], 'Database error')
            except psycopg2.DatabaseError as e:
                print(e)
                conn.rollback()
                flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        finally:
            utils.db_close(conn, cursor)

    elif not hospitalization_id:
        #create new invoice
        conn, cursor = utils.db_connect()
        statement = 'INSERT INTO fatura (valor_total) VALUES (0) RETURNING id_fatura'

        try:
            cursor.execute(statement)
            conn.commit()
            invoice_id = cursor.fetchone()[0]
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        finally:
            utils.db_close(conn, cursor)

        #create a new hospitalization
        conn, cursor = utils.db_connect()

        statement = 'INSERT INTO internamento (hora, dia, pacientes_id_pac, fatura_id_fatura, enfermeiro_trabalhadores_id_trab) VALUES (%s, %s, %s, %s, %s) RETURNING id_inter'
        values = (time, date, patient_id, invoice_id, enf_responsavel)

        try:
            cursor.execute(statement, values)
            conn.commit()
            hospitalization_id = cursor.fetchone()[0]
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        
        #create the surgery for the hospitalization
        statement = 'INSERT INTO cirurgia (internamento_id_inter, medico_trabalhadores_id_trab) VALUES (%s, %s) RETURNING id_cirur'
        values = (hospitalization_id, doctor)

        try:
            cursor.execute(statement, values)
            conn.commit()
            surgery_id = cursor.fetchone()[0]

            #add the nurses to the surgery
            for nurse in nurses:
                statement = 'INSERT INTO cirurgia_enfermeiro (cirurgia_id_cirur, enfermeiro_trabalhadores_id_trab) VALUES (%s, %s)'
                values = (surgery_id, nurse[0])
                try:
                    cursor.execute(statement, values)
                    conn.commit()
                    
                    #update the bill for the hospitalization with the surgery cost
                    statement = f"UPDATE fatura SET valor_total = valor_total + 150 WHERE id_fatura = '{invoice_id}'"
                    try:
                        cursor.execute(statement)
                        conn.commit()

                        response = {'results': f"Surgery scheduled for hospitalization {hospitalization_id}"}
                        return flask.make_response(flask.jsonify(response), utils.StatusCodes['success']) 
                    except psycopg2.DatabaseError as e:
                        print(e)
                        conn.rollback()
                        flask.abort(utils.StatusCodes['internal_error'], 'Database error')

                except psycopg2.DatabaseError as e:
                    print(e)
                    conn.rollback()
                    flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            flask.abort(utils.StatusCodes['internal_error'], 'Database error')
        finally:
            utils.db_close(conn, cursor)



    


        

                






if __name__ == '__main__':
    host='127.0.0.1'
    port= 8080
    app.run(host=host, port=port, debug=True, threaded=True)