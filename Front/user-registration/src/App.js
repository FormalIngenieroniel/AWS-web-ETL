import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({
    nombres: '',
    apellidos: '',
    fecha_nacimiento: '',
    password: ''
  });

  useEffect(() => {
    fetch('http://44.204.188.28:5000/users')
      .then(response => response.json())
      .then(data => setUsers(data))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setNewUser({ ...newUser, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    fetch('http://44.204.188.28:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newUser),
    })
    .then(response => response.json())
    .then(data => {
      const createdUser = {
        ...newUser,
        id: Date.now()
      };
      setUsers([...users, createdUser]);
      setNewUser({
        nombres: '',
        apellidos: '',
        fecha_nacimiento: '',
        password: ''
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Lista de Usuarios</h1>
      </div>
      <ul className="user-list">
        {users.map((user) => (
          <li key={user.id}>
            <span>{user.nombres} {user.apellidos} - {user.fecha_nacimiento}</span>
          </li>
        ))}
      </ul>

      <h2>Crear un nuevo usuario</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Nombres:
          <input
            type="text"
            name="nombres"
            value={newUser.nombres}
            onChange={handleInputChange}
            required
          />
        </label>
        <label>
          Apellidos:
          <input
            type="text"
            name="apellidos"
            value={newUser.apellidos}
            onChange={handleInputChange}
            required
          />
        </label>
        <label>
          Fecha de Nacimiento:
          <input
            type="date"
            name="fecha_nacimiento"
            value={newUser.fecha_nacimiento}
            onChange={handleInputChange}
            required
          />
        </label>
        <label>
          Contraseña:
          <input
            type="password"
            name="password"
            value={newUser.password}
            onChange={handleInputChange}
            required
          />
        </label>
        <button type="submit">Crear Usuario</button>
      </form>
    </div>
  );
}

export default App;
