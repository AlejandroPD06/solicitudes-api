"""Script de gestión para la aplicación."""
import os
from flask.cli import FlaskGroup
from app import create_app, db
from app.models.usuario import Usuario
from app.models.solicitud import Solicitud
from app.models.notificacion import Notificacion

app = create_app(os.getenv('FLASK_ENV', 'development'))
cli = FlaskGroup(app)


@cli.command("init-db")
def init_db():
    """Inicializar la base de datos."""
    print("Creando tablas...")
    db.create_all()
    print("Base de datos inicializada exitosamente!")


@cli.command("drop-db")
def drop_db():
    """Eliminar todas las tablas de la base de datos."""
    print("Eliminando tablas...")
    db.drop_all()
    print("Tablas eliminadas!")


@cli.command("reset-db")
def reset_db():
    """Resetear la base de datos (eliminar y crear)."""
    print("Reseteando base de datos...")
    db.drop_all()
    db.create_all()
    print("Base de datos reseteada!")


@cli.command("migrate-notifications")
def migrate_notifications():
    """Migrar tabla de notificaciones para soportar in-app notifications."""
    from sqlalchemy import text
    print("Migrando tabla de notificaciones...")

    try:
        # Ejecutar ALTER TABLE para agregar nuevas columnas
        with db.engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE notificaciones
                ADD COLUMN IF NOT EXISTS usuario_id INTEGER,
                ADD COLUMN IF NOT EXISTS titulo VARCHAR(200),
                ADD COLUMN IF NOT EXISTS mensaje TEXT,
                ADD COLUMN IF NOT EXISTS leida BOOLEAN DEFAULT FALSE NOT NULL,
                ADD COLUMN IF NOT EXISTS fecha_lectura TIMESTAMP
            """))
            conn.commit()

            # Hacer que los campos de email sean nullable (para backwards compatibility)
            campos_nullable = ['destinatario_email', 'destinatario_nombre', 'asunto']
            for campo in campos_nullable:
                try:
                    conn.execute(text(f"""
                        ALTER TABLE notificaciones
                        ALTER COLUMN {campo} DROP NOT NULL
                    """))
                    conn.commit()
                    print(f"✓ {campo} is now nullable")
                except Exception as e:
                    print(f"⚠ {campo} may already be nullable: {str(e)}")

            # Crear índice en usuario_id si no existe
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_notificaciones_usuario_id
                ON notificaciones (usuario_id)
            """))
            conn.commit()

            # Crear índice en leida si no existe
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_notificaciones_leida
                ON notificaciones (leida)
            """))
            conn.commit()

            # Agregar foreign key si no existe (solo para PostgreSQL)
            try:
                conn.execute(text("""
                    ALTER TABLE notificaciones
                    ADD CONSTRAINT fk_notificaciones_usuario_id
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                """))
                conn.commit()
            except Exception:
                # Ignorar si ya existe o no es soportado
                pass

        print("✓ Tabla de notificaciones migrada exitosamente!")

    except Exception as e:
        print(f"⚠ Error durante migración: {str(e)}")
        print("La tabla puede ya tener las columnas necesarias.")


@cli.command("seed-db")
def seed_db():
    """Poblar la base de datos con datos de prueba."""
    print("Poblando base de datos con datos de prueba...")

    # Crear usuarios de prueba
    admin = Usuario(
        email='admin@solicitudes.com',
        nombre='Admin',
        apellido='Sistema',
        rol='administrador'
    )
    admin.set_password('admin123')

    jefe = Usuario(
        email='jefe@solicitudes.com',
        nombre='Juan',
        apellido='Pérez',
        rol='jefe'
    )
    jefe.set_password('jefe123')

    empleado = Usuario(
        email='empleado@solicitudes.com',
        nombre='María',
        apellido='García',
        rol='empleado'
    )
    empleado.set_password('empleado123')

    db.session.add_all([admin, jefe, empleado])
    db.session.commit()

    print(f"✓ Usuarios creados:")
    print(f"  - Admin: admin@solicitudes.com / admin123")
    print(f"  - Jefe: jefe@solicitudes.com / jefe123")
    print(f"  - Empleado: empleado@solicitudes.com / empleado123")

    # Crear solicitudes de prueba
    solicitud1 = Solicitud(
        tipo='compra',
        titulo='Compra de laptops para equipo de desarrollo',
        descripcion='Se requieren 5 laptops para el nuevo equipo de desarrollo',
        prioridad='alta',
        usuario_id=empleado.id
    )

    solicitud2 = Solicitud(
        tipo='mantenimiento',
        titulo='Mantenimiento preventivo de servidores',
        descripcion='Realizar mantenimiento preventivo de los servidores de producción',
        prioridad='media',
        estado='aprobada',
        usuario_id=empleado.id,
        aprobador_id=jefe.id
    )

    solicitud3 = Solicitud(
        tipo='soporte_tecnico',
        titulo='Problema con impresora del 3er piso',
        descripcion='La impresora no está funcionando correctamente',
        prioridad='baja',
        usuario_id=empleado.id
    )

    db.session.add_all([solicitud1, solicitud2, solicitud3])
    db.session.commit()

    print(f"✓ {Solicitud.query.count()} solicitudes de prueba creadas")

    print("\n✅ Base de datos poblada exitosamente!")


if __name__ == '__main__':
    cli()
