"""Modelo de Notificación."""
from datetime import datetime
from app import db
from sqlalchemy import Index


class Notificacion(db.Model):
    """Modelo de Notificación para tracking de emails y notificaciones in-app."""

    __tablename__ = 'notificaciones'

    # Campos
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(
        db.Enum('solicitud_creada', 'solicitud_aprobada', 'solicitud_rechazada',
                'solicitud_actualizada', 'recordatorio', name='tipo_notificacion_enum'),
        nullable=False
    )

    # Campos para notificaciones in-app (opcionales para backwards compatibility)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    titulo = db.Column(db.String(200), nullable=True)
    mensaje = db.Column(db.Text, nullable=True)
    leida = db.Column(db.Boolean, default=False, nullable=False, index=True)
    fecha_lectura = db.Column(db.DateTime, nullable=True)

    # Campos para notificaciones por email (opcionales)
    destinatario_email = db.Column(db.String(120), nullable=True, index=True)
    destinatario_nombre = db.Column(db.String(100), nullable=True)
    asunto = db.Column(db.String(200), nullable=True)
    enviado = db.Column(db.Boolean, default=False, nullable=False, index=True)
    fecha_envio = db.Column(db.DateTime, nullable=True)
    intentos = db.Column(db.Integer, default=0, nullable=False)
    error_mensaje = db.Column(db.Text, nullable=True)

    # Campos de auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones - Foreign Keys
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes.id'), nullable=True, index=True)

    # Índices compuestos
    __table_args__ = (
        Index('idx_notificacion_enviado_created', 'enviado', 'created_at'),
        Index('idx_notificacion_solicitud_tipo', 'solicitud_id', 'tipo'),
    )

    def __repr__(self):
        """Representación de la notificación."""
        return f'<Notificacion {self.id} - {self.tipo} (enviado={self.enviado})>'

    def to_dict(self, include_relations=False):
        """
        Convertir notificación a diccionario.

        Args:
            include_relations: Si se deben incluir las relaciones

        Returns:
            dict: Diccionario con los datos de la notificación
        """
        data = {
            'id': self.id,
            'tipo': self.tipo,
            'usuario_id': self.usuario_id,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'leida': self.leida,
            'fecha_lectura': self.fecha_lectura.isoformat() if self.fecha_lectura else None,
            'solicitud_id': self.solicitud_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # Campos de email (opcionales, para backwards compatibility)
            'destinatario_email': self.destinatario_email,
            'asunto': self.asunto,
            'enviado': self.enviado,
            'fecha_envio': self.fecha_envio.isoformat() if self.fecha_envio else None,
        }

        if include_relations:
            data['solicitud'] = self.solicitud.to_dict() if self.solicitud else None

        return data

    def marcar_como_enviado(self):
        """Marcar la notificación como enviada."""
        self.enviado = True
        self.fecha_envio = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def marcar_como_leida(self):
        """Marcar la notificación como leída."""
        self.leida = True
        self.fecha_lectura = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def registrar_error(self, error_mensaje):
        """
        Registrar un error en el envío.

        Args:
            error_mensaje: Mensaje de error
        """
        self.intentos += 1
        self.error_mensaje = error_mensaje
        self.updated_at = datetime.utcnow()

    @staticmethod
    def crear_notificacion_solicitud(solicitud, tipo, destinatario_email, destinatario_nombre=None):
        """
        Crear una notificación basada en una solicitud.

        Args:
            solicitud: Objeto Solicitud
            tipo: Tipo de notificación
            destinatario_email: Email del destinatario
            destinatario_nombre: Nombre del destinatario (opcional)

        Returns:
            Notificacion: Nueva notificación creada
        """
        # Generar asunto y mensaje según el tipo
        asuntos = {
            'solicitud_creada': f'Nueva solicitud: {solicitud.titulo}',
            'solicitud_aprobada': f'Solicitud aprobada: {solicitud.titulo}',
            'solicitud_rechazada': f'Solicitud rechazada: {solicitud.titulo}',
            'solicitud_actualizada': f'Solicitud actualizada: {solicitud.titulo}',
            'recordatorio': f'Recordatorio de solicitud: {solicitud.titulo}'
        }

        mensajes = {
            'solicitud_creada': f'Se ha creado una nueva solicitud de tipo {solicitud.tipo}.',
            'solicitud_aprobada': f'Tu solicitud ha sido aprobada por {solicitud.aprobador.nombre_completo if solicitud.aprobador else "un administrador"}.',
            'solicitud_rechazada': f'Tu solicitud ha sido rechazada por {solicitud.aprobador.nombre_completo if solicitud.aprobador else "un administrador"}.',
            'solicitud_actualizada': f'La solicitud ha sido actualizada. Estado actual: {solicitud.estado}.',
            'recordatorio': f'Tienes una solicitud pendiente de revisión.'
        }

        notificacion = Notificacion(
            tipo=tipo,
            destinatario_email=destinatario_email,
            destinatario_nombre=destinatario_nombre,
            asunto=asuntos.get(tipo, 'Notificación'),
            mensaje=mensajes.get(tipo, 'Tienes una nueva notificación.'),
            solicitud_id=solicitud.id
        )

        return notificacion
