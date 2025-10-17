# backend/app/database/consultas_sqlalchemy.py
# -------------------------------------------------------------
#  Consultas analíticas del proyecto Mesa de Ayuda (versión estable)
#  Traducción fiel de las 10 consultas SQL originales
#  Compatible con SQL Server (pyodbc + SQLAlchemy)
# -------------------------------------------------------------

from sqlalchemy import func, desc, distinct, case, over, text
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.models.models import (
    Cliente, UsuarioSistema, Trabajo, ServicioCliente,
    Validacion, Ticket, Catalogo, HistorialTicket
)
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# Función auxiliar definitiva para DATEDIFF SQL Server
# =====================================================
def datediff_days(col1, col2):
    """Usa DATEDIFF(day, col1, col2) sin parámetros en SQL Server"""
    return func.datediff(text("day"), col1, col2)

# =====================================================
# Helper para mostrar y graficar sin errores
# =====================================================
def mostrar_y_graficar(df, titulo, tipo="bar", x=None, y=None):
    print(f"\n{titulo}:\n", df)
    if not df.empty and y in df.columns:
        df.plot(kind=tipo, x=x, y=y, title=titulo)
        plt.show()
    else:
        print(f"⚠️ No hay datos para mostrar en '{titulo}' (DataFrame vacío o sin columnas numéricas)\n")

# Crear sesión
session = Session(bind=engine)
print("\n===================== CONSULTAS ANALÍTICAS =====================\n")

# =====================================================
# 1️⃣ Promedio de días por técnico
# =====================================================
q1 = (
    session.query(
        UsuarioSistema.nombre.label("Tecnico"),
        func.count(Trabajo.id_trabajo).label("Total_Trabajos"),
        func.avg(datediff_days(Trabajo.fecha_creacion, func.getdate())).label("Promedio_Dias_Trabajo")
    )
    .join(Trabajo, UsuarioSistema.id_usuario == Trabajo.id_tecnico)
    .filter(UsuarioSistema.rol == "tecnico")
    .group_by(UsuarioSistema.nombre)
    .order_by("Promedio_Dias_Trabajo")
)
df1 = pd.read_sql(q1.statement, session.bind)
mostrar_y_graficar(df1, "1️⃣ Promedio de días por técnico", tipo="bar", x="Tecnico", y="Promedio_Dias_Trabajo")

# =====================================================
# 2️⃣ Técnicos con más de 5 trabajos asignados
# =====================================================
q2 = (
    session.query(
        UsuarioSistema.nombre.label("Tecnico"),
        func.count(Trabajo.id_trabajo).label("Total_Trabajos")
    )
    .join(Trabajo, UsuarioSistema.id_usuario == Trabajo.id_tecnico)
    .filter(UsuarioSistema.rol == "tecnico")
    .group_by(UsuarioSistema.nombre)
    .having(func.count(Trabajo.id_trabajo) > 5)
    .order_by(desc("Total_Trabajos"))
)
df2 = pd.read_sql(q2.statement, session.bind)
mostrar_y_graficar(df2, "2️⃣ Técnicos con más de 5 trabajos asignados", tipo="barh", x="Tecnico", y="Total_Trabajos")

# =====================================================
# 3️⃣ Clientes con más de un tipo de servicio activo
# =====================================================
q3 = (
    session.query(
        Cliente.nombre.label("Cliente"),
        func.count(distinct(ServicioCliente.id_tipo)).label("Tipos_Servicio_Activos")
    )
    .join(ServicioCliente, Cliente.id_cliente == ServicioCliente.id_cliente)
    .filter(ServicioCliente.estado == "activo")
    .group_by(Cliente.nombre)
    .having(func.count(distinct(ServicioCliente.id_tipo)) > 1)
)
df3 = pd.read_sql(q3.statement, session.bind)
mostrar_y_graficar(df3, "3️⃣ Clientes con más de un tipo de servicio activo", x="Cliente", y="Tipos_Servicio_Activos")

# =====================================================
# 4️⃣ Promedio de validaciones por supervisor
# =====================================================
q4 = (
    session.query(
        UsuarioSistema.nombre.label("Supervisor"),
        func.count(Validacion.id_validacion).label("Total_Validaciones"),
        (func.avg(case((Validacion.resultado == 1, 1), else_=0)) * 100).label("Porcentaje_Aprobadas")
    )
    .join(Validacion, UsuarioSistema.id_usuario == Validacion.id_supervisor)
    .filter(UsuarioSistema.rol == "supervisor")
    .group_by(UsuarioSistema.nombre)
    .order_by(desc("Porcentaje_Aprobadas"))
)
df4 = pd.read_sql(q4.statement, session.bind)
mostrar_y_graficar(df4, "4️⃣ Promedio de validaciones por supervisor", x="Supervisor", y="Porcentaje_Aprobadas")

# =====================================================
# 5️⃣ Top 5 clientes con más tickets creados
# =====================================================
q5 = (
    session.query(
        Cliente.nombre.label("Cliente"),
        func.count(Ticket.id_ticket).label("Total_Tickets")
    )
    .join(Trabajo, Ticket.id_trabajo == Trabajo.id_trabajo)
    .join(Cliente, Trabajo.id_cliente == Cliente.id_cliente)
    .group_by(Cliente.nombre)
    .order_by(desc("Total_Tickets"))
    .limit(5)
)
df5 = pd.read_sql(q5.statement, session.bind)
mostrar_y_graficar(df5, "5️⃣ Top 5 clientes con más tickets creados", tipo="barh", x="Cliente", y="Total_Tickets")

# =====================================================
# 6️⃣ Tickets con más de 3 cambios de estado
# =====================================================
q6 = (
    session.query(
        Ticket.id_ticket,
        func.count(HistorialTicket.id_historial).label("Total_Cambios_Estado")
    )
    .join(HistorialTicket, Ticket.id_ticket == HistorialTicket.id_ticket)
    .group_by(Ticket.id_ticket)
    .having(func.count(HistorialTicket.id_historial) > 3)
    .order_by(desc("Total_Cambios_Estado"))
)
df6 = pd.read_sql(q6.statement, session.bind)
mostrar_y_graficar(df6, "6️⃣ Tickets con más de 3 cambios de estado", x="id_ticket", y="Total_Cambios_Estado")

# =====================================================
# 7️⃣ Tiempo promedio entre creación y validación de tickets
# =====================================================
q7 = (
    session.query(
        func.avg(datediff_days(Ticket.fecha_creado, Validacion.fecha_validacion)).label("Promedio_Dias_Validacion")
    )
    .join(Validacion, Ticket.id_ticket == Validacion.id_ticket)
)
df7 = pd.read_sql(q7.statement, session.bind)
print("\n7️⃣ Promedio de días entre creación y validación:\n", df7)

# =====================================================
# 8️⃣ Catálogos más usados en tickets
# =====================================================
q8 = (
    session.query(
        Catalogo.nombre.label("Catalogo"),
        func.count(Ticket.id_ticket).label("Veces_Usado")
    )
    .join(Catalogo, Ticket.id_catalogo == Catalogo.id_catalogo)
    .group_by(Catalogo.nombre)
    .order_by(desc("Veces_Usado"))
)
df8 = pd.read_sql(q8.statement, session.bind)
mostrar_y_graficar(df8, "8️⃣ Catálogos más usados en tickets", x="Catalogo", y="Veces_Usado")

# =====================================================
# 9️⃣ Supervisores con más validaciones exitosas
# =====================================================
sub_validaciones = (
    session.query(
        Validacion.id_supervisor,
        func.count(Validacion.id_validacion).label("Validaciones_Exitosas")
    )
    .filter(Validacion.resultado == 1)
    .group_by(Validacion.id_supervisor)
    .subquery()
)

q9 = (
    session.query(
        UsuarioSistema.nombre.label("Supervisor"),
        func.coalesce(sub_validaciones.c.Validaciones_Exitosas, 0).label("Validaciones_Exitosas")
    )
    .outerjoin(sub_validaciones, UsuarioSistema.id_usuario == sub_validaciones.c.id_supervisor)
    .filter(UsuarioSistema.rol == "supervisor")
    .order_by(desc("Validaciones_Exitosas"))
)
df9 = pd.read_sql(q9.statement, session.bind)
mostrar_y_graficar(df9, "9️⃣ Supervisores con más validaciones exitosas", tipo="barh", x="Supervisor", y="Validaciones_Exitosas")

# =====================================================
# 🔟 Ranking de técnicos por eficiencia (CTE + RANK)
# =====================================================
cte = (
    session.query(
        UsuarioSistema.id_usuario.label("id_usuario"),
        UsuarioSistema.nombre.label("Tecnico"),
        func.count(Trabajo.id_trabajo).label("Total_Trabajos"),
        func.avg(datediff_days(Trabajo.fecha_creacion, func.getdate())).label("Promedio_Dias")
    )
    .join(Trabajo, UsuarioSistema.id_usuario == Trabajo.id_tecnico)
    .filter(UsuarioSistema.rol == "tecnico")
    .group_by(UsuarioSistema.id_usuario, UsuarioSistema.nombre)
    .cte("Eficiencia")
)

q10 = (
    session.query(
        cte.c.Tecnico,
        cte.c.Total_Trabajos,
        cte.c.Promedio_Dias,
        over(
            func.rank(),
            order_by=(desc(cte.c.Total_Trabajos), cte.c.Promedio_Dias)
        ).label("Ranking_Eficiencia")
    )
)
df10 = pd.read_sql(q10.statement, session.bind)
mostrar_y_graficar(df10, "🔟 Ranking de técnicos por eficiencia", x="Tecnico", y="Ranking_Eficiencia")

# Cerrar sesión
session.close()
print("\n✅ Todas las consultas analíticas se ejecutaron correctamente.\n")
