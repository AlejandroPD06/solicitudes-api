"""
Schemas de validación para notificaciones.
"""

from marshmallow import Schema, fields


class MarcarLeidaSchema(Schema):
    """Schema para validar el marcado de notificación como leída."""

    # Este schema está vacío porque el endpoint PATCH /notificaciones/{id}/marcar-leida
    # no requiere body, pero lo dejamos para consistencia y posible extensión futura
    pass
