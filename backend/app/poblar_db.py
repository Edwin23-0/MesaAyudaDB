import random
from datetime import timedelta
from faker import Faker
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.models.models import (
    Cliente, UsuarioSistema, TipoServicio, ServicioCliente, TipoProblema,
    Trabajo, DetalleTrabajo, EquipoInstalado, Catalogo, Ticket,
    Validacion, HistorialTicket
)

fake = Faker('es_CO')

def poblar_datos():
    with Session(engine) as session:
        try:
            print("🚀 Iniciando poblamiento de la base de datos...\n" + "-"*70)

            # ==================================================
            # 1️⃣ CLIENTES
            # ==================================================
            clientes = [
                Cliente(
                    nombre=fake.name(),
                    email=fake.email(),
                    telefono=fake.phone_number(),
                    direccion=fake.address()
                )
                for _ in range(30)
            ]
            session.add_all(clientes)
            session.commit()
            print(f"👥 Clientes insertados: {len(clientes)}")

            # ==================================================
            # 2️⃣ USUARIOS DEL SISTEMA
            # ==================================================
            roles = ["Técnico", "Supervisor", "Administrador"]
            usuarios = [
                UsuarioSistema(
                    nombre=fake.name(),
                    email=fake.email(),
                    telefono=fake.phone_number(),
                    rol=random.choice(roles),
                    especialidad=random.choice(["Redes", "Software", "Hardware", "Soporte"])
                )
                for _ in range(15)
            ]
            session.add_all(usuarios)
            session.commit()
            print(f"👨‍💻 Usuarios del sistema insertados: {len(usuarios)}")

            # ==================================================
            # 3️⃣ TIPO DE SERVICIO
            # ==================================================
            tipos_servicio = [
                TipoServicio(nombre=n, descripcion=fake.sentence())
                for n in ["Instalación", "Mantenimiento", "Reparación", "Actualización"]
            ]
            session.add_all(tipos_servicio)
            session.commit()
            print(f"⚙️ Tipos de servicio insertados: {len(tipos_servicio)}")

            # ==================================================
            # 4️⃣ SERVICIOS CLIENTE
            # ==================================================
            servicios_cliente = [
                ServicioCliente(
                    id_cliente=random.choice(clientes).id_cliente,
                    id_tipo=random.choice(tipos_servicio).id_tipo,
                    fecha_inicio=fake.date_between(start_date='-120d', end_date='today'),
                    estado=random.choice(["Activo", "Suspendido", "Finalizado"])
                )
                for _ in range(50)
            ]
            session.add_all(servicios_cliente)
            session.commit()
            print(f"📋 ServiciosCliente insertados: {len(servicios_cliente)}")

            # ==================================================
            # 5️⃣ TIPO DE PROBLEMA
            # ==================================================
            tipos_problema = [
                TipoProblema(nombre=n, descripcion=fake.text())
                for n in ["Conectividad", "Rendimiento", "Seguridad", "Configuración", "Error de Software"]
            ]
            session.add_all(tipos_problema)
            session.commit()
            print(f"🧩 Tipos de problema insertados: {len(tipos_problema)}")

            # ==================================================
            # 6️⃣ TRABAJOS
            # ==================================================
            trabajos = []
            for _ in range(80):
                cliente = random.choice(clientes)
                tecnico = random.choice([u for u in usuarios if u.rol == "Técnico"])
                tipo_prob = random.choice(tipos_problema)

                trabajo = Trabajo(
                    id_cliente=cliente.id_cliente,
                    id_tecnico=tecnico.id_usuario,
                    id_tipo=tipo_prob.id_tipo,
                    fecha_creacion=fake.date_time_between(start_date='-90d', end_date='now'),
                    estado=random.choice(["En Proceso", "Finalizado", "Pendiente"]),
                    tipo_problema=tipo_prob.nombre
                )
                trabajos.append(trabajo)
            session.add_all(trabajos)
            session.commit()
            print(f"🔧 Trabajos insertados: {len(trabajos)}")

            # ==================================================
            # 7️⃣ DETALLES DE TRABAJO
            # ==================================================
            detalles = [
                DetalleTrabajo(
                    id_trabajo=random.choice(trabajos).id_trabajo,
                    tipo=random.choice(["Diagnóstico", "Reparación", "Instalación"]),
                    descripcion=fake.text(max_nb_chars=150)
                )
                for _ in range(120)
            ]
            session.add_all(detalles)
            session.commit()
            print(f"📄 DetallesTrabajo insertados: {len(detalles)}")

            # ==================================================
            # 8️⃣ EQUIPOS INSTALADOS
            # ==================================================
            equipos = [
                EquipoInstalado(
                    id_trabajo=random.choice(trabajos).id_trabajo,
                    modelo=f"Modelo-{fake.random_int(100, 999)}",
                    serie=f"SN-{fake.uuid4()[:8]}",
                    fecha_instalacion=fake.date_between(start_date='-60d', end_date='today')
                )
                for _ in range(60)
            ]
            session.add_all(equipos)
            session.commit()
            print(f"💻 EquiposInstalados insertados: {len(equipos)}")

            # ==================================================
            # 9️⃣ CATALOGO
            # ==================================================
            catalogos = [
                Catalogo(
                    nombre=f"Entrada {i}",
                    descripcion=fake.text(max_nb_chars=100),
                    tipo=random.choice(["Problema", "Categoría", "MotivoCierre"]),
                    creado_por=random.choice(usuarios).id_usuario
                )
                for i in range(1, 20)
            ]
            session.add_all(catalogos)
            session.commit()
            print(f"📚 Catálogos insertados: {len(catalogos)}")

            # ==================================================
            # 🔟 TICKETS
            # ==================================================
            tickets = []
            for _ in range(100):
                trabajo = random.choice(trabajos)
                creador = random.choice(usuarios)
                catalogo = random.choice(catalogos)
                ticket = Ticket(
                    id_trabajo=trabajo.id_trabajo,
                    creado_por=creador.id_usuario,
                    id_catalogo=catalogo.id_catalogo,
                    fecha_creado=fake.date_time_between(start_date=trabajo.fecha_creacion, end_date='now'),
                    estado=random.choice(["Abierto", "En Progreso", "Cerrado"]),
                    prioridad=random.choice(["Alta", "Media", "Baja"])
                )
                tickets.append(ticket)
            session.add_all(tickets)
            session.commit()
            print(f"🎫 Tickets insertados: {len(tickets)}")

            # ==================================================
            # 1️⃣1️⃣ VALIDACIONES
            # ==================================================
            validaciones = []
            supervisores = [u for u in usuarios if u.rol == "Supervisor"]
            for t in random.sample(tickets, int(len(tickets)*0.7)):  # 70% validados
                supervisor = random.choice(supervisores)
                validacion = Validacion(
                    id_ticket=t.id_ticket,
                    id_supervisor=supervisor.id_usuario,
                    fecha_validacion=t.fecha_creado + timedelta(days=random.randint(1, 5)),
                    resultado=random.choice([True, False]),
                    observaciones=fake.sentence()
                )
                validaciones.append(validacion)
            session.add_all(validaciones)
            session.commit()
            print(f"✅ Validaciones insertadas: {len(validaciones)}")

            # ==================================================
            # 1️⃣2️⃣ HISTORIAL TICKETS
            # ==================================================
            historial = []
            for t in tickets:
                for _ in range(random.randint(1, 3)):
                    h = HistorialTicket(
                        id_ticket=t.id_ticket,
                        fecha=t.fecha_creado + timedelta(hours=random.randint(1, 72)),
                        estado_anterior=random.choice(["Abierto", "En Progreso", "Pendiente"]),
                        estado_nuevo=random.choice(["En Progreso", "Cerrado", "Reabierto"]),
                        comentario=fake.sentence()
                    )
                    historial.append(h)
            session.add_all(historial)
            session.commit()
            print(f"🕓 HistorialTickets insertados: {len(historial)}")

            print("-"*70)
            print("🎉 Poblamiento completado exitosamente 🎉")

        except Exception as e:
            session.rollback()
            print(f"❌ Error durante el poblamiento: {e}")

if __name__ == "__main__":
    poblar_datos()
