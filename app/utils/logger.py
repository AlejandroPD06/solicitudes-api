"""
Configuración y utilidades de logging.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


# Crear directorio de logs si no existe
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logger(app=None):
    """
    Configura el logger de la aplicación.

    Args:
        app: Instancia de Flask (opcional)

    Returns:
        Logger configurado
    """
    logger = logging.getLogger('solicitudes_api')
    logger.setLevel(logging.INFO)

    # Evitar duplicados
    if logger.handlers:
        return logger

    # Formato de log
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Handler para archivo (con rotación)
    file_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, 'solicitudes_api.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para errores (archivo separado)
    error_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, 'errors.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Handler para consola (solo en desarrollo)
    if app and app.config.get('DEBUG'):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger():
    """
    Obtiene el logger de la aplicación.

    Returns:
        Logger instance
    """
    return logging.getLogger('solicitudes_api')


def log_info(message, **kwargs):
    """
    Registra un mensaje informativo.

    Args:
        message: Mensaje a registrar
        **kwargs: Datos adicionales para el contexto
    """
    logger = get_logger()
    if kwargs:
        logger.info(f"{message} | Context: {kwargs}")
    else:
        logger.info(message)


def log_error(message, exception=None, **kwargs):
    """
    Registra un error.

    Args:
        message: Mensaje de error
        exception: Excepción (opcional)
        **kwargs: Datos adicionales para el contexto
    """
    logger = get_logger()
    context = kwargs.copy()

    if exception:
        context['exception_type'] = type(exception).__name__
        context['exception_message'] = str(exception)

    if context:
        logger.error(f"{message} | Context: {context}", exc_info=exception)
    else:
        logger.error(message, exc_info=exception)


def log_warning(message, **kwargs):
    """
    Registra una advertencia.

    Args:
        message: Mensaje de advertencia
        **kwargs: Datos adicionales para el contexto
    """
    logger = get_logger()
    if kwargs:
        logger.warning(f"{message} | Context: {kwargs}")
    else:
        logger.warning(message)


def log_debug(message, **kwargs):
    """
    Registra un mensaje de debug.

    Args:
        message: Mensaje de debug
        **kwargs: Datos adicionales para el contexto
    """
    logger = get_logger()
    if kwargs:
        logger.debug(f"{message} | Context: {kwargs}")
    else:
        logger.debug(message)


def log_request(request, user_id=None):
    """
    Registra detalles de una request HTTP.

    Args:
        request: Objeto request de Flask
        user_id: ID del usuario (opcional)
    """
    logger = get_logger()
    logger.info(
        f"Request: {request.method} {request.path}",
        extra={
            'method': request.method,
            'path': request.path,
            'user_id': user_id,
            'remote_addr': request.remote_addr,
            'user_agent': str(request.user_agent)
        }
    )


def log_response(request, status_code, user_id=None):
    """
    Registra detalles de una response HTTP.

    Args:
        request: Objeto request de Flask
        status_code: Código de estado HTTP
        user_id: ID del usuario (opcional)
    """
    logger = get_logger()
    level = logging.ERROR if status_code >= 500 else logging.INFO

    logger.log(
        level,
        f"Response: {request.method} {request.path} - {status_code}",
        extra={
            'method': request.method,
            'path': request.path,
            'status_code': status_code,
            'user_id': user_id,
        }
    )
