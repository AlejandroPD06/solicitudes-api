# Guía para Completar la Actualización de Códigos HTTP

## Archivos Pendientes

1. ⏳ `app/routes/solicitudes.py`
2. ⏳ `app/routes/notificaciones.py`

## Patrón a Seguir

### Antes (Código Antiguo)
```python
@solicitudes_bp.route('', methods=['POST'])
@jwt_required()
def crear_solicitud():
    usuario = obtener_usuario_actual()
    data = request.get_json()

    # Validación manual
    campos_requeridos = ['tipo', 'titulo', 'descripcion']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    # Validar tipo
    tipos_validos = ['compra', 'mantenimiento', 'soporte_tecnico', 'otro']
    if data['tipo'] not in tipos_validos:
        return jsonify({'error': f'Tipo inválido'}), 400

    solicitud = Solicitud(
        tipo=data['tipo'],
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        usuario_id=usuario.id
    )

    try:
        db.session.add(solicitud)
        db.session.commit()
        return jsonify({
            'message': 'Solicitud creada exitosamente',
            'solicitud': solicitud.to_dict()
        }), 201  # ✅ Este código está bien
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400  # ❌ Debería ser 500
```

### Después (Código Nuevo)
```python
@solicitudes_bp.route('', methods=['POST'])
@jwt_required()
@validate_request(SolicitudCreateSchema)  # ✅ Validación automática
def crear_solicitud():
    usuario = obtener_usuario_actual()
    data = request.validated_data  # ✅ Datos ya validados

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

        # Enviar notificación asíncrona
        enviar_email_solicitud.delay(solicitud.id, 'solicitud_creada')

        return created_response(  # ✅ 201 Created
            data={'solicitud': solicitud.to_dict(include_relations=True)},
            message='Solicitud creada exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(  # ✅ 500 Internal Server Error
            message='Error al crear solicitud',
            details={'error': str(e)}
        )
```

## Checklist de Cambios por Endpoint

### Para cada endpoint, verificar:

- [ ] Agregar `@validate_request(Schema)` si recibe body
- [ ] Reemplazar `request.get_json()` con `request.validated_data`
- [ ] Eliminar validación manual de campos
- [ ] Reemplazar `jsonify()` con funciones de respuesta apropiadas:
  - `success_response()` para GET, PUT, PATCH exitosos
  - `created_response()` para POST exitoso
  - `no_content_response()` para DELETE exitoso
  - `paginated_response()` para listados con paginación
- [ ] Reemplazar `return jsonify({'error': ...}), 4xx` con `raise Exception(...)`
- [ ] Reemplazar errores de BD (try/except) con `raise DatabaseError(...)`
- [ ] Actualizar docstring con códigos HTTP correctos

## Mapeo de Códigos HTTP Antiguo → Nuevo

### Códigos que YA están correctos
```python
# POST exitoso
return jsonify({...}), 201  # ✅ Correcto
# Cambiar a: return created_response(data={...}, message='...')

# GET exitoso
return jsonify({...}), 200  # ✅ Correcto
# Cambiar a: return success_response(data={...})
```

### Códigos que necesitan cambio
```python
# Errores de validación
return jsonify({'error': '...'}), 400  # ❌ Usar 422
# Cambiar a: raise ValidationError(message='...')

# Errores de BD
except Exception as e:
    return jsonify({'error': str(e)}), 400  # ❌ Usar 500
# Cambiar a: raise DatabaseError(message='...', details={...})

# Recurso no encontrado
if not solicitud:
    return jsonify({'error': '...'}), 404  # ❌ Formato incorrecto
# Cambiar a: raise SolicitudNotFoundError()

# Conflicto de estado
if solicitud.estado != 'pendiente':
    return jsonify({'error': '...'}), 403  # ❌ Usar 409
# Cambiar a: raise SolicitudAlreadyProcessedError()

# DELETE exitoso
return jsonify({'message': '...'}), 200  # ❌ Usar 204
# Cambiar a: return no_content_response()
```

## Ejemplos Específicos para app/routes/solicitudes.py

### 1. Endpoint GET /:id

**Antes:**
```python
@solicitudes_bp.route('/<int:solicitud_id>', methods=['GET'])
@jwt_required()
def obtener_solicitud(solicitud_id):
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    # Verificar permisos
    if not usuario.puede_aprobar and solicitud.usuario_id != usuario.id:
        return jsonify({'error': 'No tienes permisos'}), 403

    return jsonify({'solicitud': solicitud.to_dict(include_relations=True)}), 200
```

**Después:**
```python
@solicitudes_bp.route('/<int:solicitud_id>', methods=['GET'])
@jwt_required()
def obtener_solicitud(solicitud_id):
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        raise SolicitudNotFoundError()

    # Verificar permisos
    if not usuario.puede_aprobar and solicitud.usuario_id != usuario.id:
        raise InsufficientPermissionsError(
            message='No tienes permisos para ver esta solicitud'
        )

    return success_response(
        data={'solicitud': solicitud.to_dict(include_relations=True)}
    )
```

### 2. Endpoint PATCH /:id/estado

**Antes:**
```python
@solicitudes_bp.route('/<int:solicitud_id>/estado', methods=['PATCH'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def cambiar_estado_solicitud(solicitud_id):
    data = request.get_json()

    if not data.get('nuevo_estado'):
        return jsonify({'error': 'nuevo_estado es requerido'}), 400

    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    if solicitud.estado != 'pendiente':
        return jsonify({'error': 'Solo se pueden cambiar solicitudes pendientes'}), 403

    # Cambiar estado
    solicitud.estado = data['nuevo_estado']

    try:
        db.session.commit()
        return jsonify({'solicitud': solicitud.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

**Después:**
```python
@solicitudes_bp.route('/<int:solicitud_id>/estado', methods=['PATCH'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
@validate_request(CambiarEstadoSchema)
def cambiar_estado_solicitud(solicitud_id):
    data = request.validated_data
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        raise SolicitudNotFoundError()

    if solicitud.estado != 'pendiente':
        raise SolicitudAlreadyProcessedError(
            message='Solo se pueden cambiar solicitudes pendientes'
        )

    # Cambiar estado
    solicitud.estado = data['nuevo_estado']
    if data.get('comentarios'):
        solicitud.comentarios = data['comentarios']

    try:
        db.session.commit()

        # Enviar notificación
        enviar_email_solicitud.delay(solicitud.id, f'solicitud_{solicitud.estado}')

        return success_response(
            data={'solicitud': solicitud.to_dict(include_relations=True)},
            message=f'Solicitud {solicitud.estado} exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(
            message='Error al cambiar estado',
            details={'error': str(e)}
        )
```

### 3. Endpoint DELETE /:id

**Antes:**
```python
@solicitudes_bp.route('/<int:solicitud_id>', methods=['DELETE'])
@jwt_required()
def eliminar_solicitud(solicitud_id):
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404

    # Solo el creador o admin puede eliminar
    if solicitud.usuario_id != usuario.id and usuario.rol != 'administrador':
        return jsonify({'error': 'No tienes permisos'}), 403

    try:
        db.session.delete(solicitud)
        db.session.commit()
        return jsonify({'message': 'Solicitud eliminada'}), 200  # ❌ Debería ser 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

**Después:**
```python
@solicitudes_bp.route('/<int:solicitud_id>', methods=['DELETE'])
@jwt_required()
def eliminar_solicitud(solicitud_id):
    usuario = obtener_usuario_actual()
    solicitud = Solicitud.query.get(solicitud_id)

    if not solicitud:
        raise SolicitudNotFoundError()

    # Solo el creador o admin puede eliminar
    if solicitud.usuario_id != usuario.id and usuario.rol != 'administrador':
        raise InsufficientPermissionsError(
            message='Solo el creador o un administrador puede eliminar esta solicitud'
        )

    try:
        db.session.delete(solicitud)
        db.session.commit()
        return no_content_response()  # ✅ 204 No Content
    except Exception as e:
        db.session.rollback()
        raise DatabaseError(
            message='Error al eliminar solicitud',
            details={'error': str(e)}
        )
```

## Imports Necesarios

Al inicio de cada archivo blueprint, agregar:

```python
from app.schemas import (
    SolicitudCreateSchema,
    SolicitudUpdateSchema,
    CambiarEstadoSchema,
    # ... otros schemas necesarios
)
from app.utils.validators import validate_request
from app.utils.responses import (
    success_response,
    created_response,
    paginated_response,
    no_content_response
)
from app.exceptions import (
    SolicitudNotFoundError,
    SolicitudAlreadyProcessedError,
    InsufficientPermissionsError,
    ValidationError,
    DatabaseError,
    # ... otras excepciones necesarias
)
```

## Actualizar Docstrings Swagger

Ejemplo de docstring actualizado:

```python
def crear_solicitud():
    """
    Crear una nueva solicitud
    ---
    tags:
      - Solicitudes
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - tipo
            - titulo
            - descripcion
          properties:
            tipo:
              type: string
              enum: [compra, mantenimiento, soporte_tecnico, otro]
            titulo:
              type: string
            descripcion:
              type: string
            prioridad:
              type: string
              enum: [baja, media, alta, urgente]
            fecha_requerida:
              type: string
              format: date
    responses:
      201:
        description: Solicitud creada exitosamente
      400:
        description: JSON mal formado
      401:
        description: Token JWT inválido o expirado
      422:
        description: Errores de validación en los datos
      500:
        description: Error interno del servidor
    """
```

## Testing

Después de actualizar cada archivo, probar:

```bash
# 1. Levantar la aplicación
python wsgi.py

# 2. Probar endpoints con curl o Postman
# POST con datos válidos → 201
# POST con datos inválidos → 422
# GET con recurso existente → 200
# GET con recurso inexistente → 404
# DELETE exitoso → 204
# Operación sin permisos → 403
# Error de BD → 500
```

## Orden Recomendado

1. ✅ **COMPLETADO**: `app/exceptions.py`
2. ✅ **COMPLETADO**: `app/schemas/`
3. ✅ **COMPLETADO**: `app/utils/`
4. ✅ **COMPLETADO**: `app/__init__.py` (error handlers)
5. ✅ **COMPLETADO**: `app/routes/auth.py`
6. ⏳ **PENDIENTE**: `app/routes/solicitudes.py`
7. ⏳ **PENDIENTE**: `app/routes/notificaciones.py`
8. ⏳ **PENDIENTE**: Actualizar docstrings Swagger
9. ⏳ **PENDIENTE**: Testing completo
10. ⏳ **PENDIENTE**: Actualizar README.md con nueva documentación

## Recursos Adicionales

- **IANA HTTP Status Codes**: https://www.iana.org/assignments/http-status-codes/
- **RFC 7231 (HTTP/1.1 Semantics)**: https://tools.ietf.org/html/rfc7231
- **RFC 7807 (Problem Details)**: https://tools.ietf.org/html/rfc7807
- **Marshmallow Docs**: https://marshmallow.readthedocs.io/
- **Flask Best Practices**: https://flask.palletsprojects.com/en/2.3.x/patterns/

## Conclusión

Siguiendo este patrón de manera consistente en todos los archivos, la API tendrá:
- ✅ Códigos HTTP semánticamente correctos
- ✅ Validación automática robusta
- ✅ Respuestas estructuradas y consistentes
- ✅ Manejo centralizado de errores
- ✅ Trazabilidad completa con logging
- ✅ Código limpio y mantenible

¡Buena suerte con la implementación!
