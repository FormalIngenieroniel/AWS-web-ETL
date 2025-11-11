module.exports = {
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],  // Archivo de configuración de pruebas
  testEnvironment: 'jsdom',                             // Ambiente para simular el DOM en las pruebas
  testMatch: ['**/__tests__/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[tj]s?(x)'],  // Dónde buscar los archivos de prueba
};
