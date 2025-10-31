"""Blueprint de gestión de solicitudes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.solicitud import Solicitud
from app.models.usuario import Usuario
from app.services.auth_service import obtener_usuario_actual, rol_requerido
from app.tasks.email_tasks import enviar_email_solicitud

solicitudes_bp = Blueprint('solicitudes', __name__)


@solicitudes_bp.route('', methods=['POST'])
@jwt_required()
def crear_solicitud():
    """
    Crear una nueva solicitud.

    Headers:
        - Authorization: Bearer <access_token>

    Body:
        - tipo (str, requerido): Tipo de solicitud (compra, mantenimiento, soporte_tecnico, otro)
        - titulo (str, requerido): Título de la solicitud
        - descripcion (str, requerido): Descripción detallada
        - prioridad (str, opcional): Prioridad (baja, media, alta, urgente) - por defecto 'media'
        - fecha_requerida (str, opcional): Fecha requerida en formato ISO (YYYY-MM-DD)

    Returns:
        201: Solicitud creada exitosamente
        400: Datos inválidos
    """
    usuario = obtener_usuario_actual()
    data = request.get_json()

    # Validar campos requeridos
    campos_requeridos = ['tipo', 'titulo', 'descripcion']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    # Validar tipo
    tipos_validos = ['compra', 'mantenimiento', 'soporte_tecnico', 'otro']
    if data['tipo'] not in tipos_validos:
        return jsonify({'error': f'Tipo inválido. Debe ser uno de: {", ".join(tipos_validos)}'}), 400

    # Validar prioridad
    prioridad = data.get('prioridad', 'media')
    prioridades_validas = ['baja', 'media', 'alta', 'urgente']
    if prioridad not in prioridades_validas:
        return jsonify({'error': f'Prioridad inválida. Debe ser una de: {", ".join(prioridades_validas)}'}), 400

    # Crear solicitud
    solicitud = Solicitud(
        tipo=data['tipo'],
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        prioridad=prioridad,
        usuario_id=usuario.id
    )

    # Fecha requerida (opcional)
    if data.get('fecha_requerida'):
        try:
            fecha_requerida = datetime.strptime(data['fecha_requerida'], '%Y-%m-%d').date()
            solicitud.fecha_requerida = fecha_requerida
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    try:
        db.session.add(solicitud)
        db.session.commit()

        # Enviar notificación por email (asíncrono)
        enviar_email_solicitud.delay(solicitud.id, 'solicitud_creada')

        return jsonify({
            'message': 'Solicitud creada exitosamente',
            'solicitud': solicitud.to_dict(include_relations=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear solicitud: {str(e)}'}), 400


@solicitudes_bp.route('', methods=['GET'])
@jwt_required()
def listar_solicitudes():
    """
    Listar solicitudes del usuario autenticado o todas (si es jefe/admin).

    Headers:
        - Authorization: Bearer <access_token>

    Query params:
        - tipo (str, opcional): Filtrar por tipo
        - estado (str, opcional): Filtrar por estado
        - prioridad (str, opcional): Filtrar por prioridad
        - usuario_id (int, opcional): Filtrar por usuario (solo jefe/admin)
        - page (int, opcional): Número de página (por defecto 1)
        - per_page (int, opcional): Items por página (por defecto 10, máximo 100)

    Returns:
        200: Lista de solicitudes
    """
    usuario = obtener_usuario_actual()

    # Obtener parámetros de query
    tipo = request.args.get('tipo')
    estado = request.args.get('estado')
    prioridad = request.args.get('prioridad')
    usuario_id = request.args.get('usuario_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    # Construir query base
    query = Solicitud.query

    # Si no es jefe/admin, solo ver sus propias solicitudes
    if not usuario.puede_aprobar:
        query = query.filter_by(usuario_id=usuario.id)
    elif usuario_id:
        # Jefe/admin puede filtrar por usuario específico
        query = query.filter_by(usuario_id=usuario_id)

    # Filtros adicionales
    if tipo:
        query = query.filter_by(tipo=tipo)
    if estado:
        query = query.filter_by(estado=estado)
    if prioridad:
        query = query.filter_by(prioridad=prioridad)

    # Ordenar por fecha de creación (más recientes primero)
    query = query.order_by(Solicitud.created_at.desc())

    # Paginación
    paginacion = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'solicitudes': [sol.to_dict(include_relations=True) for sol in paginacion.items],
        'total': paginacion.total,
        'pages': paginacion.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@solicitudes_bp.route('/<int:solicitud_id>', methods=['GET'])
@jwt_required()
def obtener_solicitud(solicitud_id):
    """
    Obtener una solicitud específica.

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Datos de la solicitud
        403: Sin permisos para ver esta solicitud
        404: Solicitud no encontrada
    """
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    # Verificar permisos: solo el creador o jefe/admin pueden ver
    if not usuario.puede_aprobar and solicitud.usuario_id != usuario.id:
        return jsonify({'error': 'No tienes permisos para ver esta solicitud'}), 403

    return jsonify({'solicitud': solicitud.to_dict(include_relations=True)}), 200


@solicitudes_bp.route('/<int:solicitud_id>', methods=['PUT'])
@jwt_required()
def actualizar_solicitud(solicitud_id):
    """
    Actualizar una solicitud (solo el creador puede actualizar si está pendiente).

    Headers:
        - Authorization: Bearer <access_token>

    Body:
        - titulo (str, opcional): Nuevo título
        - descripcion (str, opcional): Nueva descripción
        - prioridad (str, opcional): Nueva prioridad
        - fecha_requerida (str, opcional): Nueva fecha requerida

    Returns:
        200: Solicitud actualizada
        400: Datos inválidos
        403: Sin permisos o solicitud ya procesada
        404: Solicitud no encontrada
    """
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    # Verificar permisos: solo el creador puede actualizar
    if solicitud.usuario_id != usuario.id:
        return jsonify({'error': 'No tienes permisos para actualizar esta solicitud'}), 403

    # No se puede actualizar si ya fue procesada
    if solicitud.estado != 'pendiente':
        return jsonify({'error': 'No se puede actualizar una solicitud que ya fue procesada'}), 403

    data = request.get_json()

    # Actualizar campos
    if 'titulo' in data:
        solicitud.titulo = data['titulo']
    if 'descripcion' in data:
        solicitud.descripcion = data['descripcion']
    if 'prioridad' in data:
        prioridades_validas = ['baja', 'media', 'alta', 'urgente']
        if data['prioridad'] not in prioridades_validas:
            return jsonify({'error': f'Prioridad inválida'}), 400
        solicitud.prioridad = data['prioridad']
    if 'fecha_requerida' in data:
        try:
            fecha_requerida = datetime.strptime(data['fecha_requerida'], '%Y-%m-%d').date()
            solicitud.fecha_requerida = fecha_requerida
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    try:
        db.session.commit()
        return jsonify({
            'message': 'Solicitud actualizada exitosamente',
            'solicitud': solicitud.to_dict(include_relations=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar solicitud: {str(e)}'}), 400


@solicitudes_bp.route('/<int:solicitud_id>', methods=['DELETE'])
@jwt_required()
def eliminar_solicitud(solicitud_id):
    """
    Eliminar una solicitud (solo el creador puede eliminar si está pendiente).

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Solicitud eliminada
        403: Sin permisos o solicitud ya procesada
        404: Solicitud no encontrada
    """
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    # Verificar permisos: solo el creador o admin pueden eliminar
    if solicitud.usuario_id != usuario.id and not usuario.es_admin:
        return jsonify({'error': 'No tienes permisos para eliminar esta solicitud'}), 403

    # Solo se puede eliminar si está pendiente (a menos que sea admin)
    if solicitud.estado != 'pendiente' and not usuario.es_admin:
        return jsonify({'error': 'No se puede eliminar una solicitud que ya fue procesada'}), 403

    try:
        db.session.delete(solicitud)
        db.session.commit()
        return jsonify({'message': 'Solicitud eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar solicitud: {str(e)}'}), 400


@solicitudes_bp.route('/<int:solicitud_id>/estado', methods=['PATCH'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def cambiar_estado_solicitud(solicitud_id):
    """
    Cambiar el estado de una solicitud (solo jefe/admin).

    Headers:
        - Authorization: Bearer <access_token>

    Body:
        - estado (str, requerido): Nuevo estado (aprobada, rechazada, en_proceso, completada)
        - comentarios (str, opcional): Comentarios adicionales

    Returns:
        200: Estado actualizado
        400: Estado inválido
        403: Sin permisos
        404: Solicitud no encontrada
    """
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    data = request.get_json()

    # Validar estado
    if not data.get('estado'):
        return jsonify({'error': 'El campo estado es requerido'}), 400

    estados_validos = ['aprobada', 'rechazada', 'en_proceso', 'completada']
    nuevo_estado = data['estado']

    if nuevo_estado not in estados_validos:
        return jsonify({'error': f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}'}), 400

    # Cambiar estado
    comentarios = data.get('comentarios')
    solicitud.cambiar_estado(nuevo_estado, usuario.id, comentarios)

    # Crear notificación in-app ANTES del commit para que ambos cambios estén en la misma transacción
    if nuevo_estado in ['aprobada', 'rechazada']:
        from app.models.notificacion import Notificacion

        tipo_notificacion = f'solicitud_{nuevo_estado}'
        titulo = f'Solicitud {nuevo_estado}'
        mensaje = f'Tu solicitud "{solicitud.titulo}" ha sido {nuevo_estado}'
        if comentarios:
            mensaje += f': {comentarios}'

        notificacion = Notificacion(
            tipo=tipo_notificacion,
            usuario_id=solicitud.usuario_id,
            titulo=titulo,
            mensaje=mensaje,
            solicitud_id=solicitud.id,
            leida=False
        )
        db.session.add(notificacion)

    try:
        # Commit único para ambos cambios (solicitud y notificación)
        db.session.commit()

        # Enviar notificación por email DESPUÉS del commit exitoso (asíncrono)
        if nuevo_estado in ['aprobada', 'rechazada']:
            tipo_notificacion = f'solicitud_{nuevo_estado}'
            enviar_email_solicitud.delay(solicitud.id, tipo_notificacion)

        return jsonify({
            'message': f'Solicitud {nuevo_estado} exitosamente',
            'solicitud': solicitud.to_dict(include_relations=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al cambiar estado: {str(e)}'}), 400


@solicitudes_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def obtener_estadisticas():
    """
    Obtener estadísticas de solicitudes (solo jefe/admin).

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Estadísticas
    """
    # Contar por estado
    total = Solicitud.query.count()
    pendientes = Solicitud.query.filter_by(estado='pendiente').count()
    aprobadas = Solicitud.query.filter_by(estado='aprobada').count()
    rechazadas = Solicitud.query.filter_by(estado='rechazada').count()
    en_proceso = Solicitud.query.filter_by(estado='en_proceso').count()
    completadas = Solicitud.query.filter_by(estado='completada').count()

    # Contar por tipo
    por_tipo = {}
    tipos = ['compra', 'mantenimiento', 'soporte_tecnico', 'otro']
    for tipo in tipos:
        por_tipo[tipo] = Solicitud.query.filter_by(tipo=tipo).count()

    # Contar por prioridad
    por_prioridad = {}
    prioridades = ['baja', 'media', 'alta', 'urgente']
    for prioridad in prioridades:
        por_prioridad[prioridad] = Solicitud.query.filter_by(prioridad=prioridad).count()

    return jsonify({
        'total': total,
        'por_estado': {
            'pendientes': pendientes,
            'aprobadas': aprobadas,
            'rechazadas': rechazadas,
            'en_proceso': en_proceso,
            'completadas': completadas
        },
        'por_tipo': por_tipo,
        'por_prioridad': por_prioridad
    }), 200
