# app/database/consultas_avanzadas.py

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from app.database.connection import engine

# ==================================================
# FUNCIONES DE CONSULTA
# ==================================================

def tickets_cerrados_por_tecnico():
    """Consulta 1: cantidad de tickets cerrados por técnico"""
    query = text("""
        SELECT u.nombre AS tecnico, COUNT(t.id_ticket) AS total_cerrados
        FROM Ticket t
        JOIN Trabajo tr ON t.id_trabajo = tr.id_trabajo
        JOIN UsuarioSistema u ON tr.id_tecnico = u.id_usuario
        WHERE t.estado = 'Cerrado'
        GROUP BY u.nombre
        ORDER BY total_cerrados DESC
    """)
    df = pd.read_sql_query(query, engine)
    print("\n📊 Tickets cerrados por técnico:\n", df)
    
    # Gráfico de barras
    df.plot(kind='bar', x='tecnico', y='total_cerrados', legend=False)
    plt.title('Tickets cerrados por técnico')
    plt.xlabel('Técnico')
    plt.ylabel('Tickets cerrados')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def distribucion_tickets_por_estado():
    """Consulta 2: distribución de tickets por estado"""
    query = text("""
        SELECT estado, COUNT(*) AS cantidad
        FROM Ticket
        GROUP BY estado
    """)
    df = pd.read_sql_query(query, engine)
    print("\n📊 Distribución de tickets por estado:\n", df)
    
    # Gráfico de pastel
    plt.pie(df['cantidad'], labels=df['estado'], autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de tickets por estado')
    plt.axis('equal')
    plt.show()


def distribucion_tickets_por_prioridad():
    """Consulta 3: distribución de tickets por prioridad"""
    query = text("""
        SELECT prioridad, COUNT(*) AS cantidad
        FROM Ticket
        GROUP BY prioridad
    """)
    df = pd.read_sql_query(query, engine)
    print("\n📊 Distribución de tickets por prioridad:\n", df)

    # Gráfico de pastel
    plt.pie(df['cantidad'], labels=df['prioridad'], autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de tickets por prioridad')
    plt.axis('equal')
    plt.show()


# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================
if __name__ == "__main__":
    print("🚀 Ejecutando consultas avanzadas...\n" + "-"*60)
    tickets_cerrados_por_tecnico()
    distribucion_tickets_por_estado()
    distribucion_tickets_por_prioridad()
    print("-"*60)
    print("✅ Consultas y gráficos generados correctamente.")
