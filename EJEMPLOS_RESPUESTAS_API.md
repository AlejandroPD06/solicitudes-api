# Ejemplos de Respuestas de la API

## Comparación Antes vs Después

### 1. Registro de Usuario Exitoso

#### ANTES (Inconsistente)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "email": "usuario@test.com",
    "nombre": "Juan",
    "rol": "empleado"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "token_type": "Bearer"
}
```

#### DESPUÉS (Estructurado)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "timestamp": "2025-10-31T14:30:45.123Z",
  "message": "Usuario registrado exitosamente",
  "data": {
    "usuario": {
      "id": 1,
      "email": "usuario@test.com",
      "nombre": "Juan",
      "apellido": null,
      "rol": "empleado",
      "activo": true,
      "created_at": "2025-10-31T14:30:45.123Z"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
    "token_type": "Bearer"
  }
}
```

**Mejoras**:
- ✅ Campo `success` para identificación rápida
- ✅ `timestamp` en ISO 8601
- ✅ Datos bajo `data` (estructura consistente)
- ✅ Código 201 correcto para creación

---

### 2. Error de Validación

#### ANTES (Código HTTP Incorrecto)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "email-invalido",
  "password": "123"
}
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "El campo nombre es requerido"
}
```

**Problemas**:
- ❌ 400 se usa para JSON mal formado, no validación
- ❌ Mensaje simple sin detalles
- ❌ No hay timestamp ni request_id

#### DESPUÉS (Código HTTP Correcto)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "email-invalido",
  "password": "123"
}
```

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T14:35:12.456Z",
  "request_id": "a3f2d891-3c4e-4b2a-8f1e-9d4c2a1b3e5f",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "errors": {
        "email": ["El formato del email no es válido"],
        "password": ["La contraseña debe tener al menos 6 caracteres"],
        "nombre": ["El nombre es requerido"]
      }
    }
  }
}
```

**Mejoras**:
- ✅ Código 422 (Unprocessable Entity) semánticamente correcto
- ✅ Todos los errores de validación en un solo response
- ✅ `request_id` para debugging
- ✅ Código de error `VALIDATION_ERROR` consistente
- ✅ Detalles estructurados por campo

---

### 3. Email Ya Registrado

#### ANTES (Código HTTP Incorrecto)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "existente@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "El email ya está registrado"
}
```

**Problemas**:
- ❌ 400 no representa un conflicto
- ❌ Debería ser 409 Conflict

#### DESPUÉS (Código HTTP Correcto)
```http
POST /api/usuarios/registro HTTP/1.1
Content-Type: application/json

{
  "email": "existente@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T14:40:23.789Z",
  "request_id": "b7e3f892-4d5f-5c3b-9g2f-8e5d3b2c4f6g",
  "error": {
    "code": "USER_ALREADY_EXISTS",
    "message": "El email ya está registrado en el sistema",
    "details": {}
  }
}
```

**Mejoras**:
- ✅ Código 409 (Conflict) semánticamente correcto
- ✅ Código de error específico `USER_ALREADY_EXISTS`
- ✅ Mensaje claro del conflicto

---

### 4. Login Exitoso

#### ANTES
```http
POST /api/usuarios/login HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "123456"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Login exitoso",
  "usuario": {...},
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer"
}
```

#### DESPUÉS
```http
POST /api/usuarios/login HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "123456"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "timestamp": "2025-10-31T14:45:30.123Z",
  "message": "Login exitoso",
  "data": {
    "usuario": {
      "id": 1,
      "email": "usuario@test.com",
      "nombre": "Juan",
      "apellido": null,
      "rol": "empleado",
      "activo": true
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
    "token_type": "Bearer"
  }
}
```

**Mejoras**:
- ✅ Estructura consistente con otros endpoints
- ✅ Timestamp para auditoría
- ✅ Campo `success` para parsing rápido

---

### 5. Credenciales Incorrectas

#### ANTES (Código Correcto)
```http
POST /api/usuarios/login HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "incorrecta"
}
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Email o contraseña incorrectos"
}
```

#### DESPUÉS (Mejorado)
```http
POST /api/usuarios/login HTTP/1.1
Content-Type: application/json

{
  "email": "usuario@test.com",
  "password": "incorrecta"
}
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T14:50:15.456Z",
  "request_id": "c8f4g903-5e6g-6d4c-0h3g-9f6e4c3d5g7h",
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email o contraseña incorrectos",
    "details": {}
  }
}
```

**Mejoras**:
- ✅ Código 401 ya era correcto
- ✅ Estructura de error consistente
- ✅ Código específico `INVALID_CREDENTIALS`

---

### 6. Token JWT Inválido

#### ANTES
```http
GET /api/usuarios/perfil HTTP/1.1
Authorization: Bearer token_invalido_o_expirado
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "msg": "Token has expired"
}
```

**Problemas**:
- ❌ Campo `msg` no es estándar
- ❌ Mensaje técnico en inglés

#### DESPUÉS
```http
GET /api/usuarios/perfil HTTP/1.1
Authorization: Bearer token_invalido_o_expirado
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T14:55:30.789Z",
  "request_id": "d9g5h014-6f7h-7e5d-1i4h-0g7f5d4e6h8i",
  "error": {
    "code": "JWT_ERROR",
    "message": "Token has expired",
    "details": {}
  }
}
```

**Mejoras**:
- ✅ Estructura de error consistente
- ✅ Código de error específico `JWT_ERROR`
- ✅ Request ID para debugging

---

### 7. Sin Permisos

#### ANTES
```http
GET /api/usuarios/usuarios HTTP/1.1
Authorization: Bearer <token_empleado>
```

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "No tienes permisos para realizar esta acción",
  "rol_requerido": ["jefe", "administrador"],
  "tu_rol": "empleado"
}
```

#### DESPUÉS
```http
GET /api/usuarios/usuarios HTTP/1.1
Authorization: Bearer <token_empleado>
```

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T15:00:45.123Z",
  "request_id": "e0h6i125-7g8i-8f6e-2j5i-1h8g6e5f7i9j",
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "No tienes permisos suficientes para realizar esta acción",
    "details": {
      "rol_requerido": ["jefe", "administrador"],
      "tu_rol": "empleado"
    }
  }
}
```

**Mejoras**:
- ✅ Código 403 ya era correcto
- ✅ Información de permisos en `details`
- ✅ Código específico `INSUFFICIENT_PERMISSIONS`

---

### 8. Recurso No Encontrado

#### ANTES
```http
GET /api/usuarios/usuarios/999 HTTP/1.1
Authorization: Bearer <token_admin>
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "Usuario no encontrado"
}
```

#### DESPUÉS
```http
GET /api/usuarios/usuarios/999 HTTP/1.1
Authorization: Bearer <token_admin>
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T15:05:20.456Z",
  "request_id": "f1i7j236-8h9j-9g7f-3k6j-2i9h7f6g8j0k",
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": {}
  }
}
```

**Mejoras**:
- ✅ Código 404 ya era correcto
- ✅ Código específico `USER_NOT_FOUND`
- ✅ Estructura consistente

---

### 9. Listado con Paginación

#### ANTES (Estructura Plana)
```http
GET /api/usuarios/usuarios?page=2&per_page=10 HTTP/1.1
Authorization: Bearer <token_jefe>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "usuarios": [...],
  "total": 45,
  "pages": 5,
  "current_page": 2,
  "per_page": 10
}
```

#### DESPUÉS (Estructura con Metadata)
```http
GET /api/usuarios/usuarios?page=2&per_page=10 HTTP/1.1
Authorization: Bearer <token_jefe>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "timestamp": "2025-10-31T15:10:35.789Z",
  "data": [
    {
      "id": 11,
      "email": "usuario11@test.com",
      "nombre": "Usuario 11",
      ...
    },
    ...
  ],
  "meta": {
    "pagination": {
      "total": 45,
      "page": 2,
      "per_page": 10,
      "total_pages": 5,
      "has_next": true,
      "has_prev": true
    }
  }
}
```

**Mejoras**:
- ✅ Metadata en objeto `meta.pagination`
- ✅ Campos `has_next` y `has_prev` para UI
- ✅ `total_pages` calculado automáticamente
- ✅ Estructura consistente

---

### 10. Eliminación Exitosa

#### ANTES (Retorna Mensaje)
```http
DELETE /api/usuarios/usuarios/5 HTTP/1.1
Authorization: Bearer <token_admin>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Usuario eliminado exitosamente"
}
```

**Problemas**:
- ❌ 200 con cuerpo para DELETE no es semántico
- ❌ Debería ser 204 No Content

#### DESPUÉS (Sin Contenido)
```http
DELETE /api/usuarios/usuarios/5 HTTP/1.1
Authorization: Bearer <token_admin>
```

```http
HTTP/1.1 204 No Content
```

**Mejoras**:
- ✅ Código 204 (No Content) semánticamente correcto
- ✅ Sin cuerpo (más eficiente)
- ✅ Indica eliminación exitosa por código HTTP

---

### 11. Error de Base de Datos

#### ANTES (Expone Detalles Técnicos)
```http
PUT /api/usuarios/perfil HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Juan Carlos Con Un Nombre Demasiado Largo Que Excede Los 100 Caracteres Permitidos Por La Base De Datos Y Causa Un Error"
}
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Error al actualizar perfil: (pymysql.err.DataError) (1406, \"Data too long for column 'nombre' at row 1\")"
}
```

**Problemas**:
- ❌ Expone detalles de la base de datos
- ❌ Código 400 incorrecto (debería ser 500)
- ❌ Información de seguridad sensible

#### DESPUÉS (Producción - No Expone Detalles)
```http
PUT /api/usuarios/perfil HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Juan Carlos Con Un Nombre Demasiado Largo..."
}
```

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T15:15:50.123Z",
  "request_id": "g2j8k347-9i0k-0h8g-4l7k-3j0i8g7h9k1l",
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Error al procesar la operación en la base de datos",
    "details": {}
  }
}
```

#### DESPUÉS (Desarrollo - Con Detalles)
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "success": false,
  "timestamp": "2025-10-31T15:15:50.123Z",
  "request_id": "g2j8k347-9i0k-0h8g-4l7k-3j0i8g7h9k1l",
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Error al procesar la operación en la base de datos",
    "details": {
      "error": "(pymysql.err.DataError) (1406, \"Data too long for column 'nombre' at row 1\")"
    }
  }
}
```

**Mejoras**:
- ✅ Código 500 correcto para errores de servidor
- ✅ No expone detalles técnicos en producción
- ✅ Incluye request_id para buscar en logs
- ✅ Detalles solo en modo desarrollo

---

## Resumen de Códigos HTTP

### Éxito (2xx)
| Código | Cuándo Usar | Ejemplo |
|--------|-------------|---------|
| 200 OK | GET, PUT, PATCH exitosos | Obtener perfil |
| 201 Created | POST crea recurso | Registrar usuario |
| 204 No Content | DELETE exitoso | Eliminar usuario |

### Errores de Cliente (4xx)
| Código | Cuándo Usar | Ejemplo |
|--------|-------------|---------|
| 400 Bad Request | JSON mal formado | `{"invalid json` |
| 401 Unauthorized | Auth fallida | Password incorrecta |
| 403 Forbidden | Sin permisos | Empleado accede a /usuarios |
| 404 Not Found | Recurso no existe | Usuario ID 999 |
| 409 Conflict | Conflicto de estado | Email ya registrado |
| 422 Validation Error | Datos inválidos | Email sin @ |

### Errores de Servidor (5xx)
| Código | Cuándo Usar | Ejemplo |
|--------|-------------|---------|
| 500 Internal Server Error | Error no esperado | Error de BD |

## Conclusión

La nueva estructura de respuestas proporciona:
- ✅ **Consistencia** en todos los endpoints
- ✅ **Códigos HTTP semánticos** según IANA
- ✅ **Trazabilidad** con request_id
- ✅ **Debugging fácil** con timestamps
- ✅ **Parsing simple** con campo `success`
- ✅ **Seguridad** sin exponer detalles en producción
- ✅ **Experiencia mejorada** para consumidores de la API
