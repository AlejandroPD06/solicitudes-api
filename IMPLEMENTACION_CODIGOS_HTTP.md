# Implementación de Códigos HTTP Estándar - Solicitudes API

## Resumen

Se ha implementado un sistema robusto de manejo de códigos de estado HTTP según los estándares de IANA para la API de Solicitudes. Esta implementación mejora significativamente la calidad del código, la experiencia del desarrollador y el cumplimiento de estándares web.

## Archivos Creados

### 1. Sistema de Excepciones (`app/exceptions.py`)

Se creó un sistema completo de excepciones personalizadas que mapean automáticamente a códigos HTTP apropiados:

#### Excepciones de Cliente (4xx)
- `BadRequestError` (400) - Sintaxis incorrecta en la solicitud
- `UnauthorizedError` (401) - Autenticación requerida o fallida
- `ForbiddenError` (403) - Sin permisos para el recurso
- `NotFoundError` (404) - Recurso no encontrado
- `MethodNotAllowedError` (405) - Método HTTP no permitido
- `ConflictError` (409) - Conflicto con el estado actual
- `ValidationError` (422) - Errores semánticos de validación
- `TooManyRequestsError` (429) - Exceso de solicitudes

#### Excepciones de Servidor (5xx)
- `InternalServerError` (500) - Error genérico del servidor
- `NotImplementedError` (501) - Funcionalidad no implementada
- `ServiceUnavailableError` (503) - Servicio temporalmente no disponible

#### Excepciones Específicas del Dominio
- `UserAlreadyExistsError` (409)
- `UserNotFoundError` (404)
- `InvalidCredentialsError` (401)
- `InactiveUserError` (403)
- `InsufficientPermissionsError` (403)
- `SolicitudNotFoundError` (404)
- `SolicitudAlreadyProcessedError` (409)
- `NotificacionNotFoundError` (404)
- `DatabaseError` (500)

### 2. Schemas de Validación (`app/schemas/`)

Implementación de validación automática con Marshmallow:

#### `usuario_schema.py`
- `UsuarioRegistroSchema` - Validación de registro
- `UsuarioLoginSchema` - Validación de login
- `UsuarioUpdateSchema` - Validación de actualización
- `CambiarPasswordSchema` - Validación de cambio de contraseña

#### `solicitud_schema.py`
- `SolicitudCreateSchema` - Validación de creación
- `SolicitudUpdateSchema` - Validación de actualización
- `CambiarEstadoSchema` - Validación de cambio de estado

#### `notificacion_schema.py`
- `MarcarLeidaSchema` - Esquema para notificaciones

### 3. Utilidades (`app/utils/`)

#### `validators.py`
- `@validate_request(schema)` - Decorador para validación automática
- `@validate_json()` - Validación simple de JSON
- Manejo automático de errores de validación

#### `responses.py`
- `success_response()` - Respuestas exitosas consistentes
- `error_response()` - Respuestas de error estructuradas
- `paginated_response()` - Respuestas paginadas
- `created_response()` - Respuestas 201 Created
- `no_content_response()` - Respuestas 204 No Content
- Generación automática de request_id para tracking
- Timestamps en formato ISO 8601

#### `logger.py`
- `setup_logger()` - Configuración de logging
- `get_logger()` - Obtener instancia del logger
- `log_error()`, `log_info()`, `log_warning()`, `log_debug()` - Funciones de logging
- Rotación automática de archivos de log
- Logs separados para errores (errors.log) y operaciones (solicitudes_api.log)

### 4. Error Handlers Globales (`app/__init__.py`)

Manejadores centralizados de errores:
- `APIException` - Todas las excepciones personalizadas
- `JWTExtendedException` - Errores de JWT (401)
- `HTTPException` - Excepciones HTTP estándar de Werkzeug
- `404`, `405`, `500` - Códigos HTTP específicos
- `Exception` - Cualquier excepción no capturada
- Rollback automático de base de datos en errores
- No exposición de detalles técnicos en producción

## Archivos Actualizados

### 1. `app/routes/auth.py` ✅ COMPLETADO

Todos los endpoints actualizados con:
- Validación automática con schemas
- Códigos HTTP apropiados
- Excepciones específicas del dominio
- Respuestas estructuradas

#### Cambios por Endpoint:

**POST /registro**
- Código 201 (Created) para éxito
- Código 409 (Conflict) si email ya existe
- Código 422 (Validation Error) para errores de validación
- Validación automática con `UsuarioRegistroSchema`

**POST /login**
- Código 200 (OK) para éxito
- Código 401 (Unauthorized) para credenciales incorrectas
- Código 422 para errores de validación
- Validación automática con `UsuarioLoginSchema`

**GET /perfil**
- Código 200 (OK) para éxito
- Código 404 (Not Found) si usuario no existe
- Lanza `UserNotFoundError` en lugar de retornar JSON

**PUT /perfil**
- Código 200 (OK) para actualización exitosa
- Código 422 para errores de validación
- Código 500 (Internal Server Error) para errores de BD
- Validación automática con `UsuarioUpdateSchema`

**POST /cambiar-password**
- Código 200 (OK) para cambio exitoso
- Código 401 (Unauthorized) para contraseña incorrecta
- Código 422 para errores de validación
- Validación automática con `CambiarPasswordSchema`

**GET /usuarios**
- Código 200 (OK) con paginación
- Código 403 (Forbidden) si no tiene permisos
- Usa `paginated_response()` para respuesta estructurada

**GET /usuarios/:id**
- Código 200 (OK) para éxito
- Código 404 (Not Found) si usuario no existe
- Código 403 si no tiene permisos

**PUT /usuarios/:id**
- Código 200 (OK) para actualización exitosa
- Código 404 si usuario no existe
- Código 422 para errores de validación
- Código 500 para errores de BD
- Validación automática con `UsuarioUpdateSchema`

**DELETE /usuarios/:id**
- ⭐ Código 204 (No Content) para eliminación exitosa
- Código 404 si usuario no existe
- Código 500 para errores de BD
- Usa `no_content_response()`

### 2. `app/routes/solicitudes.py` ⏳ PENDIENTE

Se requiere aplicar el mismo patrón:
- Usar `@validate_request()` con schemas
- Reemplazar `jsonify()` con `success_response()`, `created_response()`, etc.
- Lanzar excepciones específicas en lugar de retornar JSON de error
- Código 201 para POST exitoso
- Código 204 para DELETE exitoso
- Código 409 para `SolicitudAlreadyProcessedError`
- Código 422 para errores de validación

### 3. `app/routes/notificaciones.py` ⏳ PENDIENTE

Mismos cambios que solicitudes.py

## Mapeo de Códigos HTTP Implementados

### Códigos de Éxito (2xx)
| Código | Uso | Ejemplo |
|--------|-----|---------|
| 200 OK | Operaciones exitosas (GET, PUT, PATCH) | `success_response()` |
| 201 Created | Recursos creados exitosamente (POST) | `created_response()` |
| 204 No Content | Eliminación exitosa (DELETE) | `no_content_response()` |

### Códigos de Error de Cliente (4xx)
| Código | Uso | Excepción |
|--------|-----|-----------|
| 400 Bad Request | JSON mal formado o sintaxis incorrecta | `BadRequestError` |
| 401 Unauthorized | Autenticación fallida o token inválido | `UnauthorizedError`, `InvalidCredentialsError` |
| 403 Forbidden | Sin permisos para el recurso | `ForbiddenError`, `InsufficientPermissionsError` |
| 404 Not Found | Recurso no encontrado | `NotFoundError`, `UserNotFoundError`, `SolicitudNotFoundError` |
| 405 Method Not Allowed | Método HTTP no soportado | `MethodNotAllowedError` |
| 409 Conflict | Conflicto de estado | `ConflictError`, `UserAlreadyExistsError`, `SolicitudAlreadyProcessedError` |
| 422 Unprocessable Entity | Errores semánticos de validación | `ValidationError` |
| 429 Too Many Requests | Rate limiting | `TooManyRequestsError` |

### Códigos de Error de Servidor (5xx)
| Código | Uso | Excepción |
|--------|-----|-----------|
| 500 Internal Server Error | Error genérico del servidor | `InternalServerError`, `DatabaseError` |
| 501 Not Implemented | Funcionalidad no implementada | `NotImplementedError` |
| 503 Service Unavailable | Servicio temporalmente no disponible | `ServiceUnavailableError` |

## Formato de Respuestas

### Respuesta Exitosa
```json
{
  "success": true,
  "timestamp": "2025-10-31T12:34:56.789Z",
  "message": "Operación exitosa",
  "data": {
    "usuario": {...}
  }
}
```

### Respuesta de Error
```json
{
  "success": false,
  "timestamp": "2025-10-31T12:34:56.789Z",
  "request_id": "uuid-123-456-789",
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": {}
  }
}
```

### Respuesta Paginada
```json
{
  "success": true,
  "timestamp": "2025-10-31T12:34:56.789Z",
  "data": [...],
  "meta": {
    "pagination": {
      "total": 100,
      "page": 1,
      "per_page": 10,
      "total_pages": 10,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

## Beneficios de la Implementación

### 1. Cumplimiento de Estándares
- ✅ Códigos HTTP según IANA
- ✅ Respuestas RESTful consistentes
- ✅ Separación clara entre errores de cliente (4xx) y servidor (5xx)

### 2. Mejor Experiencia del Desarrollador
- ✅ Validación automática elimina código repetitivo
- ✅ Excepciones específicas simplifican el manejo de errores
- ✅ Respuestas estructuradas fáciles de consumir
- ✅ Request IDs para tracking de errores

### 3. Mantenibilidad
- ✅ Código más limpio y DRY (Don't Repeat Yourself)
- ✅ Centralización del manejo de errores
- ✅ Fácil extensión con nuevas excepciones y schemas
- ✅ Logging estructurado para debugging

### 4. Seguridad
- ✅ No exposición de detalles técnicos en producción
- ✅ Validación robusta de entrada
- ✅ Logging de todos los errores para auditoría
- ✅ Rollback automático de transacciones en errores

### 5. Producción
- ✅ Logs rotativos para evitar llenar disco
- ✅ Separación de logs de errores y operaciones
- ✅ Timestamps en formato ISO 8601
- ✅ Tracking con request_id

## Próximos Pasos para Completar

### 1. Actualizar `app/routes/solicitudes.py`

Aplicar el mismo patrón que auth.py:

```python
# Imports
from app.schemas import SolicitudCreateSchema, SolicitudUpdateSchema, CambiarEstadoSchema
from app.utils.validators import validate_request
from app.utils.responses import success_response, created_response, paginated_response, no_content_response
from app.exceptions import SolicitudNotFoundError, SolicitudAlreadyProcessedError, ValidationError, DatabaseError

# Ejemplo de endpoint actualizado
@solicitudes_bp.route('', methods=['POST'])
@jwt_required()
@validate_request(SolicitudCreateSchema)
def crear_solicitud():
    usuario = obtener_usuario_actual()
    data = request.validated_data

    solicitud = Solicitud(
        tipo=data['tipo'],
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        prioridad=data.get('prioridad', 'media'),
        usuario_id=usuario.id,
        fecha_requerida=data.get('fecha_requerida')
    )

    try:
        db.session.add(solicitud)
        db.session.commit()
        enviar_email_solicitud.delay(solicitud.id, 'solicitud_creada')

        return created_response(
            data={'solicitud': solicitud.to_dict(include_relations=True)},
            message='Solicitud creada exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(message='Error al crear solicitud', details={'error': str(e)})
```

### 2. Actualizar `app/routes/notificaciones.py`

Similar a solicitudes.py.

### 3. Actualizar Documentación Swagger

Revisar todos los docstrings y asegurar que los códigos de respuesta estén documentados correctamente.

### 4. Testing

Crear tests para verificar:
- Códigos HTTP correctos
- Formato de respuestas
- Manejo de excepciones
- Validación de schemas

### 5. Actualizar README

Documentar los nuevos códigos HTTP y formatos de respuesta para los consumidores de la API.

## Referencia

- **Estándares HTTP**: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
- **RFC 7231**: Definición de códigos HTTP
- **RFC 7807**: Problem Details for HTTP APIs

## Conclusión

Esta implementación transforma la API de Solicitudes en un servicio RESTful profesional con:
- Manejo robusto de errores
- Validación automática
- Códigos HTTP apropiados
- Respuestas consistentes
- Logging estructurado
- Trazabilidad completa

El código es ahora más limpio, mantenible y cumple con los estándares internacionales de la industria web.
