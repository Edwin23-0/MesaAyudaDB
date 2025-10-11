# backend/app/models.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect

Base = declarative_base()

# -------------------------
# Tabla: Cliente
# -------------------------
class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(200))


# -------------------------
# Tabla: UsuarioSistema
# -------------------------
class UsuarioSistema(Base):
    __tablename__ = "UsuarioSistema"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100))
    telefono = Column(String(20))
    rol = Column(String(50))           # tecnico, supervisor, admin
    especialidad = Column(String(100)) # opcional, solo para técnicos


# -------------------------
# Tabla: TipoServicio
# -------------------------
class TipoServicio(Base):
    __tablename__ = "TipoServicio"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


# -------------------------
# Tabla: ServicioCliente
# -------------------------
class ServicioCliente(Base):
    __tablename__ = "ServicioCliente"

    id_servicio = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("TipoServicio.id_tipo"), nullable=False)
    fecha_inicio = Column(Date)
    estado = Column(String(50))


# -------------------------
# Tabla: TipoProblema
# -------------------------
class TipoProblema(Base):
    __tablename__ = "TipoProblema"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


# -------------------------
# Tabla: Trabajo
# -------------------------
class Trabajo(Base):
    __tablename__ = "Trabajo"

    id_trabajo = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"), nullable=False)
    id_tecnico = Column(Integer, ForeignKey("UsuarioSistema.id_usuario"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("TipoProblema.id_tipo"), nullable=False)
    fecha_creacion = Column(DateTime)
    estado = Column(String(50))
    tipo_problema = Column(String(100))  # redundante para consultas rápidas


# -------------------------
# Tabla: DetalleTrabajo
# -------------------------
class DetalleTrabajo(Base):
    __tablename__ = "DetalleTrabajo"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_trabajo = Column(Integer, ForeignKey("Trabajo.id_trabajo"), nullable=False)
    tipo = Column(String(50))
    descripcion = Column(Text)


# -------------------------
# Tabla: EquipoInstalado
# -------------------------
class EquipoInstalado(Base):
    __tablename__ = "EquipoInstalado"

    id_equipo = Column(Integer, primary_key=True, autoincrement=True)
    id_trabajo = Column(Integer, ForeignKey("Trabajo.id_trabajo"), nullable=False)
    modelo = Column(String(100))
    serie = Column(String(100))
    fecha_instalacion = Column(Date)


# -------------------------
# Tabla: Catalogo
# -------------------------
class Catalogo(Base):
    __tablename__ = "Catalogo"

    id_catalogo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    tipo = Column(String(50))  # problemas, categorías, motivos_cierre
    creado_por = Column(Integer, ForeignKey("UsuarioSistema.id_usuario"))


# -------------------------
# Tabla: Ticket
# -------------------------
class Ticket(Base):
    __tablename__ = "Ticket"

    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    id_trabajo = Column(Integer, ForeignKey("Trabajo.id_trabajo"), nullable=False)
    creado_por = Column(Integer, ForeignKey("UsuarioSistema.id_usuario"), nullable=False)
    id_catalogo = Column(Integer, ForeignKey("Catalogo.id_catalogo"), nullable=False)
    fecha_creado = Column(DateTime)
    estado = Column(String(50))
    prioridad = Column(String(20))  # alta, media, baja


# -------------------------
# Tabla: Validacion
# -------------------------
class Validacion(Base):
    __tablename__ = "Validacion"

    id_validacion = Column(Integer, primary_key=True, autoincrement=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id_ticket"), nullable=False)
    id_supervisor = Column(Integer, ForeignKey("UsuarioSistema.id_usuario"), nullable=False)
    fecha_validacion = Column(DateTime)
    resultado = Column(Boolean)
    observaciones = Column(Text)


# -------------------------
# Tabla: HistorialTicket
# -------------------------
class HistorialTicket(Base):
    __tablename__ = "HistorialTicket"

    id_historial = Column(Integer, primary_key=True, autoincrement=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id_ticket"), nullable=False)
    fecha = Column(DateTime)
    estado_anterior = Column(String(50))
    estado_nuevo = Column(String(50))
    comentario = Column(Text)


# -------------------------
# Helper: serializar instancias a dict
# -------------------------
def to_dict(instance):
    """
    Convierte una instancia de modelo SQLAlchemy a diccionario plano.
    Útil para jsonify en endpoints.
    """
    return {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}
