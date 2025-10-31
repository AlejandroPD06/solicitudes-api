"""
Decoradores y funciones de validación.
"""

from functools import wraps
from flask import request
from marshmallow import ValidationError as MarshmallowValidationError
from app.exceptions import ValidationError, BadRequestError


def validate_request(schema_class):
    """
    Decorador para validar el cuerpo de la request usando un schema de Marshmallow.

    Args:
        schema_class: Clase del schema de Marshmallow a usar para validación

    Raises:
        BadRequestError: Si el JSON es inválido
        ValidationError: Si la validación del schema falla

    Example:
        @app.route('/users', methods=['POST'])
        @validate_request(UserCreateSchema)
        def create_user():
            data = request.validated_data
            # ... usar data validado
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar que el content-type sea JSON
            if not request.is_json:
                raise BadRequestError(
                    message='El Content-Type debe ser application/json',
                    error_code='INVALID_CONTENT_TYPE'
                )

            # Obtener el JSON del request
            try:
                json_data = request.get_json()
            except Exception as e:
                raise BadRequestError(
                    message='El cuerpo de la solicitud no es un JSON válido',
                    error_code='INVALID_JSON',
                    details={'error': str(e)}
                )

            if json_data is None:
                raise BadRequestError(
                    message='El cuerpo de la solicitud está vacío',
                    error_code='EMPTY_BODY'
                )

            # Validar usando el schema
            schema = schema_class()
            try:
                validated_data = schema.load(json_data)
            except MarshmallowValidationError as e:
                raise ValidationError(
                    message='Los datos proporcionados no son válidos',
                    error_code='VALIDATION_ERROR',
                    details={'errors': e.messages}
                )

            # Adjuntar los datos validados al request para acceso fácil
            request.validated_data = validated_data

            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_json():
    """
    Decorador simple para validar que el request tenga JSON válido.

    Raises:
        BadRequestError: Si el JSON es inválido o está vacío
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise BadRequestError(
                    message='El Content-Type debe ser application/json',
                    error_code='INVALID_CONTENT_TYPE'
                )

            try:
                json_data = request.get_json()
            except Exception as e:
                raise BadRequestError(
                    message='El cuerpo de la solicitud no es un JSON válido',
                    error_code='INVALID_JSON',
                    details={'error': str(e)}
                )

            if json_data is None:
                raise BadRequestError(
                    message='El cuerpo de la solicitud está vacío',
                    error_code='EMPTY_BODY'
                )

            return f(*args, **kwargs)
        return wrapper
    return decorator
