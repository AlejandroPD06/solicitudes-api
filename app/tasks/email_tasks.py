"""Tareas de Celery para el envío de emails."""
import os
from flask import Flask
from flask_mail import Message
from app.tasks import celery_app
from config import config_by_name


# Crear una app Flask mínima para el contexto
def crear_app_contexto():
    """Crear una app Flask para el contexto de Celery."""
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_by_name[config_name])

    from app import mail, db
    mail.init_app(app)
    db.init_app(app)

    return app


def obtener_solicitud_y_contexto(solicitud_id):
    """
    Obtener la solicitud y crear el contexto de la app.

    Args:
        solicitud_id: ID de la solicitud

    Returns:
        tuple: (app, solicitud)
    """
    app = crear_app_contexto()

    with app.app_context():
        from app.models.solicitud import Solicitud
        solicitud = Solicitud.query.get(solicitud_id)
        return app, solicitud


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def enviar_email_solicitud(self, solicitud_id, tipo_notificacion):
    """
    Enviar email de notificación de solicitud.

    Args:
        solicitud_id: ID de la solicitud
        tipo_notificacion: Tipo de notificación (solicitud_creada, solicitud_aprobada, etc.)
    """
    app, solicitud = obtener_solicitud_y_contexto(solicitud_id)

    if not solicitud:
        print(f"Solicitud {solicitud_id} no encontrada")
        return

    with app.app_context():
        from app import mail, db
        from app.models.notificacion import Notificacion
        from flask_mail import Message

        # Determinar destinatario según el tipo de notificación
        if tipo_notificacion == 'solicitud_creada':
            # Enviar a jefes/administradores
            from app.models.usuario import Usuario
            destinatarios = Usuario.query.filter(
                Usuario.rol.in_(['jefe', 'administrador']),
                Usuario.activo == True
            ).all()
        else:
            # Enviar al creador de la solicitud
            destinatarios = [solicitud.usuario]

        # Crear y enviar notificación para cada destinatario
        for destinatario in destinatarios:
            try:
                # Crear registro de notificación
                notificacion = Notificacion.crear_notificacion_solicitud(
                    solicitud,
                    tipo_notificacion,
                    destinatario.email,
                    destinatario.nombre_completo
                )
                db.session.add(notificacion)
                db.session.commit()

                # Construir mensaje de email
                asunto = notificacion.asunto
                cuerpo = crear_cuerpo_email(solicitud, tipo_notificacion, destinatario)

                # Enviar email
                msg = Message(
                    subject=asunto,
                    recipients=[destinatario.email],
                    body=cuerpo,
                    html=crear_html_email(solicitud, tipo_notificacion, destinatario)
                )

                mail.send(msg)

                # Marcar como enviado
                notificacion.marcar_como_enviado()
                db.session.commit()

                print(f"Email enviado a {destinatario.email} para solicitud {solicitud_id}")

            except Exception as e:
                # Registrar error
                if 'notificacion' in locals():
                    notificacion.registrar_error(str(e))
                    db.session.commit()

                print(f"Error al enviar email a {destinatario.email}: {str(e)}")

                # Reintentar la tarea
                try:
                    raise self.retry(exc=e)
                except Exception as retry_exc:
                    print(f"No se pudo reintentar: {retry_exc}")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def reenviar_notificacion(self, notificacion_id):
    """
    Reenviar una notificación existente.

    Args:
        notificacion_id: ID de la notificación
    """
    app = crear_app_contexto()

    with app.app_context():
        from app import mail, db
        from app.models.notificacion import Notificacion
        from flask_mail import Message

        notificacion = Notificacion.query.get(notificacion_id)

        if not notificacion:
            print(f"Notificación {notificacion_id} no encontrada")
            return

        try:
            # Construir mensaje de email
            msg = Message(
                subject=notificacion.asunto,
                recipients=[notificacion.destinatario_email],
                body=notificacion.mensaje,
                html=crear_html_email(
                    notificacion.solicitud,
                    notificacion.tipo,
                    None,
                    notificacion.destinatario_nombre
                )
            )

            mail.send(msg)

            # Marcar como enviado
            notificacion.marcar_como_enviado()
            db.session.commit()

            print(f"Notificación {notificacion_id} reenviada exitosamente")

        except Exception as e:
            # Registrar error
            notificacion.registrar_error(str(e))
            db.session.commit()

            print(f"Error al reenviar notificación {notificacion_id}: {str(e)}")

            # Reintentar la tarea
            try:
                raise self.retry(exc=e)
            except Exception as retry_exc:
                print(f"No se pudo reintentar: {retry_exc}")


def crear_cuerpo_email(solicitud, tipo_notificacion, destinatario):
    """
    Crear el cuerpo del email en texto plano.

    Args:
        solicitud: Objeto Solicitud
        tipo_notificacion: Tipo de notificación
        destinatario: Usuario destinatario

    Returns:
        str: Cuerpo del email
    """
    cuerpo = f"Hola {destinatario.nombre},\n\n"

    if tipo_notificacion == 'solicitud_creada':
        cuerpo += f"Se ha creado una nueva solicitud que requiere tu atención:\n\n"
    elif tipo_notificacion == 'solicitud_aprobada':
        cuerpo += f"Tu solicitud ha sido aprobada:\n\n"
    elif tipo_notificacion == 'solicitud_rechazada':
        cuerpo += f"Tu solicitud ha sido rechazada:\n\n"

    cuerpo += f"Tipo: {solicitud.tipo.replace('_', ' ').title()}\n"
    cuerpo += f"Título: {solicitud.titulo}\n"
    cuerpo += f"Descripción: {solicitud.descripcion}\n"
    cuerpo += f"Estado: {solicitud.estado.replace('_', ' ').title()}\n"
    cuerpo += f"Prioridad: {solicitud.prioridad.title()}\n"

    if solicitud.aprobador:
        cuerpo += f"Procesado por: {solicitud.aprobador.nombre_completo}\n"

    if solicitud.comentarios:
        cuerpo += f"\nComentarios:\n{solicitud.comentarios}\n"

    cuerpo += "\n---\n"
    cuerpo += "Sistema de Gestión de Solicitudes Internas\n"
    cuerpo += "Este es un mensaje automático, por favor no responder.\n"

    return cuerpo


def crear_html_email(solicitud, tipo_notificacion, destinatario, destinatario_nombre=None):
    """
    Crear el cuerpo del email en HTML.

    Args:
        solicitud: Objeto Solicitud
        tipo_notificacion: Tipo de notificación
        destinatario: Usuario destinatario (puede ser None)
        destinatario_nombre: Nombre del destinatario (alternativa)

    Returns:
        str: HTML del email
    """
    nombre = destinatario.nombre if destinatario else destinatario_nombre

    # Colores según el tipo de notificación
    colores = {
        'solicitud_creada': '#3498db',  # Azul
        'solicitud_aprobada': '#2ecc71',  # Verde
        'solicitud_rechazada': '#e74c3c',  # Rojo
        'solicitud_actualizada': '#f39c12',  # Naranja
        'recordatorio': '#9b59b6'  # Púrpura
    }

    color = colores.get(tipo_notificacion, '#34495e')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .info-row {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .footer {{ text-align: center; padding: 20px; color: #777; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Sistema de Gestión de Solicitudes</h2>
            </div>
            <div class="content">
                <p>Hola {nombre},</p>
    """

    if tipo_notificacion == 'solicitud_creada':
        html += "<p>Se ha creado una nueva solicitud que requiere tu atención:</p>"
    elif tipo_notificacion == 'solicitud_aprobada':
        html += "<p>Tu solicitud ha sido <strong>aprobada</strong>:</p>"
    elif tipo_notificacion == 'solicitud_rechazada':
        html += "<p>Tu solicitud ha sido <strong>rechazada</strong>:</p>"

    html += f"""
                <div class="info-row"><span class="label">ID:</span> #{solicitud.id}</div>
                <div class="info-row"><span class="label">Tipo:</span> {solicitud.tipo.replace('_', ' ').title()}</div>
                <div class="info-row"><span class="label">Título:</span> {solicitud.titulo}</div>
                <div class="info-row"><span class="label">Descripción:</span> {solicitud.descripcion}</div>
                <div class="info-row"><span class="label">Estado:</span> {solicitud.estado.replace('_', ' ').title()}</div>
                <div class="info-row"><span class="label">Prioridad:</span> {solicitud.prioridad.title()}</div>
    """

    if solicitud.aprobador:
        html += f'<div class="info-row"><span class="label">Procesado por:</span> {solicitud.aprobador.nombre_completo}</div>'

    if solicitud.comentarios:
        html += f'<div class="info-row"><span class="label">Comentarios:</span><br>{solicitud.comentarios}</div>'

    html += """
            </div>
            <div class="footer">
                <p>Sistema de Gestión de Solicitudes Internas</p>
                <p>Este es un mensaje automático, por favor no responder.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html
