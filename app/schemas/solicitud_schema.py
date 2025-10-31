"""
Schemas de validación para solicitudes.
"""

from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError as MarshmallowValidationError
from datetime import datetime, date


class SolicitudCreateSchema(Schema):
    """Schema para validar la creación de solicitudes."""

    tipo = fields.Str(
        required=True,
        validate=validate.OneOf(['compra', 'mantenimiento', 'soporte_tecnico', 'otro']),
        error_messages={
            'required': 'El tipo es requerido',
            'invalid': 'El tipo debe ser uno de: compra, mantenimiento, soporte_tecnico, otro'
        }
    )
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={
            'required': 'El título es requerido',
            'invalid': 'El título debe tener entre 1 y 200 caracteres'
        }
    )
    descripcion = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': 'La descripción es requerida',
            'invalid': 'La descripción no puede estar vacía'
        }
    )
    prioridad = fields.Str(
        required=False,
        validate=validate.OneOf(['baja', 'media', 'alta', 'urgente']),
        missing='media',
        error_messages={
            'invalid': 'La prioridad debe ser una de: baja, media, alta, urgente'
        }
    )
    fecha_requerida = fields.Date(
        required=False,
        allow_none=True,
        error_messages={
            'invalid': 'El formato de fecha debe ser YYYY-MM-DD'
        }
    )
    comentarios = fields.Str(
        required=False,
        allow_none=True
    )

    @validates('fecha_requerida')
    def validate_fecha_requerida(self, value):
        """Validar que la fecha requerida no sea en el pasado."""
        if value and value < date.today():
            raise MarshmallowValidationError('La fecha requerida no puede ser en el pasado')


class SolicitudUpdateSchema(Schema):
    """Schema para validar la actualización de solicitudes."""

    titulo = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=200),
        error_messages={
            'invalid': 'El título debe tener entre 1 y 200 caracteres'
        }
    )
    descripcion = fields.Str(
        required=False,
        validate=validate.Length(min=1),
        error_messages={
            'invalid': 'La descripción no puede estar vacía'
        }
    )
    tipo = fields.Str(
        required=False,
        validate=validate.OneOf(['compra', 'mantenimiento', 'soporte_tecnico', 'otro']),
        error_messages={
            'invalid': 'El tipo debe ser uno de: compra, mantenimiento, soporte_tecnico, otro'
        }
    )
    prioridad = fields.Str(
        required=False,
        validate=validate.OneOf(['baja', 'media', 'alta', 'urgente']),
        error_messages={
            'invalid': 'La prioridad debe ser una de: baja, media, alta, urgente'
        }
    )
    fecha_requerida = fields.Date(
        required=False,
        allow_none=True,
        error_messages={
            'invalid': 'El formato de fecha debe ser YYYY-MM-DD'
        }
    )
    comentarios = fields.Str(
        required=False,
        allow_none=True
    )

    @validates('fecha_requerida')
    def validate_fecha_requerida(self, value):
        """Validar que la fecha requerida no sea en el pasado."""
        if value and value < date.today():
            raise MarshmallowValidationError('La fecha requerida no puede ser en el pasado')

    @validates_schema
    def validate_at_least_one_field(self, data, **kwargs):
        """Validar que al menos un campo esté presente para actualizar."""
        if not data:
            raise MarshmallowValidationError('Debe proporcionar al menos un campo para actualizar')


class CambiarEstadoSchema(Schema):
    """Schema para validar el cambio de estado de una solicitud."""

    nuevo_estado = fields.Str(
        required=True,
        validate=validate.OneOf(['pendiente', 'aprobada', 'rechazada', 'en_proceso', 'completada']),
        error_messages={
            'required': 'El nuevo estado es requerido',
            'invalid': 'El estado debe ser uno de: pendiente, aprobada, rechazada, en_proceso, completada'
        }
    )
    comentarios = fields.Str(
        required=False,
        allow_none=True
    )
