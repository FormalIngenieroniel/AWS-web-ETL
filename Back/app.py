import os
import sqlite3
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(_name_)

# Configuración de CORS
CORS(app, resources={r"/*": {"origins": "http://ec2-3-86-153-248.compute-1.amazonaws.com:3000"}})

def get_db_connection():
    if os.getenv('FLASK_ENV') == 'testing':
        # Usar SQLite en memoria para pruebas
        conn = sqlite3.connect(':memory:')
        return conn
    else:
        # Conectar a RDS MySQL en producción (Sakila)
        conn = mysql.connector.connect(
            host='database-2.c99cmwwsyi8p.us-east-1.rds.amazonaws.com',  # Cambia al endpoint RDS
            user='main',  # Reemplaza con tu usuario
            password='Lucas3044.',  # Reemplaza con tu contraseña
            database='sakila'  # Usar la base de datos Sakila
        )
        return conn

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Usar diferentes marcadores de posición para SQLite y MySQL
    query = 'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)'

    try:
        cursor.execute(query, (nombre_usuario, correo, contrasena))
        conn.commit()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to add user'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre_usuario, correo FROM table1')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Convertir los datos a un formato de diccionario
    users = [{'id': row[0], 'nombre_usuario': row[1], 'correo': row[2]} for row in rows]
    return jsonify(users)

@app.route('/add_rental', methods=['POST'])
def add_rental():
    data = request.get_json()
    customer_id = data.get('customer_id')
    film_id = data.get('film_id')
    rental_date = data.get('rental_date')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar la renta en la tabla rental de Sakila
    query = '''
    INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, return_date)
    VALUES (%s, (SELECT inventory_id FROM inventory WHERE film_id = %s LIMIT 1), %s, 1, NULL)
    '''

    try:
        cursor.execute(query, (rental_date, film_id, customer_id))
        conn.commit()
        return jsonify({'message': 'Rental added successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to add rental'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT customer_id, first_name, last_name, email FROM customer')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir los datos a un formato de diccionario
    customers = [{'customer_id': row[0], 'first_name': row[1], 'last_name': row[2], 'email': row[3]} for row in rows]
    return jsonify(customers)

@app.route('/films', methods=['GET'])
def get_films():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT film_id, title FROM film')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir los datos a un formato de diccionario
    films = [{'film_id': row[0], 'title': row[1]} for row in rows]
    return jsonify(films)

if _name_ == '_main_':
    app.run(port=5000, host='0.0.0.0', debug=True)
