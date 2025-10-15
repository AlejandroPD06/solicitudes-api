"""Punto de entrada WSGI para la aplicación."""
import os
from app import create_app, db

# Crear la aplicación
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Crear contexto para Flask shell."""
    from app.models.usuario import Usuario
    from app.models.solicitud import Solicitud
    from app.models.notificacion import Notificacion

    return {
        'db': db,
        'Usuario': Usuario,
        'Solicitud': Solicitud,
        'Notificacion': Notificacion
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
