"""Blueprint de autenticación y gestión de usuarios."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
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

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['POST'])
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Usuario registrado exitosamente
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
            access_token:
              type: string
            refresh_token:
              type: string
            token_type:
              type: string
              example: Bearer
      400:
        description: Datos inválidos o email ya registrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()

    # Validar campos requeridos
    campos_requeridos = ['email', 'password', 'nombre']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    # Registrar usuario
    usuario, error = registrar_usuario(
        email=data['email'],
        password=data['password'],
        nombre=data['nombre'],
        apellido=data.get('apellido'),
        rol=data.get('rol', 'empleado')
    )

    if error:
        return jsonify({'error': error}), 400

    # Crear tokens
    tokens = crear_tokens(usuario)

    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict(),
        **tokens
    }), 201


@auth_bp.route('/login', methods=['POST'])
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Login exitoso
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
            access_token:
              type: string
            refresh_token:
              type: string
            token_type:
              type: string
              example: Bearer
      400:
        description: Datos inválidos
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Credenciales incorrectas
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()

    # Validar campos requeridos
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email y password son requeridos'}), 400

    # Autenticar usuario
    usuario, error = autenticar_usuario(data['email'], data['password'])

    if error:
        return jsonify({'error': error}), 401

    # Crear tokens
    tokens = crear_tokens(usuario)

    return jsonify({
        'message': 'Login exitoso',
        'usuario': usuario.to_dict(),
        **tokens
    }), 200


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
        schema:
          type: object
          properties:
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'usuario': usuario.to_dict()
    }), 200


@auth_bp.route('/perfil', methods=['PUT'])
@jwt_required()
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Perfil actualizado exitosamente
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
      400:
        description: Datos inválidos
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()

    # Actualizar campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'apellido' in data:
        usuario.apellido = data['apellido']

    try:
        db.session.commit()
        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar perfil: {str(e)}'}), 400


@auth_bp.route('/cambiar-password', methods=['POST'])
@jwt_required()
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Contraseña cambiada exitosamente
      400:
        description: Datos inválidos o contraseña actual incorrecta
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()

    # Validar campos requeridos
    if not data.get('password_actual') or not data.get('password_nueva'):
        return jsonify({'error': 'password_actual y password_nueva son requeridos'}), 400

    # Cambiar contraseña
    success, error = cambiar_password(
        usuario,
        data['password_actual'],
        data['password_nueva']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Contraseña cambiada exitosamente'}), 200


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
        description: Lista de usuarios
        schema:
          type: object
          properties:
            usuarios:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  email:
                    type: string
                  nombre:
                    type: string
                  apellido:
                    type: string
                  rol:
                    type: string
                  activo:
                    type: boolean
            total:
              type: integer
              example: 50
            pages:
              type: integer
              example: 5
            current_page:
              type: integer
              example: 1
            per_page:
              type: integer
              example: 10
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

    return jsonify({
        'usuarios': [usuario.to_dict() for usuario in paginacion.items],
        'total': paginacion.total,
        'pages': paginacion.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


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
        schema:
          type: object
          properties:
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'usuario': usuario.to_dict()}), 200


@auth_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
@rol_requerido('administrador')
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Usuario actualizado exitosamente
            usuario:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                nombre:
                  type: string
                apellido:
                  type: string
                rol:
                  type: string
                activo:
                  type: boolean
      400:
        description: Datos inválidos
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()

    # Actualizar campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'apellido' in data:
        usuario.apellido = data['apellido']
    if 'rol' in data:
        if data['rol'] not in ['empleado', 'jefe', 'administrador']:
            return jsonify({'error': 'Rol inválido'}), 400
        usuario.rol = data['rol']
    if 'activo' in data:
        usuario.activo = data['activo']

    try:
        db.session.commit()
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar usuario: {str(e)}'}), 400


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
      200:
        description: Usuario eliminado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: Usuario eliminado exitosamente
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Error al eliminar usuario
        schema:
          type: object
          properties:
            error:
              type: string
    """
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar usuario: {str(e)}'}), 400
