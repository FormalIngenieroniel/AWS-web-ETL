import pytest
from Servidor import create_test_app, db, Usuario

@pytest.fixture
def client():
    """
    Fixture que configura el cliente de pruebas para la aplicación.

    Retorna:
        client (FlaskClient): Cliente de pruebas para realizar solicitudes a la aplicación.
    """
    app = create_test_app()

    # Abre el cliente de pruebas
    with app.test_client() as client:
        # Contexto de aplicación para operaciones con la base de datos
        with app.app_context():
            db.create_all()  # Crea todas las tablas necesarias
        yield client  # Lo que se devuelva aquí estará disponible en las pruebas
        # Limpiar la base de datos después de cada prueba
        with app.app_context():
            db.drop_all()  # Elimina todas las tablas al finalizar las pruebas

# Prueba para crear un usuario
def test_create_usuario(client):
    """
    Prueba para verificar la creación de un usuario.

    Parámetros:
        client (FlaskClient): Cliente de pruebas.
    
    Verifica:
        - Que el código de estado sea 201.
        - Que el mensaje de éxito sea el esperado.
    """
    response = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Verificaciones
    assert response.status_code == 201
    assert response.get_json()['mensaje'] == 'Usuario creado exitosamente'

# Prueba para obtener todos los usuarios
def test_get_usuarios(client):
    """
    Prueba para verificar la obtención de todos los usuarios.

    Parámetros:
        client (FlaskClient): Cliente de pruebas.
    
    Verifica:
        - Que la lista de usuarios tenga al menos un elemento.
        - Que el usuario devuelto tenga el nombre correcto.
    """
    # Primero, se crea un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, se verifica la lista de usuarios
    response = client.get('/usuarios')
    
    # Verificaciones
    assert response.status_code == 200
    usuarios = response.get_json()
    assert len(usuarios) == 1
    assert usuarios[0]['nombre'] == 'Juan'

# Prueba para obtener un usuario específico
def test_get_usuario(client):
    """
    Prueba para verificar la obtención de un usuario por ID.

    Parámetros:
        client (FlaskClient): Cliente de pruebas.
    
    Verifica:
        - Que el código de estado sea 200.
        - Que el nombre del usuario devuelto sea correcto.
    """
    # Primero, se crea un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, se obtiene el usuario por su ID
    response = client.get('/usuarios/1')
    
    # Verificaciones
    assert response.status_code == 200
    usuario = response.get_json()
    assert usuario['nombre'] == 'Juan'

# Prueba para actualizar un usuario
def test_update_usuario(client):
    """
    Prueba para verificar la actualización de un usuario.

    Parámetros:
        client (FlaskClient): Cliente de pruebas.
    
    Verifica:
        - Que el código de estado sea 200.
        - Que el mensaje de éxito sea el esperado.
    """
    # Primero, se crea un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, se actualiza el usuario
    response = client.put('/usuarios/1', json={
        'nombre': 'Juan actualizado',
        'apellido': 'Pérez actualizado',
        'fechaNacimiento': '1990-01-01',
        'password': 'newpassword123'
    })
    
    # Verificaciones
    assert response.status_code == 200
    assert response.get_json()['mensaje'] == 'Usuario actualizado exitosamente'

# Prueba para eliminar un usuario
def test_delete_usuario(client):
    """
    Prueba para verificar la eliminación de un usuario.

    Parámetros:
        client (FlaskClient): Cliente de pruebas.
    
    Verifica:
        - Que el código de estado sea 204 al eliminar correctamente un usuario.
    """
    # Primero, se crea un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, se elimina el usuario
    response = client.delete('/usuarios/1')
    
    # Verificaciones
    assert response.status_code == 204
