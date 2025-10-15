"""Blueprint para el frontend de empleados."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.models.usuario import Usuario
from app.models.solicitud import Solicitud
from app import db, bcrypt
from datetime import datetime

frontend_bp = Blueprint('frontend', __name__)


def login_required(f):
    """Decorator para requerir login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'frontend_user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'error')
            return redirect(url_for('frontend.login'))
        return f(*args, **kwargs)
    return decorated_function


@frontend_bp.route('/')
def index():
    """Página de inicio - redirige a login o dashboard."""
    if 'frontend_user_id' in session:
        return redirect(url_for('frontend.dashboard'))
    return redirect(url_for('frontend.login'))


@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login para empleados."""
    # Si ya está logueado, redirigir al dashboard
    if 'frontend_user_id' in session:
        return redirect(url_for('frontend.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor ingresa email y contraseña.', 'error')
            return render_template('frontend/login.html')

        user = Usuario.query.filter_by(email=email).first()

        if not user:
            flash('Email o contraseña incorrectos.', 'error')
            return render_template('frontend/login.html')

        if not user.activo:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
            return render_template('frontend/login.html')

        if not user.check_password(password):
            flash('Email o contraseña incorrectos.', 'error')
            return render_template('frontend/login.html')

        # Login exitoso
        session['frontend_user_id'] = user.id
        session['frontend_user_email'] = user.email
        session['frontend_user_rol'] = user.rol
        session['frontend_user_nombre'] = user.nombre_completo

        flash(f'Bienvenido {user.nombre_completo}!', 'success')
        return redirect(url_for('frontend.dashboard'))

    return render_template('frontend/login.html')


@frontend_bp.route('/logout')
def logout():
    """Cerrar sesión."""
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('frontend.login'))


@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del empleado."""
    user_id = session.get('frontend_user_id')
    user = Usuario.query.get(user_id)

    # Obtener estadísticas del usuario
    mis_solicitudes = Solicitud.query.filter_by(usuario_id=user_id).all()
    total_solicitudes = len(mis_solicitudes)
    pendientes = len([s for s in mis_solicitudes if s.estado == 'pendiente'])
    aprobadas = len([s for s in mis_solicitudes if s.estado == 'aprobada'])
    rechazadas = len([s for s in mis_solicitudes if s.estado == 'rechazada'])
    en_proceso = len([s for s in mis_solicitudes if s.estado == 'en_proceso'])

    # Solicitudes recientes (últimas 5)
    solicitudes_recientes = Solicitud.query.filter_by(usuario_id=user_id)\
        .order_by(Solicitud.created_at.desc())\
        .limit(5)\
        .all()

    return render_template('frontend/dashboard.html',
                         user=user,
                         total_solicitudes=total_solicitudes,
                         pendientes=pendientes,
                         aprobadas=aprobadas,
                         rechazadas=rechazadas,
                         en_proceso=en_proceso,
                         solicitudes_recientes=solicitudes_recientes)


@frontend_bp.route('/solicitudes')
@login_required
def mis_solicitudes():
    """Ver todas las solicitudes del usuario."""
    user_id = session.get('frontend_user_id')

    # Filtros
    estado_filter = request.args.get('estado', '')
    tipo_filter = request.args.get('tipo', '')

    query = Solicitud.query.filter_by(usuario_id=user_id)

    if estado_filter:
        query = query.filter_by(estado=estado_filter)

    if tipo_filter:
        query = query.filter_by(tipo=tipo_filter)

    solicitudes = query.order_by(Solicitud.created_at.desc()).all()

    return render_template('frontend/solicitudes.html',
                         solicitudes=solicitudes,
                         estado_filter=estado_filter,
                         tipo_filter=tipo_filter)


@frontend_bp.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
def nueva_solicitud():
    """Crear una nueva solicitud."""
    if request.method == 'POST':
        user_id = session.get('frontend_user_id')

        tipo = request.form.get('tipo')
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        prioridad = request.form.get('prioridad', 'media')
        fecha_requerida_str = request.form.get('fecha_requerida')

        # Validaciones
        if not tipo or not titulo or not descripcion:
            flash('Todos los campos obligatorios deben ser completados.', 'error')
            return render_template('frontend/nueva_solicitud.html')

        # Parsear fecha si fue proporcionada
        fecha_requerida = None
        if fecha_requerida_str:
            try:
                fecha_requerida = datetime.strptime(fecha_requerida_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido.', 'error')
                return render_template('frontend/nueva_solicitud.html')

        # Crear la solicitud
        nueva = Solicitud(
            tipo=tipo,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            fecha_requerida=fecha_requerida,
            usuario_id=user_id,
            estado='pendiente'
        )

        db.session.add(nueva)
        db.session.commit()

        # Enviar notificación asíncrona
        try:
            from app.tasks.email_tasks import enviar_email_solicitud
            enviar_email_solicitud.delay(nueva.id, 'solicitud_creada')
        except Exception as e:
            print(f"Error enviando notificación: {e}")

        flash('Solicitud creada exitosamente!', 'success')
        return redirect(url_for('frontend.mis_solicitudes'))

    return render_template('frontend/nueva_solicitud.html')


@frontend_bp.route('/solicitudes/<int:id>')
@login_required
def ver_solicitud(id):
    """Ver detalles de una solicitud."""
    user_id = session.get('frontend_user_id')
    solicitud = Solicitud.query.get_or_404(id)

    # Verificar que la solicitud pertenece al usuario
    if solicitud.usuario_id != user_id:
        flash('No tienes permiso para ver esta solicitud.', 'error')
        return redirect(url_for('frontend.mis_solicitudes'))

    return render_template('frontend/detalle_solicitud.html', solicitud=solicitud)


@frontend_bp.route('/perfil')
@login_required
def perfil():
    """Ver y editar perfil del usuario."""
    user_id = session.get('frontend_user_id')
    user = Usuario.query.get(user_id)

    return render_template('frontend/perfil.html', user=user)


@frontend_bp.route('/perfil/actualizar', methods=['POST'])
@login_required
def actualizar_perfil():
    """Actualizar información del perfil."""
    user_id = session.get('frontend_user_id')
    user = Usuario.query.get(user_id)

    user.nombre = request.form.get('nombre', user.nombre)
    user.apellido = request.form.get('apellido', user.apellido)

    password_actual = request.form.get('password_actual')
    password_nueva = request.form.get('password_nueva')

    if password_actual and password_nueva:
        if user.check_password(password_actual):
            user.set_password(password_nueva)
            flash('Contraseña actualizada exitosamente.', 'success')
        else:
            flash('Contraseña actual incorrecta.', 'error')
            return redirect(url_for('frontend.perfil'))

    db.session.commit()

    # Actualizar sesión
    session['frontend_user_nombre'] = user.nombre_completo

    flash('Perfil actualizado exitosamente.', 'success')
    return redirect(url_for('frontend.perfil'))
