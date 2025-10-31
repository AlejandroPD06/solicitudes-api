"""Blueprint de gestión de notificaciones."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.notificacion import Notificacion
from app.models.solicitud import Solicitud
from app.services.auth_service import obtener_usuario_actual, rol_requerido
from app.tasks.email_tasks import reenviar_notificacion

notificaciones_bp = Blueprint('notificaciones', __name__)


@notificaciones_bp.route('', methods=['GET'])
@jwt_required()
def listar_notificaciones():
    """
    Listar notificaciones (filtradas por usuario).

    Headers:
        - Authorization: Bearer <access_token>

    Query params:
        - tipo (str, opcional): Filtrar por tipo
        - leida (bool, opcional): Filtrar por estado de lectura
        - solicitud_id (int, opcional): Filtrar por solicitud
        - page (int, opcional): Número de página (por defecto 1)
        - per_page (int, opcional): Items por página (por defecto 10, máximo 100)

    Returns:
        200: Lista de notificaciones
    """
    usuario = obtener_usuario_actual()

    # Obtener parámetros de query
    tipo = request.args.get('tipo')
    leida = request.args.get('leida')
    solicitud_id = request.args.get('solicitud_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    # Construir query base - filtrar por usuario_id
    query = Notificacion.query.filter_by(usuario_id=usuario.id)

    # Filtros adicionales
    if tipo:
        query = query.filter_by(tipo=tipo)
    if leida is not None:
        leida_bool = leida.lower() in ['true', '1', 'yes']
        query = query.filter_by(leida=leida_bool)
    if solicitud_id:
        query = query.filter_by(solicitud_id=solicitud_id)

    # Ordenar por fecha de creación (más recientes primero)
    query = query.order_by(Notificacion.created_at.desc())

    # Paginación
    paginacion = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'notificaciones': [notif.to_dict(include_relations=True) for notif in paginacion.items],
        'total': paginacion.total,
        'pages': paginacion.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@notificaciones_bp.route('/<int:notificacion_id>', methods=['GET'])
@jwt_required()
def obtener_notificacion(notificacion_id):
    """
    Obtener una notificación específica.

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Datos de la notificación
        403: Sin permisos
        404: Notificación no encontrada
    """
    usuario = obtener_usuario_actual()
    notificacion = Notificacion.query.get(notificacion_id)

    if not notificacion:
        return jsonify({'error': 'Notificación no encontrada'}), 404

    # Verificar permisos - solo puede ver sus propias notificaciones
    if notificacion.usuario_id != usuario.id:
        return jsonify({'error': 'No tienes permisos para ver esta notificación'}), 403

    return jsonify({'notificacion': notificacion.to_dict(include_relations=True)}), 200


@notificaciones_bp.route('/<int:notificacion_id>/marcar-leida', methods=['PATCH'])
@jwt_required()
def marcar_notificacion_leida(notificacion_id):
    """
    Marcar una notificación como leída.

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Notificación marcada como leída
        403: Sin permisos
        404: Notificación no encontrada
    """
    usuario = obtener_usuario_actual()
    notificacion = Notificacion.query.get(notificacion_id)

    if not notificacion:
        return jsonify({'error': 'Notificación no encontrada'}), 404

    # Verificar permisos - solo puede marcar sus propias notificaciones
    if notificacion.usuario_id != usuario.id:
        return jsonify({'error': 'No tienes permisos para modificar esta notificación'}), 403

    # Marcar como leída
    notificacion.marcar_como_leida()

    try:
        db.session.commit()
        return jsonify({
            'message': 'Notificación marcada como leída',
            'notificacion': notificacion.to_dict(include_relations=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al marcar notificación: {str(e)}'}), 400


@notificaciones_bp.route('/<int:notificacion_id>/reenviar', methods=['POST'])
@jwt_required()
@rol_requerido('administrador')
def reenviar_notificacion_endpoint(notificacion_id):
    """
    Reenviar una notificación (solo administradores).

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Notificación reenviada
        404: Notificación no encontrada
    """
    notificacion = Notificacion.query.get(notificacion_id)

    if not notificacion:
        return jsonify({'error': 'Notificación no encontrada'}), 404

    # Reenviar notificación (asíncrono)
    reenviar_notificacion.delay(notificacion_id)

    return jsonify({'message': 'Notificación en proceso de reenvío'}), 200


@notificaciones_bp.route('/pendientes', methods=['GET'])
@jwt_required()
@rol_requerido('administrador')
def listar_notificaciones_pendientes():
    """
    Listar notificaciones pendientes de envío (solo administradores).

    Headers:
        - Authorization: Bearer <access_token>

    Query params:
        - max_intentos (int, opcional): Filtrar por máximo de intentos (por defecto 3)

    Returns:
        200: Lista de notificaciones pendientes
    """
    max_intentos = request.args.get('max_intentos', 3, type=int)

    # Notificaciones no enviadas con menos de X intentos
    notificaciones = Notificacion.query.filter(
        Notificacion.enviado == False,
        Notificacion.intentos < max_intentos
    ).order_by(Notificacion.created_at.desc()).all()

    return jsonify({
        'notificaciones': [notif.to_dict(include_relations=True) for notif in notificaciones],
        'total': len(notificaciones)
    }), 200


@notificaciones_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def obtener_estadisticas_notificaciones():
    """
    Obtener estadísticas de notificaciones (solo jefe/admin).

    Headers:
        - Authorization: Bearer <access_token>

    Returns:
        200: Estadísticas
    """
    total = Notificacion.query.count()
    enviadas = Notificacion.query.filter_by(enviado=True).count()
    pendientes = Notificacion.query.filter_by(enviado=False).count()

    # Contar por tipo
    por_tipo = {}
    tipos = ['solicitud_creada', 'solicitud_aprobada', 'solicitud_rechazada',
             'solicitud_actualizada', 'recordatorio']
    for tipo in tipos:
        por_tipo[tipo] = Notificacion.query.filter_by(tipo=tipo).count()

    # Notificaciones con errores (intentos > 0 y no enviadas)
    con_errores = Notificacion.query.filter(
        Notificacion.enviado == False,
        Notificacion.intentos > 0
    ).count()

    return jsonify({
        'total': total,
        'enviadas': enviadas,
        'pendientes': pendientes,
        'con_errores': con_errores,
        'por_tipo': por_tipo
    }), 200
