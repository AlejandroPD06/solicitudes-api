"""
Funciones helper para respuestas HTTP consistentes.
"""

from flask import jsonify
from datetime import datetime
import uuid


def _generate_request_id():
    """Genera un ID único para la request."""
    return str(uuid.uuid4())


def success_response(data=None, message=None, status_code=200, meta=None):
    """
    Crea una respuesta de éxito consistente.

    Args:
        data: Datos a retornar (dict, list, o None)
        message: Mensaje opcional de éxito
        status_code: Código HTTP (default: 200)
        meta: Metadata adicional (ej: paginación)

    Returns:
        tuple: (response, status_code)

    Example:
        return success_response(
            data={'user': user.to_dict()},
            message='Usuario creado exitosamente',
            status_code=201
        )
    """
    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    if meta:
        response['meta'] = meta

    return jsonify(response), status_code


def error_response(error_code, message, status_code=400, details=None, request_id=None):
    """
    Crea una respuesta de error consistente.

    Args:
        error_code: Código de error interno (string)
        message: Mensaje de error legible
        status_code: Código HTTP (default: 400)
        details: Detalles adicionales del error (dict)
        request_id: ID de la request para tracking

    Returns:
        tuple: (response, status_code)

    Example:
        return error_response(
            error_code='USER_NOT_FOUND',
            message='Usuario no encontrado',
            status_code=404
        )
    """
    response = {
        'success': False,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'error': {
            'code': error_code,
            'message': message,
        }
    }

    if details:
        response['error']['details'] = details

    if request_id:
        response['request_id'] = request_id
    else:
        response['request_id'] = _generate_request_id()

    return jsonify(response), status_code


def paginated_response(items, total, page, per_page, message=None, status_code=200):
    """
    Crea una respuesta paginada consistente.

    Args:
        items: Lista de items para la página actual
        total: Total de items disponibles
        page: Página actual
        per_page: Items por página
        message: Mensaje opcional
        status_code: Código HTTP (default: 200)

    Returns:
        tuple: (response, status_code)

    Example:
        return paginated_response(
            items=[sol.to_dict() for sol in solicitudes],
            total=pagination.total,
            page=page,
            per_page=per_page
        )
    """
    total_pages = (total + per_page - 1) // per_page  # Redondeo hacia arriba

    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'data': items,
        'meta': {
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1,
            }
        }
    }

    if message:
        response['message'] = message

    return jsonify(response), status_code


def created_response(data, message='Recurso creado exitosamente', location=None):
    """
    Crea una respuesta 201 Created.

    Args:
        data: Datos del recurso creado
        message: Mensaje de éxito
        location: URL del recurso creado (opcional)

    Returns:
        tuple: (response, status_code, headers)

    Example:
        return created_response(
            data={'user': user.to_dict()},
            message='Usuario creado exitosamente',
            location=f'/api/usuarios/{user.id}'
        )
    """
    response, status_code = success_response(
        data=data,
        message=message,
        status_code=201
    )

    if location:
        headers = {'Location': location}
        return response, status_code, headers

    return response, status_code


def no_content_response():
    """
    Crea una respuesta 204 No Content (para DELETE exitoso).

    Returns:
        tuple: ('', status_code)

    Example:
        return no_content_response()
    """
    return '', 204
