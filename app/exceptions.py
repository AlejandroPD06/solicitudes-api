"""
Excepciones personalizadas para la API de Solicitudes.

Este módulo define excepciones personalizadas que mapean a códigos de estado HTTP
específicos según los estándares de IANA (https://www.iana.org/assignments/http-status-codes/).
"""


class APIException(Exception):
    """Excepción base para todas las excepciones de la API."""

    status_code = 500
    error_code = 'INTERNAL_ERROR'

    def __init__(self, message=None, error_code=None, details=None):
        super().__init__()
        self.message = message or self.get_default_message()
        if error_code:
            self.error_code = error_code
        self.details = details or {}

    def get_default_message(self):
        return 'Ha ocurrido un error en el servidor'

    def to_dict(self):
        return {
            'error': {
                'code': self.error_code,
                'message': self.message,
                'details': self.details
            }
        }


# 4xx Client Errors

class BadRequestError(APIException):
    """400 Bad Request - La solicitud no puede ser procesada debido a sintaxis incorrecta."""

    status_code = 400
    error_code = 'BAD_REQUEST'

    def get_default_message(self):
        return 'La solicitud contiene sintaxis incorrecta'


class UnauthorizedError(APIException):
    """401 Unauthorized - Autenticación requerida o fallida."""

    status_code = 401
    error_code = 'UNAUTHORIZED'

    def get_default_message(self):
        return 'Autenticación requerida o credenciales inválidas'


class ForbiddenError(APIException):
    """403 Forbidden - El usuario no tiene permisos para acceder al recurso."""

    status_code = 403
    error_code = 'FORBIDDEN'

    def get_default_message(self):
        return 'No tienes permisos para acceder a este recurso'


class NotFoundError(APIException):
    """404 Not Found - El recurso solicitado no existe."""

    status_code = 404
    error_code = 'NOT_FOUND'

    def get_default_message(self):
        return 'El recurso solicitado no fue encontrado'


class MethodNotAllowedError(APIException):
    """405 Method Not Allowed - El método HTTP no está permitido para este recurso."""

    status_code = 405
    error_code = 'METHOD_NOT_ALLOWED'

    def get_default_message(self):
        return 'El método HTTP no está permitido para este recurso'


class ConflictError(APIException):
    """409 Conflict - La solicitud no puede completarse debido a un conflicto con el estado actual."""

    status_code = 409
    error_code = 'CONFLICT'

    def get_default_message(self):
        return 'La solicitud genera un conflicto con el estado actual del recurso'


class ValidationError(APIException):
    """422 Unprocessable Entity - La solicitud está bien formada pero contiene errores semánticos."""

    status_code = 422
    error_code = 'VALIDATION_ERROR'

    def get_default_message(self):
        return 'Los datos proporcionados no son válidos'


class TooManyRequestsError(APIException):
    """429 Too Many Requests - El usuario ha enviado demasiadas solicitudes en un período de tiempo."""

    status_code = 429
    error_code = 'TOO_MANY_REQUESTS'

    def get_default_message(self):
        return 'Has excedido el límite de solicitudes permitidas'


# 5xx Server Errors

class InternalServerError(APIException):
    """500 Internal Server Error - Error genérico del servidor."""

    status_code = 500
    error_code = 'INTERNAL_SERVER_ERROR'

    def get_default_message(self):
        return 'Ha ocurrido un error interno en el servidor'


class NotImplementedError(APIException):
    """501 Not Implemented - El servidor no reconoce el método de solicitud."""

    status_code = 501
    error_code = 'NOT_IMPLEMENTED'

    def get_default_message(self):
        return 'Esta funcionalidad aún no está implementada'


class ServiceUnavailableError(APIException):
    """503 Service Unavailable - El servidor no está disponible temporalmente."""

    status_code = 503
    error_code = 'SERVICE_UNAVAILABLE'

    def get_default_message(self):
        return 'El servicio no está disponible temporalmente'


# Excepciones específicas del dominio

class UserAlreadyExistsError(ConflictError):
    """El email ya está registrado en el sistema."""

    error_code = 'USER_ALREADY_EXISTS'

    def get_default_message(self):
        return 'El email ya está registrado en el sistema'


class UserNotFoundError(NotFoundError):
    """Usuario no encontrado."""

    error_code = 'USER_NOT_FOUND'

    def get_default_message(self):
        return 'Usuario no encontrado'


class InvalidCredentialsError(UnauthorizedError):
    """Credenciales incorrectas."""

    error_code = 'INVALID_CREDENTIALS'

    def get_default_message(self):
        return 'Email o contraseña incorrectos'


class InactiveUserError(ForbiddenError):
    """Usuario inactivo."""

    error_code = 'INACTIVE_USER'

    def get_default_message(self):
        return 'Tu cuenta está inactiva. Contacta al administrador'


class InsufficientPermissionsError(ForbiddenError):
    """Permisos insuficientes para realizar la acción."""

    error_code = 'INSUFFICIENT_PERMISSIONS'

    def get_default_message(self):
        return 'No tienes permisos suficientes para realizar esta acción'


class SolicitudNotFoundError(NotFoundError):
    """Solicitud no encontrada."""

    error_code = 'SOLICITUD_NOT_FOUND'

    def get_default_message(self):
        return 'Solicitud no encontrada'


class SolicitudAlreadyProcessedError(ConflictError):
    """La solicitud ya fue procesada."""

    error_code = 'SOLICITUD_ALREADY_PROCESSED'

    def get_default_message(self):
        return 'La solicitud ya fue procesada y no puede ser modificada'


class NotificacionNotFoundError(NotFoundError):
    """Notificación no encontrada."""

    error_code = 'NOTIFICACION_NOT_FOUND'

    def get_default_message(self):
        return 'Notificación no encontrada'


class DatabaseError(InternalServerError):
    """Error de base de datos."""

    error_code = 'DATABASE_ERROR'

    def get_default_message(self):
        return 'Error al procesar la operación en la base de datos'
