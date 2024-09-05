from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Configurar la conexión con MySQL
# Reemplaza usuario, password y db con tus valores
engine = create_engine('mysql+pymysql://usuario:password@localhost/db')

# Crear la base declarativa usando SQLAlchemy 2.0
Base = declarative_base()

# Definir la tabla 'usuarios'
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    password = Column(String(255), nullable=False)

# Crear todas las tablas (si no existen)
Base.metadata.create_all(engine)
