"""Vistas de Flask-Admin para el panel de administración."""
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash
from app.models.usuario import Usuario
from app.models.solicitud import Solicitud
from app.models.notificacion import Notificacion
from app import bcrypt


class SecureModelView(ModelView):
    """Vista base con autenticación para Flask-Admin."""

    def is_accessible(self):
        """
        Verificar si el usuario tiene acceso al panel de admin.
        Solo jefes y administradores pueden acceder.
        """
        if 'user_id' not in session:
            return False

        user_id = session.get('user_id')
        user = Usuario.query.get(user_id)

        if not user or not user.activo:
            return False

        # Solo jefes y administradores tienen acceso
        return user.rol in ['jefe', 'administrador']

    def inaccessible_callback(self, name, **kwargs):
        """Redirigir al login si no tiene acceso."""
        flash('Debes iniciar sesión como jefe o administrador para acceder.', 'error')
        return redirect(url_for('admin.login_view'))


class UsuarioModelView(SecureModelView):
    """Vista de administración para Usuarios."""

    column_list = ['id', 'email', 'nombre', 'apellido', 'rol', 'activo', 'created_at']
    column_searchable_list = ['email', 'nombre', 'apellido']
    column_filters = ['rol', 'activo', 'created_at']
    column_editable_list = ['activo', 'rol']
    column_sortable_list = ['id', 'email', 'nombre', 'rol', 'created_at']

    # Campos a mostrar en el formulario de creación/edición
    form_columns = ['email', 'nombre', 'apellido', 'rol', 'activo']

    # Excluir el campo password_hash del formulario
    form_excluded_columns = ['password_hash', 'solicitudes', 'solicitudes_aprobadas']

    # Nombres de columnas más amigables
    column_labels = {
        'id': 'ID',
        'email': 'Email',
        'nombre': 'Nombre',
        'apellido': 'Apellido',
        'rol': 'Rol',
        'activo': 'Activo',
        'created_at': 'Fecha de Registro',
        'updated_at': 'Última Actualización'
    }

    # Valores por defecto
    form_args = {
        'rol': {
            'choices': [
                ('empleado', 'Empleado'),
                ('jefe', 'Jefe'),
                ('administrador', 'Administrador')
            ]
        }
    }

    # Paginación
    page_size = 20


class SolicitudModelView(SecureModelView):
    """Vista de administración para Solicitudes."""

    column_list = ['id', 'tipo', 'titulo', 'estado', 'prioridad', 'usuario_id', 'created_at']
    column_searchable_list = ['titulo', 'descripcion']
    column_filters = ['tipo', 'estado', 'prioridad', 'usuario_id', 'created_at']
    column_editable_list = ['estado', 'prioridad']
    column_sortable_list = ['id', 'tipo', 'estado', 'prioridad', 'created_at']

    # Campos a mostrar en el formulario
    form_columns = ['tipo', 'titulo', 'descripcion', 'estado', 'prioridad',
                    'comentarios', 'fecha_requerida', 'usuario_id', 'aprobador_id']

    # Nombres de columnas más amigables
    column_labels = {
        'id': 'ID',
        'tipo': 'Tipo',
        'titulo': 'Título',
        'descripcion': 'Descripción',
        'estado': 'Estado',
        'prioridad': 'Prioridad',
        'comentarios': 'Comentarios',
        'fecha_requerida': 'Fecha Requerida',
        'usuario_id': 'ID Solicitante',
        'aprobador_id': 'ID Aprobador',
        'created_at': 'Fecha de Creación',
        'updated_at': 'Última Actualización',
        'fecha_aprobacion': 'Fecha de Aprobación'
    }

    # Valores por defecto
    form_args = {
        'tipo': {
            'choices': [
                ('compra', 'Compra'),
                ('mantenimiento', 'Mantenimiento'),
                ('soporte_tecnico', 'Soporte Técnico'),
                ('otro', 'Otro')
            ]
        },
        'estado': {
            'choices': [
                ('pendiente', 'Pendiente'),
                ('aprobada', 'Aprobada'),
                ('rechazada', 'Rechazada'),
                ('en_proceso', 'En Proceso'),
                ('completada', 'Completada')
            ]
        },
        'prioridad': {
            'choices': [
                ('baja', 'Baja'),
                ('media', 'Media'),
                ('alta', 'Alta'),
                ('urgente', 'Urgente')
            ]
        }
    }

    # Paginación
    page_size = 20


class NotificacionModelView(SecureModelView):
    """Vista de administración para Notificaciones."""

    column_list = ['id', 'tipo', 'destinatario_email', 'asunto', 'enviado',
                   'intentos', 'created_at']
    column_searchable_list = ['destinatario_email', 'asunto', 'mensaje']
    column_filters = ['tipo', 'enviado', 'created_at']
    column_editable_list = ['enviado']
    column_sortable_list = ['id', 'tipo', 'enviado', 'intentos', 'created_at']

    # Campos a mostrar en el formulario (solo lectura principalmente)
    form_columns = ['tipo', 'destinatario_email', 'destinatario_nombre',
                    'asunto', 'mensaje', 'enviado', 'intentos',
                    'error_mensaje', 'solicitud_id']

    # Nombres de columnas más amigables
    column_labels = {
        'id': 'ID',
        'tipo': 'Tipo',
        'destinatario_email': 'Email Destinatario',
        'destinatario_nombre': 'Nombre Destinatario',
        'asunto': 'Asunto',
        'mensaje': 'Mensaje',
        'enviado': 'Enviado',
        'fecha_envio': 'Fecha de Envío',
        'intentos': 'Intentos',
        'error_mensaje': 'Mensaje de Error',
        'solicitud_id': 'ID Solicitud',
        'created_at': 'Fecha de Creación'
    }

    # Valores por defecto
    form_args = {
        'tipo': {
            'choices': [
                ('solicitud_creada', 'Solicitud Creada'),
                ('solicitud_aprobada', 'Solicitud Aprobada'),
                ('solicitud_rechazada', 'Solicitud Rechazada'),
                ('solicitud_actualizada', 'Solicitud Actualizada'),
                ('recordatorio', 'Recordatorio')
            ]
        }
    }

    # Paginación
    page_size = 20

    # Solo permitir ver y editar (no crear ni eliminar)
    can_create = False
    can_delete = False


class CustomAdminIndexView(AdminIndexView):
    """Vista personalizada para el índice del panel de administración."""

    def is_accessible(self):
        """Verificar si el usuario está autenticado como jefe o admin."""
        # Permitir acceso público a login y logout
        if request.endpoint in ['admin.login_view', 'admin.logout_view']:
            return True

        # Para otras rutas, verificar autenticación
        if 'user_id' not in session:
            return False

        user_id = session.get('user_id')
        user = Usuario.query.get(user_id)

        if not user or not user.activo:
            return False

        return user.rol in ['jefe', 'administrador']

    def inaccessible_callback(self, name, **kwargs):
        """Redirigir al login si no tiene acceso."""
        return redirect(url_for('admin.login_view'))

    @expose('/')
    def index(self):
        """Página principal del panel de administración."""
        # Obtener estadísticas básicas
        from app import db

        # Obtener usuario actual
        user_id = session.get('user_id')
        current_user = Usuario.query.get(user_id)

        total_usuarios = Usuario.query.count()
        total_solicitudes = Solicitud.query.count()
        solicitudes_pendientes = Solicitud.query.filter_by(estado='pendiente').count()
        total_notificaciones = Notificacion.query.count()
        notificaciones_pendientes = Notificacion.query.filter_by(enviado=False).count()

        return self.render('admin/index.html',
                         current_user=current_user,
                         total_usuarios=total_usuarios,
                         total_solicitudes=total_solicitudes,
                         solicitudes_pendientes=solicitudes_pendientes,
                         total_notificaciones=total_notificaciones,
                         notificaciones_pendientes=notificaciones_pendientes)

    @expose('/login', methods=['GET', 'POST'])
    def login_view(self):
        """Vista de login para el panel de administración."""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                flash('Por favor ingresa email y contraseña.', 'error')
                return self.render('admin/login.html')

            user = Usuario.query.filter_by(email=email).first()

            if not user:
                flash('Email o contraseña incorrectos.', 'error')
                return self.render('admin/login.html')

            if not user.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                return self.render('admin/login.html')

            if not user.check_password(password):
                flash('Email o contraseña incorrectos.', 'error')
                return self.render('admin/login.html')

            if user.rol not in ['jefe', 'administrador']:
                flash('No tienes permisos para acceder al panel de administración.', 'error')
                return self.render('admin/login.html')

            # Login exitoso
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_rol'] = user.rol
            session['user_nombre'] = user.nombre_completo

            flash(f'Bienvenido {user.nombre_completo}!', 'success')
            return redirect(url_for('admin.index'))

        return self.render('admin/login.html')

    @expose('/logout')
    def logout_view(self):
        """Cerrar sesión del panel de administración."""
        session.clear()
        flash('Has cerrado sesión exitosamente.', 'success')
        return redirect(url_for('admin.login_view'))


def configure_admin(admin, db):
    """
    Configurar las vistas de Flask-Admin.

    Args:
        admin: Instancia de Flask-Admin
        db: Instancia de SQLAlchemy
    """
    # Agregar vistas de modelos con endpoints únicos
    admin.add_view(UsuarioModelView(Usuario, db.session, name='Usuarios', category='Gestión', endpoint='usuarios_admin'))
    admin.add_view(SolicitudModelView(Solicitud, db.session, name='Solicitudes', category='Gestión', endpoint='solicitudes_admin'))
    admin.add_view(NotificacionModelView(Notificacion, db.session, name='Notificaciones', category='Sistema', endpoint='notificaciones_admin'))
