"""Modelo de Solicitud."""
from datetime import datetime
from app import db
from sqlalchemy import Index


class Solicitud(db.Model):
    """Modelo de Solicitud interna."""

    __tablename__ = 'solicitudes'

    # Campos
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(
        db.Enum('compra', 'mantenimiento', 'soporte_tecnico', 'otro', name='tipo_solicitud_enum'),
        nullable=False
    )
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(
        db.Enum('pendiente', 'aprobada', 'rechazada', 'en_proceso', 'completada', name='estado_solicitud_enum'),
        nullable=False,
        default='pendiente',
        index=True
    )
    prioridad = db.Column(
        db.Enum('baja', 'media', 'alta', 'urgente', name='prioridad_enum'),
        nullable=False,
        default='media'
    )
    comentarios = db.Column(db.Text, nullable=True)
    fecha_requerida = db.Column(db.Date, nullable=True)

    # Campos de auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_aprobacion = db.Column(db.DateTime, nullable=True)

    # Relaciones - Foreign Keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    aprobador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    # Relaciones inversas
    notificaciones = db.relationship(
        'Notificacion',
        backref='solicitud',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Índices compuestos
    __table_args__ = (
        Index('idx_solicitud_usuario_estado', 'usuario_id', 'estado'),
        Index('idx_solicitud_tipo_estado', 'tipo', 'estado'),
        Index('idx_solicitud_created', 'created_at'),
    )

    def __repr__(self):
        """Representación de la solicitud."""
        return f'<Solicitud {self.id} - {self.tipo} ({self.estado})>'

    def to_dict(self, include_relations=False):
        """
        Convertir solicitud a diccionario.

        Args:
            include_relations: Si se deben incluir las relaciones

        Returns:
            dict: Diccionario con los datos de la solicitud
        """
        data = {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'comentarios': self.comentarios,
            'fecha_requerida': self.fecha_requerida.isoformat() if self.fecha_requerida else None,
            'usuario_id': self.usuario_id,
            'aprobador_id': self.aprobador_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'fecha_aprobacion': self.fecha_aprobacion.isoformat() if self.fecha_aprobacion else None
        }

        if include_relations:
            data['usuario'] = self.usuario.to_dict(include_email=False) if self.usuario else None
            data['aprobador'] = self.aprobador.to_dict(include_email=False) if self.aprobador else None

        return data

    def cambiar_estado(self, nuevo_estado, aprobador_id=None, comentarios=None):
        """
        Cambiar el estado de la solicitud.

        Args:
            nuevo_estado: Nuevo estado de la solicitud
            aprobador_id: ID del usuario que aprueba/rechaza
            comentarios: Comentarios adicionales
        """
        self.estado = nuevo_estado
        self.updated_at = datetime.utcnow()

        if nuevo_estado in ['aprobada', 'rechazada'] and aprobador_id:
            self.aprobador_id = aprobador_id
            self.fecha_aprobacion = datetime.utcnow()

        if comentarios:
            if self.comentarios:
                self.comentarios += f"\n---\n{comentarios}"
            else:
                self.comentarios = comentarios

    @property
    def esta_pendiente(self):
        """Verificar si la solicitud está pendiente."""
        return self.estado == 'pendiente'

    @property
    def esta_aprobada(self):
        """Verificar si la solicitud está aprobada."""
        return self.estado == 'aprobada'

    @property
    def esta_rechazada(self):
        """Verificar si la solicitud está rechazada."""
        return self.estado == 'rechazada'

    @property
    def requiere_atencion(self):
        """Verificar si la solicitud requiere atención urgente."""
        return self.prioridad in ['alta', 'urgente'] and self.estado == 'pendiente'
