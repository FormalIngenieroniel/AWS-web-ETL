from sqlalchemy import text
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos SQL

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:password@172.31.87.146/db'
db = SQLAlchemy(app)

# Definición del modelo de usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(225), nullable=False)

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        nuevo_usuario = Usuario(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            fecha_nacimiento=data['fecha_nacimiento'],
            password=data['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuario registrado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# Ruta para obtener los usuarios registrados
@app.route('/users', methods=['GET'])
def get_users():
    try:
        usuarios = Usuario.query.all()  # Obtiene todos los usuarios
        usuarios_list = [
            {
                "id": usuario.id,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos,
                "fecha_nacimiento": usuario.fecha_nacimiento.strftime('%Y-%m-%d'),
                "password": usuario.password
            }
            for usuario in usuarios
        ]
        return jsonify(usuarios_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/check_db')
def check_db():
    try:
        # Ejecuta una simple consulta para verificar la conexión
        result = db.session.execute(text('SELECT 1'))
        return 'Conexión exitosa a la base de datos'
    except Exception as e:
        return f'Error al conectar a la base de datos: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


