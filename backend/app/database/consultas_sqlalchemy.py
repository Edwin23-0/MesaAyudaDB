# backend/app/database/consultas_sqlalchemy.py
# -------------------------------------------------------------
#  Consultas analíticas del proyecto Mesa de Ayuda (versión final)
#  Ejecuta 10 consultas SQL con SQLAlchemy + Pandas + Matplotlib
#  Guarda cada gráfico como imagen PNG en la carpeta /graficos_consultas
# -------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import func, desc, distinct, case, over, text
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.models.models import (
    Cliente, UsuarioSistema, Trabajo, ServicioCliente,
    Validacion, Ticket, Catalogo, HistorialTicket
)

# =====================================================
# Función auxiliar definitiva para DATEDIFF SQL Server
# =====================================================
def datediff_days(col1, col2):
    """Usa DATEDIFF(day, col1, col2) sin parámetros en SQL Server"""
    return func.datediff(text("day"), col1, col2)

# =====================================================
# Crear carpeta para guardar gráficos
# =====================================================
output_dir = os.path.join(os.path.dirname(__file__), "../../graficos_consultas")
os.makedirs(output_dir, exist_ok=True)

# =====================================================
# Helpers para mostrar/guardar gráficos (incluye placeholders)
# =====================================================
def save_placeholder(filename, title, subtitle):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    ax.text(0.5, 0.6, title, ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(0.5, 0.4, subtitle, ha="center", va="center", fontsize=11, color="#555")
    plt.tight_layout()
    path = os.path.join(output_dir, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"⚠️ {subtitle} | Imagen guardada como placeholder en: {path}\n")

def mostrar_y_guardar(df, titulo, archivo, tipo="bar", x=None, y=None):
    print(f"\n{titulo}:\n", df)
    path = os.path.join(output_dir, archivo)
    if not df.empty and (y is None or y in df.columns):
        ax = df.plot(kind=tipo, x=x, y=y, title=titulo, figsize=(8, 5))
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"✅ Gráfico guardado en: {path}\n")
    else:
        save_placeholder(archivo, titulo, "Sin datos para graficar")

def guardar_valor_unico(valor, titulo, archivo, etiqueta="Promedio (días)"):
    path = os.path.join(output_dir, archivo)
    if valor is not None:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar([etiqueta], [valor])
        ax.set_title(titulo)
        ax.set_ylim(0, max(valor * 1.2, 1))  # margen visual
        for i, v in enumerate([valor]):
            ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"✅ Gráfico guardado en: {path}\n")
    else:
        save_placeholder(archivo, titulo, "Sin datos para calcular promedio")

# =====================================================
# Iniciar sesión de base de datos
# =====================================================
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
mostrar_y_guardar(df1, "1️⃣ Promedio de días por técnico", "consulta_1.png", tipo="bar", x="Tecnico", y="Promedio_Dias_Trabajo")

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
mostrar_y_guardar(df2, "2️⃣ Técnicos con más de 5 trabajos asignados", "consulta_2.png", tipo="barh", x="Tecnico", y="Total_Trabajos")

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
mostrar_y_guardar(df3, "3️⃣ Clientes con más de un tipo de servicio activo", "consulta_3.png", tipo="bar", x="Cliente", y="Tipos_Servicio_Activos")

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
mostrar_y_guardar(df4, "4️⃣ Promedio de validaciones por supervisor", "consulta_4.png", tipo="bar", x="Supervisor", y="Porcentaje_Aprobadas")

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
mostrar_y_guardar(df5, "5️⃣ Top 5 clientes con más tickets creados", "consulta_5.png", tipo="barh", x="Cliente", y="Total_Tickets")

# =====================================================
# 6️⃣ Tickets con más de 3 cambios de estado (SIEMPRE guarda imagen)
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
if df6.empty:
    save_placeholder("consulta_6.png", "6️⃣ Tickets con más de 3 cambios de estado", "Sin registros (>3 cambios)")
else:
    mostrar_y_guardar(df6, "6️⃣ Tickets con más de 3 cambios de estado", "consulta_6.png", tipo="bar", x="id_ticket", y="Total_Cambios_Estado")

# =====================================================
# 7️⃣ Tiempo promedio entre creación y validación de tickets (SIEMPRE guarda imagen)
# =====================================================
q7 = (
    session.query(
        func.avg(datediff_days(Ticket.fecha_creado, Validacion.fecha_validacion)).label("Promedio_Dias_Validacion")
    )
    .join(Validacion, Ticket.id_ticket == Validacion.id_ticket)
)
df7 = pd.read_sql(q7.statement, session.bind)
print("\n7️⃣ Promedio de días entre creación y validación:\n", df7)
promedio_val = None
if not df7.empty and "Promedio_Dias_Validacion" in df7.columns:
    val = df7["Promedio_Dias_Validacion"].iloc[0]
    # Manejo de None/NaN
    if pd.notnull(val):
        promedio_val = float(val)

guardar_valor_unico(promedio_val, "7️⃣ Promedio de días entre creación y validación", "consulta_7.png", etiqueta="Promedio (días)")

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
mostrar_y_guardar(df8, "8️⃣ Catálogos más usados en tickets", "consulta_8.png", tipo="bar", x="Catalogo", y="Veces_Usado")

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
mostrar_y_guardar(df9, "9️⃣ Supervisores con más validaciones exitosas", "consulta_9.png", tipo="barh", x="Supervisor", y="Validaciones_Exitosas")

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
mostrar_y_guardar(df10, "🔟 Ranking de técnicos por eficiencia", "consulta_10.png", tipo="bar", x="Tecnico", y="Ranking_Eficiencia")

# Cerrar sesión
session.close()
print(f"\n✅ Todas las consultas ejecutadas correctamente. Las imágenes se guardaron en:\n📁 {output_dir}\n")
