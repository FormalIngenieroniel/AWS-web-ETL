import { render, screen } from '@testing-library/react';
import { act } from 'react';
import App from './App';

test('updates form input fields', async () => {
  await act(async () => {
    render(<App />);
  });

  const nameInput = screen.getByLabelText(/Nombres/i);
  const lastNameInput = screen.getByLabelText(/Apellidos/i);

  expect(nameInput).toBeInTheDocument();
  expect(lastNameInput).toBeInTheDocument();
});

test('renders the user list', async () => {
  // Mock de la respuesta de la API
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () =>
        Promise.resolve([
          { id: 1, nombres: 'Juan', apellidos: 'Pérez', fecha_nacimiento: '1990-01-01' },
          { id: 2, nombres: 'Ana', apellidos: 'García', fecha_nacimiento: '1995-06-15' },
        ]),
    })
  );

  render(<App />);

  // Verificar que los usuarios se muestran correctamente
  const user1 = await screen.findByText(/Juan Pérez/i);
  const user2 = await screen.findByText(/Ana García/i);

  expect(user1).toBeInTheDocument();
  expect(user2).toBeInTheDocument();

  // Restaurar el mock
  global.fetch.mockRestore();
});


test('creates a new user', async () => {
  // Mock de la respuesta de la API para crear usuario
  global.fetch = jest.fn((url, options) =>
    Promise.resolve({
      json: () => Promise.resolve({ id: Date.now() }),
    })
  );

  render(<App />);

  // Llenar el formulario
  fireEvent.change(screen.getByLabelText(/Nombres/i), {
    target: { value: 'Carlos', name: 'nombres' },
  });
  fireEvent.change(screen.getByLabelText(/Apellidos/i), {
    target: { value: 'Martínez', name: 'apellidos' },
  });
  fireEvent.change(screen.getByLabelText(/Fecha de Nacimiento/i), {
    target: { value: '1985-10-10', name: 'fecha_nacimiento' },
  });
  fireEvent.change(screen.getByLabelText(/Contraseña/i), {
    target: { value: 'password123', name: 'password' },
  });

  // Enviar el formulario
  fireEvent.click(screen.getByText(/Crear Usuario/i));

  // Verificar que el fetch fue llamado correctamente
  expect(global.fetch).toHaveBeenCalledWith('http://44.204.188.28:5000/register', expect.objectContaining({
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombres: 'Carlos',
      apellidos: 'Martínez',
      fecha_nacimiento: '1985-10-10',
      password: 'password123'
    })
  }));

  // Restaurar el mock
  global.fetch.mockRestore();
});


test('updates form input fields', () => {
  render(<App />);

  const nameInput = screen.getByLabelText(/Nombres/i);
  const lastNameInput = screen.getByLabelText(/Apellidos/i);
  const birthDateInput = screen.getByLabelText(/Fecha de Nacimiento/i);
  const passwordInput = screen.getByLabelText(/Contraseña/i);

  // Cambiar el valor de los inputs
  fireEvent.change(nameInput, { target: { value: 'Pedro', name: 'nombres' } });
  fireEvent.change(lastNameInput, { target: { value: 'Gómez', name: 'apellidos' } });
  fireEvent.change(birthDateInput, { target: { value: '1992-03-12', name: 'fecha_nacimiento' } });
  fireEvent.change(passwordInput, { target: { value: 'mysecretpassword', name: 'password' } });

  // Verificar que los valores han cambiado correctamente
  expect(nameInput.value).toBe('Pedro');
  expect(lastNameInput.value).toBe('Gómez');
  expect(birthDateInput.value).toBe('1992-03-12');
  expect(passwordInput.value).toBe('mysecretpassword');
});

