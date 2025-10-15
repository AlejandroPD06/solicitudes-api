"""Modelo de Usuario."""
from datetime import datetime
from app import db, bcrypt
from sqlalchemy import Index


class Usuario(db.Model):
    """Modelo de Usuario con roles y autenticación."""

    __tablename__ = 'usuarios'

    # Campos
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)
    rol = db.Column(
        db.Enum('empleado', 'jefe', 'administrador', name='rol_enum'),
        nullable=False,
        default='empleado'
    )
    activo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    solicitudes = db.relationship(
        'Solicitud',
        foreign_keys='Solicitud.usuario_id',
        backref='usuario',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    solicitudes_aprobadas = db.relationship(
        'Solicitud',
        foreign_keys='Solicitud.aprobador_id',
        backref='aprobador',
        lazy='dynamic'
    )

    # Índices compuestos
    __table_args__ = (
        Index('idx_usuario_rol_activo', 'rol', 'activo'),
    )

    def __repr__(self):
        """Representación del usuario."""
        return f'<Usuario {self.email}>'

    def set_password(self, password):
        """
        Hash de la contraseña usando bcrypt.

        Args:
            password: Contraseña en texto plano
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Verificar contraseña contra el hash.

        Args:
            password: Contraseña en texto plano

        Returns:
            bool: True si la contraseña es correcta
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=True):
        """
        Convertir usuario a diccionario.

        Args:
            include_email: Si se debe incluir el email

        Returns:
            dict: Diccionario con los datos del usuario
        """
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rol': self.rol,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_email:
            data['email'] = self.email

        return data

    @property
    def nombre_completo(self):
        """Obtener nombre completo."""
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre

    @property
    def es_admin(self):
        """Verificar si el usuario es administrador."""
        return self.rol == 'administrador'

    @property
    def es_jefe(self):
        """Verificar si el usuario es jefe."""
        return self.rol == 'jefe'

    @property
    def puede_aprobar(self):
        """Verificar si el usuario puede aprobar solicitudes."""
        return self.rol in ['jefe', 'administrador']
