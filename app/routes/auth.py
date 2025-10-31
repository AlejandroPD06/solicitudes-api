"""Blueprint de autenticación y gestión de usuarios."""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.usuario import Usuario
from app.services.auth_service import (
    crear_tokens,
    registrar_usuario,
    autenticar_usuario,
    cambiar_password,
    obtener_usuario_actual,
    rol_requerido
)
from app.schemas import (
    UsuarioRegistroSchema,
    UsuarioLoginSchema,
    UsuarioUpdateSchema,
    CambiarPasswordSchema
)
from app.utils.validators import validate_request
from app.utils.responses import success_response, created_response, paginated_response, no_content_response
from app.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InsufficientPermissionsError,
    ValidationError,
    DatabaseError
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['POST'])
@validate_request(UsuarioRegistroSchema)
def registro():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - nombre
          properties:
            email:
              type: string
              example: usuario@solicitudes.com
            password:
              type: string
              example: password123
            nombre:
              type: string
              example: Juan
            apellido:
              type: string
              example: Pérez
            rol:
              type: string
              enum: [empleado, jefe, administrador]
              example: empleado
    responses:
      201:
        description: Usuario registrado exitosamente
      400:
        description: JSON inválido o mal formado
      409:
        description: El email ya está registrado
      422:
        description: Errores de validación en los datos
      500:
        description: Error interno del servidor
    """
    data = request.validated_data

    # Registrar usuario
    usuario, error = registrar_usuario(
        email=data['email'],
        password=data['password'],
        nombre=data['nombre'],
        apellido=data.get('apellido'),
        rol=data.get('rol', 'empleado')
    )

    if error:
        # Lanzar excepción apropiada
        if 'ya está registrado' in error.lower():
            raise UserAlreadyExistsError(message=error)
        else:
            raise DatabaseError(message=error)

    # Crear tokens
    tokens = crear_tokens(usuario)

    return created_response(
        data={
            'usuario': usuario.to_dict(),
            **tokens
        },
        message='Usuario registrado exitosamente'
    )


@auth_bp.route('/login', methods=['POST'])
@validate_request(UsuarioLoginSchema)
def login():
    """
    Iniciar sesión en el sistema
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: admin@solicitudes.com
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login exitoso
      400:
        description: JSON inválido o mal formado
      401:
        description: Credenciales incorrectas o usuario inactivo
      422:
        description: Errores de validación en los datos
    """
    data = request.validated_data

    # Autenticar usuario
    usuario, error = autenticar_usuario(data['email'], data['password'])

    if error:
        raise InvalidCredentialsError(message=error)

    # Crear tokens
    tokens = crear_tokens(usuario)

    return success_response(
        data={
            'usuario': usuario.to_dict(),
            **tokens
        },
        message='Login exitoso',
        status_code=200
    )


@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil():
    """
    Obtener perfil del usuario autenticado
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    responses:
      200:
        description: Datos del usuario
      401:
        description: Token JWT inválido o expirado
      404:
        description: Usuario no encontrado
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        raise UserNotFoundError()

    return success_response(
        data={'usuario': usuario.to_dict()}
    )


@auth_bp.route('/perfil', methods=['PUT'])
@jwt_required()
@validate_request(UsuarioUpdateSchema)
def actualizar_perfil():
    """
    Actualizar perfil del usuario autenticado
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: Juan
            apellido:
              type: string
              example: Pérez
    responses:
      200:
        description: Perfil actualizado exitosamente
      400:
        description: JSON inválido o mal formado
      401:
        description: Token JWT inválido o expirado
      404:
        description: Usuario no encontrado
      422:
        description: Errores de validación en los datos
      500:
        description: Error al actualizar en base de datos
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        raise UserNotFoundError()

    data = request.validated_data

    # Actualizar campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'apellido' in data:
        usuario.apellido = data['apellido']

    try:
        db.session.commit()
        return success_response(
            data={'usuario': usuario.to_dict()},
            message='Perfil actualizado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(message='Error al actualizar perfil', details={'error': str(e)})


@auth_bp.route('/cambiar-password', methods=['POST'])
@jwt_required()
@validate_request(CambiarPasswordSchema)
def cambiar_password_endpoint():
    """
    Cambiar contraseña del usuario autenticado
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - password_actual
            - password_nueva
          properties:
            password_actual:
              type: string
              example: password123
            password_nueva:
              type: string
              example: newpassword456
    responses:
      200:
        description: Contraseña cambiada exitosamente
      400:
        description: JSON inválido o mal formado
      401:
        description: Token JWT inválido o contraseña actual incorrecta
      404:
        description: Usuario no encontrado
      422:
        description: Errores de validación en los datos
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        raise UserNotFoundError()

    data = request.validated_data

    # Cambiar contraseña
    success, error = cambiar_password(
        usuario,
        data['password_actual'],
        data['password_nueva']
    )

    if error:
        # Si es contraseña incorrecta, usar 401 en lugar de 422
        raise InvalidCredentialsError(message=error)

    return success_response(message='Contraseña cambiada exitosamente')


@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def listar_usuarios():
    """
    Listar todos los usuarios (solo para jefes y administradores)
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    parameters:
      - in: query
        name: rol
        type: string
        enum: [empleado, jefe, administrador]
        description: Filtrar por rol
      - in: query
        name: activo
        type: boolean
        description: Filtrar por estado activo
      - in: query
        name: page
        type: integer
        default: 1
        description: Número de página
      - in: query
        name: per_page
        type: integer
        default: 10
        description: Items por página (máximo 100)
    responses:
      200:
        description: Lista de usuarios con metadata de paginación
      401:
        description: Token JWT inválido o expirado
      403:
        description: Sin permisos para listar usuarios
    """
    # Obtener parámetros de query
    rol = request.args.get('rol')
    activo = request.args.get('activo')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    # Construir query
    query = Usuario.query

    if rol:
        query = query.filter_by(rol=rol)

    if activo is not None:
        activo_bool = activo.lower() in ['true', '1', 'yes']
        query = query.filter_by(activo=activo_bool)

    # Paginación
    paginacion = query.paginate(page=page, per_page=per_page, error_out=False)

    return paginated_response(
        items=[usuario.to_dict() for usuario in paginacion.items],
        total=paginacion.total,
        page=page,
        per_page=per_page
    )


@auth_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def obtener_usuario(usuario_id):
    """
    Obtener un usuario específico (solo para jefes y administradores)
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    parameters:
      - in: path
        name: usuario_id
        type: integer
        required: true
        description: ID del usuario
    responses:
      200:
        description: Datos del usuario
      401:
        description: Token JWT inválido o expirado
      403:
        description: Sin permisos para ver este usuario
      404:
        description: Usuario no encontrado
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        raise UserNotFoundError()

    return success_response(data={'usuario': usuario.to_dict()})


@auth_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
@rol_requerido('administrador')
@validate_request(UsuarioUpdateSchema)
def actualizar_usuario(usuario_id):
    """
    Actualizar un usuario (solo para administradores)
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    parameters:
      - in: path
        name: usuario_id
        type: integer
        required: true
        description: ID del usuario
      - in: body
        name: body
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: Juan
            apellido:
              type: string
              example: Pérez
            rol:
              type: string
              enum: [empleado, jefe, administrador]
              example: jefe
            activo:
              type: boolean
              example: true
    responses:
      200:
        description: Usuario actualizado exitosamente
      400:
        description: JSON inválido o mal formado
      401:
        description: Token JWT inválido o expirado
      403:
        description: Sin permisos para actualizar usuarios
      404:
        description: Usuario no encontrado
      422:
        description: Errores de validación en los datos
      500:
        description: Error al actualizar en base de datos
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        raise UserNotFoundError()

    data = request.validated_data

    # Actualizar campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'apellido' in data:
        usuario.apellido = data['apellido']
    if 'rol' in data:
        usuario.rol = data['rol']
    if 'activo' in data:
        usuario.activo = data['activo']

    try:
        db.session.commit()
        return success_response(
            data={'usuario': usuario.to_dict()},
            message='Usuario actualizado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(message='Error al actualizar usuario', details={'error': str(e)})


@auth_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
@rol_requerido('administrador')
def eliminar_usuario(usuario_id):
    """
    Eliminar un usuario (solo para administradores)
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    parameters:
      - in: path
        name: usuario_id
        type: integer
        required: true
        description: ID del usuario a eliminar
    responses:
      204:
        description: Usuario eliminado exitosamente (sin contenido)
      401:
        description: Token JWT inválido o expirado
      403:
        description: Sin permisos para eliminar usuarios
      404:
        description: Usuario no encontrado
      500:
        description: Error al eliminar en base de datos
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        raise UserNotFoundError()

    try:
        db.session.delete(usuario)
        db.session.commit()
        return no_content_response()
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(message='Error al eliminar usuario', details={'error': str(e)})
