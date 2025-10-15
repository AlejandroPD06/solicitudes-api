"""Servicio de autenticación JWT."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    verify_jwt_in_request
)
from app import db
from app.models.usuario import Usuario


def crear_tokens(usuario):
    """
    Crear tokens de acceso y refresh para un usuario.

    Args:
        usuario: Objeto Usuario

    Returns:
        dict: Diccionario con los tokens
    """
    # Usar solo el ID del usuario como identity (Flask-JWT-Extended espera un valor simple)
    # Convertir a string para compatibilidad con PyJWT 2.x
    identity = str(usuario.id)

    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }


def obtener_usuario_actual():
    """
    Obtener el usuario actual desde el JWT.

    Returns:
        Usuario: Usuario actual o None
    """
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()  # Identity es el user_id como string
        usuario = Usuario.query.get(int(identity))  # Convertir a int para la consulta
        return usuario
    except:
        return None


def rol_requerido(*roles_permitidos):
    """
    Decorador para verificar el rol del usuario.

    Args:
        roles_permitidos: Roles que tienen permiso para acceder

    Returns:
        function: Decorador
    """
    def decorador(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()  # Identity es el user_id como string
            usuario = Usuario.query.get(int(identity))  # Convertir a int para la consulta

            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            if not usuario.activo:
                return jsonify({'error': 'Usuario inactivo'}), 403

            if usuario.rol not in roles_permitidos:
                return jsonify({
                    'error': 'No tienes permisos para realizar esta acción',
                    'rol_requerido': list(roles_permitidos),
                    'tu_rol': usuario.rol
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorador


def registrar_usuario(email, password, nombre, apellido=None, rol='empleado'):
    """
    Registrar un nuevo usuario.

    Args:
        email: Email del usuario
        password: Contraseña del usuario
        nombre: Nombre del usuario
        apellido: Apellido del usuario (opcional)
        rol: Rol del usuario (por defecto 'empleado')

    Returns:
        tuple: (Usuario, error_mensaje)
    """
    # Validar que el email no exista
    if Usuario.query.filter_by(email=email).first():
        return None, 'El email ya está registrado'

    # Validar rol
    roles_validos = ['empleado', 'jefe', 'administrador']
    if rol not in roles_validos:
        return None, f'Rol inválido. Debe ser uno de: {", ".join(roles_validos)}'

    # Crear usuario
    usuario = Usuario(
        email=email,
        nombre=nombre,
        apellido=apellido,
        rol=rol
    )
    usuario.set_password(password)

    try:
        db.session.add(usuario)
        db.session.commit()
        return usuario, None
    except Exception as e:
        db.session.rollback()
        return None, f'Error al registrar usuario: {str(e)}'


def autenticar_usuario(email, password):
    """
    Autenticar un usuario.

    Args:
        email: Email del usuario
        password: Contraseña del usuario

    Returns:
        tuple: (Usuario, error_mensaje)
    """
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return None, 'Credenciales inválidas'

    if not usuario.activo:
        return None, 'Usuario inactivo'

    if not usuario.check_password(password):
        return None, 'Credenciales inválidas'

    return usuario, None


def cambiar_password(usuario, password_actual, password_nueva):
    """
    Cambiar la contraseña de un usuario.

    Args:
        usuario: Objeto Usuario
        password_actual: Contraseña actual
        password_nueva: Nueva contraseña

    Returns:
        tuple: (success, error_mensaje)
    """
    if not usuario.check_password(password_actual):
        return False, 'Contraseña actual incorrecta'

    usuario.set_password(password_nueva)

    try:
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, f'Error al cambiar contraseña: {str(e)}'
