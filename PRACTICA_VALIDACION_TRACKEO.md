# Guía Práctica: Validación y Trackeo de Errores

## Objetivo

Aprender a probar y entender el sistema de validación automática y trackeo de errores implementado en la API.

## Requisitos Previos

1. Tener la API corriendo:
```bash
cd /mnt/c/Users/aleja/solicitudes-api
python wsgi.py
```

2. Tener instalado `curl` o usar Postman/Insomnia

## Parte 1: Practicar Validación de Errores

### 🧪 Ejercicio 1: Error de JSON Mal Formado (400 Bad Request)

**Concepto**: El JSON está roto sintácticamente.

```bash
# Enviar JSON inválido (falta comilla de cierre)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com", "password":"123456'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "INVALID_JSON",
    "message": "El cuerpo de la solicitud no es un JSON válido",
    "details": {
      "error": "..."
    }
  }
}
```

**Código HTTP**: `400 Bad Request`

**¿Por qué 400?**: El JSON está mal formado sintácticamente (error de sintaxis).

---

### 🧪 Ejercicio 2: Errores de Validación (422 Unprocessable Entity)

**Concepto**: El JSON está bien formado, pero los datos no cumplen las reglas de negocio.

#### 2.1 Email Inválido

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-sin-arroba",
    "password": "123456",
    "nombre": "Juan"
  }'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "errors": {
        "email": ["El formato del email no es válido"]
      }
    }
  }
}
```

**Código HTTP**: `422 Unprocessable Entity`

**¿Por qué 422?**: El JSON es válido, pero el email no cumple las reglas de validación.

#### 2.2 Password Muy Corta

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "123",
    "nombre": "Juan"
  }'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "errors": {
        "password": ["La contraseña debe tener al menos 6 caracteres"]
      }
    }
  }
}
```

**Código HTTP**: `422 Unprocessable Entity`

#### 2.3 Múltiples Errores de Validación

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-invalido",
    "password": "12"
  }'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
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

**Código HTTP**: `422 Unprocessable Entity`

**✨ Observa**: Todos los errores se retornan en una sola respuesta (mejor UX).

---

### 🧪 Ejercicio 3: Conflicto de Estado (409 Conflict)

**Concepto**: La operación genera un conflicto con el estado actual.

#### 3.1 Email Ya Registrado

```bash
# Paso 1: Registrar un usuario
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "123456",
    "nombre": "Juan"
  }'

# Paso 2: Intentar registrar el mismo email otra vez
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "123456",
    "nombre": "Pedro"
  }'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "USER_ALREADY_EXISTS",
    "message": "El email ya está registrado en el sistema",
    "details": {}
  }
}
```

**Código HTTP**: `409 Conflict`

**¿Por qué 409?**: Hay un conflicto con el estado actual (el email ya existe).

---

### 🧪 Ejercicio 4: Autenticación Fallida (401 Unauthorized)

**Concepto**: Las credenciales son incorrectas.

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "password_incorrecta"
  }'
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email o contraseña incorrectos",
    "details": {}
  }
}
```

**Código HTTP**: `401 Unauthorized`

**¿Por qué 401?**: La autenticación falló (credenciales incorrectas).

---

### 🧪 Ejercicio 5: Sin Permisos (403 Forbidden)

**Concepto**: Usuario autenticado pero sin permisos suficientes.

```bash
# Paso 1: Login como empleado
RESPONSE=$(curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empleado@test.com",
    "password": "123456"
  }')

# Extraer token (en Linux/Mac)
TOKEN=$(echo $RESPONSE | jq -r '.data.access_token')

# Paso 2: Intentar acceder a endpoint de admin
curl -X GET http://localhost:5000/api/usuarios/usuarios \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
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

**Código HTTP**: `403 Forbidden`

**¿Por qué 403?**: Usuario autenticado pero sin permisos para este recurso.

---

### 🧪 Ejercicio 6: Recurso No Encontrado (404 Not Found)

**Concepto**: El recurso solicitado no existe.

```bash
# Primero obtener un token
TOKEN="..." # Del ejercicio anterior

# Intentar obtener usuario que no existe
curl -X GET http://localhost:5000/api/usuarios/usuarios/99999 \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": {}
  }
}
```

**Código HTTP**: `404 Not Found`

**¿Por qué 404?**: El recurso (usuario con ID 99999) no existe.

---

### 🧪 Ejercicio 7: Token JWT Inválido (401 Unauthorized)

**Concepto**: Token expirado o malformado.

```bash
# Intentar acceder con token inválido
curl -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer token_invalido_123"
```

**Respuesta Esperada**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "JWT_ERROR",
    "message": "Not enough segments",
    "details": {}
  }
}
```

**Código HTTP**: `401 Unauthorized`

---

## Parte 2: Trackeo de Errores

### 📍 Ejercicio 8: Usar Request ID para Trackear Errores

**Concepto**: Cada error tiene un `request_id` único para debugging.

#### Paso 1: Provocar un Error

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@error.com",
    "password": "123"
  }' | jq
```

**Respuesta**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T15:30:45.123Z",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",  // ⬅️ COPIAR ESTE ID
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "errors": {
        "password": ["La contraseña debe tener al menos 6 caracteres"]
      }
    }
  }
}
```

#### Paso 2: Buscar en los Logs

```bash
# Buscar el error en los logs usando el request_id
cd /mnt/c/Users/aleja/solicitudes-api
grep "a1b2c3d4-e5f6-7890-abcd-ef1234567890" logs/solicitudes_api.log
```

**Beneficio**: Puedes rastrear exactamente qué pasó con esa request específica.

---

### 📍 Ejercicio 9: Ver Logs en Tiempo Real

**Concepto**: Monitorear errores mientras haces requests.

#### Terminal 1: Ver Logs en Tiempo Real

```bash
cd /mnt/c/Users/aleja/solicitudes-api
tail -f logs/solicitudes_api.log
```

#### Terminal 2: Hacer Requests

```bash
# Provocar varios tipos de error
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"noexiste@test.com","password":"123456"}'

curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}'
```

**Observa**: En la Terminal 1 verás los logs aparecer en tiempo real.

---

### 📍 Ejercicio 10: Filtrar Logs por Tipo de Error

#### Ver solo errores (ERROR level)

```bash
grep "ERROR" logs/solicitudes_api.log
```

#### Ver solo errores de validación

```bash
grep "VALIDATION_ERROR" logs/solicitudes_api.log
```

#### Ver errores de base de datos

```bash
grep "DATABASE_ERROR" logs/errors.log
```

---

## Parte 3: Crear un Script de Pruebas

Voy a crear un script que puedes ejecutar para probar todos los casos:

```bash
#!/bin/bash

echo "🧪 Script de Pruebas de Validación y Trackeo de Errores"
echo "========================================================"
echo ""

API_URL="http://localhost:5000"

echo "📋 Test 1: JSON mal formado (400 Bad Request)"
curl -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com"' \
  -w "\nCódigo HTTP: %{http_code}\n\n"

echo "📋 Test 2: Email inválido (422 Validation Error)"
curl -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"sin-arroba","password":"123456","nombre":"Juan"}' \
  -w "\nCódigo HTTP: %{http_code}\n\n" | jq

echo "📋 Test 3: Password muy corta (422 Validation Error)"
curl -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123","nombre":"Juan"}' \
  -w "\nCódigo HTTP: %{http_code}\n\n" | jq

echo "📋 Test 4: Múltiples errores de validación (422)"
curl -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}' \
  -w "\nCódigo HTTP: %{http_code}\n\n" | jq

echo "📋 Test 5: Registro exitoso (201 Created)"
REGISTRO=$(curl -s -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test'$(date +%s)'@test.com","password":"123456","nombre":"Juan"}')
echo $REGISTRO | jq
echo "Código HTTP: 201"
echo ""

echo "📋 Test 6: Login con credenciales incorrectas (401 Unauthorized)"
curl -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"incorrecta"}' \
  -w "\nCódigo HTTP: %{http_code}\n\n" | jq

echo "📋 Test 7: Token JWT inválido (401 Unauthorized)"
curl -X GET $API_URL/api/usuarios/perfil \
  -H "Authorization: Bearer token_invalido" \
  -w "\nCódigo HTTP: %{http_code}\n\n" | jq

echo "✅ Pruebas completadas!"
echo ""
echo "💡 Revisa los logs en: logs/solicitudes_api.log"
```

---

## Parte 4: Ejercicios Prácticos Guiados

### 🎯 Ejercicio Práctico 1: Flujo Completo de Registro

**Objetivo**: Probar la validación paso a paso.

```bash
# 1. Intenta registrar sin nombre (422)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456"}'

# Pregunta: ¿Qué código HTTP recibiste?
# Respuesta esperada: 422
# ¿Por qué?: Falta el campo requerido "nombre"

# 2. Intenta con email inválido (422)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test","password":"123456","nombre":"Juan"}'

# Pregunta: ¿Qué error específico recibes?
# Respuesta esperada: "El formato del email no es válido"

# 3. Intenta con password corta (422)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123","nombre":"Juan"}'

# Pregunta: ¿Qué código HTTP recibiste?
# Respuesta esperada: 422
# ¿Cuál es el error?: "La contraseña debe tener al menos 6 caracteres"

# 4. Registro exitoso (201)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456","nombre":"Juan"}'

# Pregunta: ¿Qué código HTTP recibiste?
# Respuesta esperada: 201 Created
# ¿Recibes tokens?: Sí, access_token y refresh_token

# 5. Intenta registrar el mismo email (409)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456","nombre":"Pedro"}'

# Pregunta: ¿Qué código HTTP recibiste?
# Respuesta esperada: 409 Conflict
# ¿Por qué?: El email ya está registrado
```

---

### 🎯 Ejercicio Práctico 2: Trackear un Error Específico

**Objetivo**: Provocar un error y rastrearlo en los logs.

```bash
# 1. Provocar un error de validación
RESPONSE=$(curl -s -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}')

# 2. Ver la respuesta completa
echo $RESPONSE | jq

# 3. Extraer el request_id
REQUEST_ID=$(echo $RESPONSE | jq -r '.request_id')
echo "Request ID: $REQUEST_ID"

# 4. Buscar en los logs
grep "$REQUEST_ID" logs/solicitudes_api.log

# 5. Ver el contexto completo (10 líneas antes y después)
grep -A 10 -B 10 "$REQUEST_ID" logs/solicitudes_api.log
```

---

### 🎯 Ejercicio Práctico 3: Comparar Códigos HTTP

**Objetivo**: Entender la diferencia entre 400, 422, 409, 401, 403, 404.

```bash
# Test 1: 400 Bad Request (JSON mal formado)
echo "=== 400 Bad Request ==="
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"invalid json' \
  -w "\nHTTP: %{http_code}\n"

# Test 2: 422 Validation Error (JSON válido, datos inválidos)
echo "=== 422 Validation Error ==="
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"123456","nombre":"Juan"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 3: 409 Conflict (registro duplicado)
echo "=== 409 Conflict ==="
# Primero registra
curl -s -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"conflict@test.com","password":"123456","nombre":"Juan"}' > /dev/null
# Luego intenta duplicar
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"conflict@test.com","password":"123456","nombre":"Pedro"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 4: 401 Unauthorized (credenciales incorrectas)
echo "=== 401 Unauthorized ==="
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"incorrecta"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 5: 403 Forbidden (sin permisos - requiere token de empleado)
echo "=== 403 Forbidden ==="
echo "Requiere token de empleado - ver ejercicio 5"

# Test 6: 404 Not Found (recurso no existe - requiere token de admin)
echo "=== 404 Not Found ==="
echo "Requiere token de admin - ver ejercicio 6"
```

---

## Parte 5: Usando Postman

### Colección de Postman para Pruebas

Crea una colección en Postman con estos requests:

#### 1. **Carpeta: Validación**

**Request 1.1**: Email Inválido (422)
```
POST http://localhost:5000/api/usuarios/registro
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "sin-arroba",
  "password": "123456",
  "nombre": "Juan"
}
```

**Request 1.2**: Password Corta (422)
```
POST http://localhost:5000/api/usuarios/registro
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "test@test.com",
  "password": "123",
  "nombre": "Juan"
}
```

**Request 1.3**: Múltiples Errores (422)
```
POST http://localhost:5000/api/usuarios/registro
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "invalido",
  "password": "12"
}
```

#### 2. **Carpeta: Códigos HTTP**

**Request 2.1**: 201 Created
```
POST http://localhost:5000/api/usuarios/registro
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "nuevo{{$timestamp}}@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```

**Request 2.2**: 409 Conflict
```
POST http://localhost:5000/api/usuarios/registro
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "duplicado@test.com",
  "password": "123456",
  "nombre": "Juan"
}
```
*Ejecuta dos veces para ver el 409*

**Request 2.3**: 401 Unauthorized
```
POST http://localhost:5000/api/usuarios/login
Headers:
  Content-Type: application/json
Body (JSON):
{
  "email": "test@test.com",
  "password": "incorrecta"
}
```

### Tests en Postman

Agrega estos tests en la pestaña "Tests":

```javascript
// Test para verificar código HTTP
pm.test("Status code is 422", function () {
    pm.response.to.have.status(422);
});

// Test para verificar estructura de error
pm.test("Error structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success', false);
    pm.expect(jsonData).to.have.property('error');
    pm.expect(jsonData.error).to.have.property('code');
    pm.expect(jsonData.error).to.have.property('message');
});

// Test para verificar request_id
pm.test("Request ID exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('request_id');
    console.log("Request ID:", jsonData.request_id);
});
```

---

## Resumen de Códigos HTTP

| Código | Cuándo | Ejemplo |
|--------|--------|---------|
| 400 | JSON mal formado | `{"invalid` |
| 401 | Auth fallida | Password incorrecta |
| 403 | Sin permisos | Empleado accede a /usuarios |
| 404 | No existe | Usuario ID 99999 |
| 409 | Conflicto | Email duplicado |
| 422 | Validación | Email sin @ |

## Checklist de Práctica

- [ ] Provocar error 400 (JSON inválido)
- [ ] Provocar error 422 (email inválido)
- [ ] Provocar error 422 (password corta)
- [ ] Provocar error 422 (múltiples errores)
- [ ] Provocar error 409 (email duplicado)
- [ ] Provocar error 401 (login fallido)
- [ ] Provocar error 401 (token inválido)
- [ ] Provocar error 403 (sin permisos)
- [ ] Provocar error 404 (recurso no existe)
- [ ] Extraer y buscar request_id en logs
- [ ] Ver logs en tiempo real
- [ ] Crear colección en Postman
- [ ] Ejecutar script de pruebas automatizado

## Próximos Pasos

1. ✅ Completar todos los ejercicios de esta guía
2. ✅ Crear tu propia colección de Postman
3. ✅ Practicar tracking de errores con request_id
4. ✅ Entender la diferencia entre cada código HTTP
5. 📚 Aplicar estos conceptos a `solicitudes.py` y `notificaciones.py`

¡Ahora tienes todas las herramientas para practicar validación y trackeo de errores como un profesional! 🚀
