from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from app.database.connection import Base

# 🧍‍♂️ Tabla Cliente
class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(200))


# 👨‍💻 Tabla UsuarioSistema
class UsuarioSistema(Base):
    __tablename__ = "UsuarioSistema"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    rol = Column(String(50))          # técnico, supervisor, admin
    especialidad = Column(String(100))  # opcional, solo para técnicos


# 🧾 Tabla TipoServicio
class TipoServicio(Base):
    __tablename__ = "TipoServicio"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


# 🧍‍♂️ Tabla Cliente
class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(200))


# 👨‍💻 Tabla UsuarioSistema
class UsuarioSistema(Base):
    __tablename__ = "UsuarioSistema"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    rol = Column(String(50))
    especialidad = Column(String(100))


# 🧾 Tabla TipoServicio
class TipoServicio(Base):
    __tablename__ = "TipoServicio"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


# 📦 Tabla ServicioCliente
class ServicioCliente(Base):
    __tablename__ = "ServicioCliente"

    id_servicio = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("TipoServicio.id_tipo"), nullable=False)
    fecha_inicio = Column(Date)
    estado = Column(String(50))


# ⚙️ Tabla TipoProblema
class TipoProblema(Base):
    __tablename__ = "TipoProblema"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


# 🔧 Tabla Trabajo
class Trabajo(Base):
    __tablename__ = "Trabajo"

    id_trabajo = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"), nullable=False)
    id_tecnico = Column(Integer, ForeignKey("UsuarioSistema.id_usuario"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("TipoProblema.id_tipo"), nullable=False)
    fecha_creacion = Column(DateTime)
    estado = Column(String(50))
    tipo_problema = Column(String(100))  # redundante para consultas rápidas
