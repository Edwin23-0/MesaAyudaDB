# backend/app/database/consultas_sqlalchemy.py

from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.models.models import (
    Cliente, UsuarioSistema, TipoServicio, ServicioCliente,
    TipoProblema, Trabajo, DetalleTrabajo, EquipoInstalado,
    Catalogo, Ticket, Validacion, HistorialTicket
)
import pandas as pd
import matplotlib.pyplot as plt

# Crear sesión
session = Session(bind=engine)

# ========================================
# CONSULTA 1: Total de trabajos por estado
# ========================================
q1 = (
    session.query(Trabajo.estado, func.count(Trabajo.id_trabajo).label("Cantidad"))
    .group_by(Trabajo.estado)
    .order_by(desc("Cantidad"))
)
df1 = pd.read_sql(q1.statement, session.bind)
print("\n1️⃣ Total de trabajos por estado:\n", df1)
df1.plot(kind="bar", x="estado", y="Cantidad", legend=False, title="Trabajos por estado")
plt.show()

# ========================================
# CONSULTA 2: Técnicos con más trabajos realizados
# ========================================
q2 = (
    session.query(UsuarioSistema.nombre.label("Técnico"), func.count(Trabajo.id_trabajo).label("Total_Trabajos"))
    .join(Trabajo, UsuarioSistema.id_usuario == Trabajo.id_tecnico)
    .filter(UsuarioSistema.rol == "tecnico")
    .group_by(UsuarioSistema.nombre)
    .order_by(desc("Total_Trabajos"))
)
df2 = pd.read_sql(q2.statement, session.bind)
print("\n2️⃣ Técnicos con más trabajos realizados:\n", df2)
df2.plot(kind="barh", x="Técnico", y="Total_Trabajos", legend=False, title="Técnicos con más trabajos")
plt.show()

# ========================================
# CONSULTA 3: Promedio de validaciones por supervisor
# ========================================
q3 = (
    session.query(UsuarioSistema.nombre.label("Supervisor"), func.count(Validacion.id_validacion).label("Validaciones"))
    .join(Validacion, UsuarioSistema.id_usuario == Validacion.id_supervisor)
    .filter(UsuarioSistema.rol == "supervisor")
    .group_by(UsuarioSistema.nombre)
)
df3 = pd.read_sql(q3.statement, session.bind)
print("\n3️⃣ Promedio de validaciones por supervisor:\n", df3)
df3.plot(kind="bar", x="Supervisor", y="Validaciones", title="Validaciones por supervisor")
plt.show()

# ========================================
# CONSULTA 4: Tickets por prioridad
# ========================================
q4 = (
    session.query(Ticket.prioridad, func.count(Ticket.id_ticket).label("Cantidad"))
    .group_by(Ticket.prioridad)
)
df4 = pd.read_sql(q4.statement, session.bind)
print("\n4️⃣ Tickets por prioridad:\n", df4)
df4.plot(kind="pie", y="Cantidad", labels=df4["prioridad"], autopct="%1.1f%%", title="Distribución de tickets por prioridad")
plt.ylabel("")
plt.show()

# ========================================
# CONSULTA 5: Tipos de problema más comunes
# ========================================
q5 = (
    session.query(TipoProblema.nombre.label("Tipo_Problema"), func.count(Trabajo.id_trabajo).label("Frecuencia"))
    .join(Trabajo, TipoProblema.id_tipo == Trabajo.id_tipo)
    .group_by(TipoProblema.nombre)
    .order_by(desc("Frecuencia"))
)
df5 = pd.read_sql(q5.statement, session.bind)
print("\n5️⃣ Tipos de problema más comunes:\n", df5)
df5.plot(kind="bar", x="Tipo_Problema", y="Frecuencia", title="Tipos de problema más comunes")
plt.show()

# ========================================
# CONSULTA 6: Clientes con más servicios activos
# ========================================
q6 = (
    session.query(Cliente.nombre.label("Cliente"), func.count(ServicioCliente.id_servicio).label("Servicios_Activos"))
    .join(ServicioCliente, Cliente.id_cliente == ServicioCliente.id_cliente)
    .filter(ServicioCliente.estado == "Activo")
    .group_by(Cliente.nombre)
    .order_by(desc("Servicios_Activos"))
)
df6 = pd.read_sql(q6.statement, session.bind)
print("\n6️⃣ Clientes con más servicios activos:\n", df6)
df6.plot(kind="barh", x="Cliente", y="Servicios_Activos", title="Clientes con más servicios activos")
plt.show()

# ========================================
# CONSULTA 7: Promedio de trabajos por técnico
# ========================================
q7 = (
    session.query(func.avg(func.count(Trabajo.id_trabajo)))
    .join(UsuarioSistema, UsuarioSistema.id_usuario == Trabajo.id_tecnico)
    .group_by(UsuarioSistema.id_usuario)
)
promedio_trabajos = session.execute(q7.statement).scalar()
print(f"\n7️⃣ Promedio de trabajos por técnico: {promedio_trabajos:.2f}")

# ========================================
# CONSULTA 8: Estados más frecuentes en historial de tickets
# ========================================
q8 = (
    session.query(HistorialTicket.estado_nuevo, func.count(HistorialTicket.id_historial).label("Frecuencia"))
    .group_by(HistorialTicket.estado_nuevo)
    .order_by(desc("Frecuencia"))
)
df8 = pd.read_sql(q8.statement, session.bind)
print("\n8️⃣ Estados más frecuentes en historial de tickets:\n", df8)
df8.plot(kind="bar", x="estado_nuevo", y="Frecuencia", title="Estados más frecuentes en historial")
plt.show()

# ========================================
# CONSULTA 9: Equipos instalados por modelo
# ========================================
q9 = (
    session.query(EquipoInstalado.modelo, func.count(EquipoInstalado.id_equipo).label("Cantidad"))
    .group_by(EquipoInstalado.modelo)
)
df9 = pd.read_sql(q9.statement, session.bind)
print("\n9️⃣ Equipos instalados por modelo:\n", df9)
df9.plot(kind="bar", x="modelo", y="Cantidad", title="Equipos instalados por modelo")
plt.show()

# ========================================
# CONSULTA 10: Porcentaje de tickets validados exitosamente
# ========================================
total_validaciones = session.query(func.count(Validacion.id_validacion)).scalar()
exitosas = session.query(func.count(Validacion.id_validacion)).filter(Validacion.resultado == True).scalar()
porcentaje = (exitosas / total_validaciones * 100) if total_validaciones > 0 else 0
print(f"\n🔟 Porcentaje de validaciones exitosas: {porcentaje:.2f}%")

# Cerrar sesión
session.close()
print("\n✅ Todas las consultas se ejecutaron correctamente.")
