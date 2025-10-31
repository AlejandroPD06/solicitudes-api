"""
Schemas de validación para la API de Solicitudes.
"""

from .usuario_schema import UsuarioRegistroSchema, UsuarioLoginSchema, UsuarioUpdateSchema, CambiarPasswordSchema
from .solicitud_schema import SolicitudCreateSchema, SolicitudUpdateSchema, CambiarEstadoSchema
from .notificacion_schema import MarcarLeidaSchema

__all__ = [
    'UsuarioRegistroSchema',
    'UsuarioLoginSchema',
    'UsuarioUpdateSchema',
    'CambiarPasswordSchema',
    'SolicitudCreateSchema',
    'SolicitudUpdateSchema',
    'CambiarEstadoSchema',
    'MarcarLeidaSchema',
]
