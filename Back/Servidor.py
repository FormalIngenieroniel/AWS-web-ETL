from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa CORS
from datetime import datetime

# Inicializa la instancia de SQLAlchemy, pero sin conectarla aún a la app
db = SQLAlchemy()

# Modelo de Usuario que representa la tabla en la base de datos
class Usuario(db.Model):
    """
    Modelo que representa un Usuario en la base de datos.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        apellidos (str): Apellido del usuario.
        fecha_nacimiento (date): Fecha de nacimiento del usuario.
        password (str): Contraseña del usuario.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(225), nullable=False)

def create_test_app():
    """
    Crea y configura una aplicación Flask para realizar pruebas unitarias.

    Configura una base de datos SQLite en memoria y prepara las rutas necesarias
    para las pruebas de operaciones CRUD sobre usuarios.

    Retorna:
        Flask: La aplicación configurada para pruebas.
    """
    app = Flask(__name__)
    
    # Configuraciones para pruebas (base de datos en memoria)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Crea todas las tablas necesarias para las pruebas
    
    # Configura CORS
    CORS(app)
    
    # Rutas CRUD (similares a las anteriores)
    @app.route('/register', methods=['POST'])
    def create_usuario():
        data = request.get_json()
        # Convertir fecha_nacimiento a datetime.date
        fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            fecha_nacimiento=fecha_nacimiento,
            password=data['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    @app.route('/users', methods=['GET'])
    def get_usuarios():
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'nombre': u.nombre,
            'apellidos': u.apellidos,
            'fecha_nacimiento': u.fecha_nacimiento.isoformat(),  # Convert date to string
            'password': u.password
        } for u in usuarios])
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
