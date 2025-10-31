# 🚀 Práctica de Validación y Trackeo - EJECUTA AHORA

## ⚠️ IMPORTANTE: Debes iniciar la API primero

### Paso 1: Abrir 3 Terminales

#### Terminal 1: Iniciar la API
```bash
cd /mnt/c/Users/aleja/solicitudes-api
python wsgi.py
```

Deberías ver:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**⚠️ NO CIERRES ESTA TERMINAL** - La API debe estar corriendo

---

#### Terminal 2: Ver Logs en Tiempo Real
```bash
cd /mnt/c/Users/aleja/solicitudes-api
tail -f logs/solicitudes_api.log
```

Si el directorio `logs/` no existe, créalo:
```bash
mkdir -p logs
```

**⚠️ DEJA ESTA TERMINAL ABIERTA** - Verás los logs aparecer aquí

---

#### Terminal 3: Ejecutar Pruebas

Ahora sí, vamos a practicar! Ejecuta estos comandos uno por uno:

---

## 🧪 EJERCICIO 1: Error 400 - JSON Mal Formado

**Concepto**: El JSON está roto sintácticamente

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com", "password":"123456'
```

**¿Qué observar?**
1. ✅ Código HTTP: **400 Bad Request**
2. ✅ En Terminal 2 (logs): Verás el error registrado
3. ✅ Mensaje: "El cuerpo de la solicitud no es un JSON válido"

**Resultado esperado**:
```json
{
  "success": false,
  "timestamp": "2025-10-31T...",
  "request_id": "uuid-...",
  "error": {
    "code": "INVALID_JSON",
    "message": "El cuerpo de la solicitud no es un JSON válido",
    "details": {...}
  }
}
```

**Pregunta para ti**: ¿Por qué 400 y no 422?
**Respuesta**: Porque el JSON está **MAL FORMADO** (sintaxis rota), no es un problema de validación.

---

## 🧪 EJERCICIO 2: Error 422 - Email Inválido

**Concepto**: JSON bien formado, pero datos incorrectos

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-sin-arroba",
    "password": "123456",
    "nombre": "Juan"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **422 Unprocessable Entity**
2. ✅ JSON está bien formado (por eso NO es 400)
3. ✅ Pero el email no tiene @ (por eso ES 422)
4. ✅ Error específico: "El formato del email no es válido"

**Resultado esperado**:
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

**Copia el `request_id`** - Lo usaremos en el ejercicio 6

---

## 🧪 EJERCICIO 3: Error 422 - Password Muy Corta

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "123",
    "nombre": "Juan"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **422 Unprocessable Entity**
2. ✅ Error: "La contraseña debe tener al menos 6 caracteres"

**Pregunta para ti**: ¿Cuántos caracteres tiene "123"?
**Respuesta**: 3 caracteres (mínimo es 6)

---

## 🧪 EJERCICIO 4: Error 422 - Múltiples Errores a la Vez

**Concepto**: Todos los errores se retornan juntos (mejor UX)

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalido",
    "password": "12"
  }'
```

**¿Qué observar?**
1. ✅ **3 errores en una sola respuesta**:
   - Email inválido (sin @)
   - Password muy corta (2 caracteres)
   - Falta el campo "nombre"

**Resultado esperado**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
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

**✨ Observa**: No necesitas hacer 3 requests para ver los 3 errores. Todos vienen juntos!

---

## 🧪 EJERCICIO 5: Éxito 201 - Registro Correcto

**Concepto**: Cuando todo está bien, código 201 Created

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario1@test.com",
    "password": "123456",
    "nombre": "Juan"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **201 Created**
2. ✅ `success: true`
3. ✅ Recibes `access_token` y `refresh_token`
4. ✅ Timestamp en formato ISO 8601

**Resultado esperado**:
```json
{
  "success": true,
  "timestamp": "2025-10-31T...",
  "message": "Usuario registrado exitosamente",
  "data": {
    "usuario": {
      "id": 1,
      "email": "usuario1@test.com",
      "nombre": "Juan",
      "rol": "empleado"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJh...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJh...",
    "token_type": "Bearer"
  }
}
```

**Guarda el token** para ejercicios posteriores:
```bash
# En Linux/Mac
TOKEN="eyJ0eXAiOiJKV1QiLCJh..."  # Copia el access_token aquí

# O guárdalo en un archivo
echo "eyJ0eXAiOiJKV1QiLCJh..." > token.txt
```

---

## 🧪 EJERCICIO 6: Trackeo con Request ID

**Concepto**: Cada error tiene un ID único para tracking

**Paso 1**: Provoca un error y guarda la respuesta
```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}' > error.json
```

**Paso 2**: Ver la respuesta completa
```bash
cat error.json
```

**Paso 3**: Busca el campo `request_id` (será algo como `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

**Paso 4**: Búscalo en los logs
```bash
# Reemplaza REQUEST_ID con el valor que copiaste
grep "a1b2c3d4-e5f6-7890-abcd-ef1234567890" logs/solicitudes_api.log
```

**Paso 5**: Ver contexto completo (10 líneas antes y después)
```bash
grep -A 10 -B 10 "a1b2c3d4-e5f6-7890-abcd-ef1234567890" logs/solicitudes_api.log
```

**✨ Beneficio**: En producción, el usuario te da su `request_id` y tú encuentras exactamente qué pasó!

---

## 🧪 EJERCICIO 7: Error 409 - Conflicto (Email Duplicado)

**Concepto**: La operación genera un conflicto con el estado actual

**Paso 1**: Registra un usuario (ya lo hicimos en ejercicio 5)

**Paso 2**: Intenta registrar el mismo email otra vez
```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario1@test.com",
    "password": "123456",
    "nombre": "Pedro"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **409 Conflict**
2. ✅ Error: "El email ya está registrado en el sistema"
3. ✅ Código específico: `USER_ALREADY_EXISTS`

**Pregunta para ti**: ¿Por qué 409 y no 422?
**Respuesta**: Porque NO es un error de validación. El email es válido, pero YA EXISTE (conflicto de estado).

---

## 🧪 EJERCICIO 8: Error 401 - Credenciales Incorrectas

**Concepto**: Autenticación fallida

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario1@test.com",
    "password": "password_incorrecta"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **401 Unauthorized**
2. ✅ Error: "Email o contraseña incorrectos"
3. ✅ Código específico: `INVALID_CREDENTIALS`

**Pregunta para ti**: ¿Por qué 401 y no 403?
**Respuesta**:
- **401** = No estás autenticado (credenciales incorrectas)
- **403** = Estás autenticado pero sin permisos

---

## 🧪 EJERCICIO 9: Éxito 200 - Login Correcto

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario1@test.com",
    "password": "123456"
  }'
```

**¿Qué observar?**
1. ✅ Código HTTP: **200 OK**
2. ✅ `success: true`
3. ✅ Recibes nuevos tokens

---

## 🧪 EJERCICIO 10: Error 401 - Token Inválido

**Concepto**: Token JWT malformado o expirado

```bash
curl -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer token_invalido_xyz123"
```

**¿Qué observar?**
1. ✅ Código HTTP: **401 Unauthorized**
2. ✅ Error: "Not enough segments" (token malformado)
3. ✅ Código específico: `JWT_ERROR`

---

## 🧪 EJERCICIO 11: Éxito 200 - Acceso con Token Válido

**Prerequisito**: Debes tener un token del ejercicio 5 o 9

```bash
# Reemplaza TOKEN con tu token real
curl -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJh..."
```

**¿Qué observar?**
1. ✅ Código HTTP: **200 OK**
2. ✅ Recibes tus datos de usuario

---

## 🧪 EJERCICIO 12: Ver Logs Filtrados

Ahora que has generado varios errores, vamos a analizarlos:

```bash
# Ver todos los errores
grep "ERROR" logs/solicitudes_api.log

# Ver solo errores de validación
grep "VALIDATION_ERROR" logs/solicitudes_api.log

# Contar cuántos errores de cada tipo
grep -o '"code": "[^"]*"' logs/solicitudes_api.log | sort | uniq -c

# Ver últimos 20 errores
grep "ERROR" logs/solicitudes_api.log | tail -20
```

---

## 📊 RESUMEN DE CÓDIGOS HTTP QUE PRACTICASTE

| Código | Nombre | Cuándo | Ejercicio |
|--------|--------|--------|-----------|
| 200 | OK | Login exitoso, GET perfil | 9, 11 |
| 201 | Created | Registro exitoso | 5 |
| 400 | Bad Request | JSON mal formado | 1 |
| 401 | Unauthorized | Credenciales incorrectas, token inválido | 8, 10 |
| 409 | Conflict | Email duplicado | 7 |
| 422 | Validation Error | Datos inválidos | 2, 3, 4 |

---

## ✅ CHECKLIST DE PRÁCTICA

Marca lo que ya completaste:

- [ ] Ejercicio 1: Error 400 (JSON mal formado)
- [ ] Ejercicio 2: Error 422 (Email inválido)
- [ ] Ejercicio 3: Error 422 (Password corta)
- [ ] Ejercicio 4: Error 422 (Múltiples errores)
- [ ] Ejercicio 5: Éxito 201 (Registro correcto)
- [ ] Ejercicio 6: Trackeo con request_id
- [ ] Ejercicio 7: Error 409 (Email duplicado)
- [ ] Ejercicio 8: Error 401 (Login fallido)
- [ ] Ejercicio 9: Éxito 200 (Login exitoso)
- [ ] Ejercicio 10: Error 401 (Token inválido)
- [ ] Ejercicio 11: Éxito 200 (Acceso con token)
- [ ] Ejercicio 12: Ver logs filtrados

---

## 🎯 DESAFÍO FINAL

Realiza un flujo completo de principio a fin:

1. Intenta registrar con email inválido → 422
2. Intenta registrar con password corta → 422
3. Registra correctamente → 201
4. Intenta registrar el mismo email → 409
5. Intenta login con password incorrecta → 401
6. Login correcto → 200
7. Accede a tu perfil con el token → 200
8. Busca todos los request_ids en los logs

**Tiempo estimado**: 10-15 minutos

---

## 💡 PREGUNTAS DE AUTOEVALUACIÓN

1. **¿Cuál es la diferencia entre 400 y 422?**
   - 400 = JSON mal formado (sintaxis)
   - 422 = JSON bien formado pero datos inválidos (semántica)

2. **¿Cuándo usar 409 vs 422?**
   - 409 = Conflicto de estado (ya existe)
   - 422 = Validación fallida (formato incorrecto)

3. **¿Para qué sirve el request_id?**
   - Para trackear una request específica en los logs
   - Para debugging en producción

4. **¿Por qué todos los errores vienen juntos en 422?**
   - Mejor experiencia de usuario
   - El usuario no tiene que corregir de uno en uno

5. **¿Qué código HTTP se usa para registro exitoso?**
   - 201 Created (no 200)

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Completa todos los ejercicios
2. ✅ Intenta el desafío final
3. ✅ Responde las preguntas de autoevaluación
4. 📚 Lee `EJEMPLOS_RESPUESTAS_API.md` para ver más ejemplos
5. 🔧 Practica con Postman (guía en `PRACTICA_VALIDACION_TRACKEO.md`)
6. 🤖 Ejecuta `./test_validacion.sh` para ver todos los tests automatizados

---

## ❓ SI ALGO NO FUNCIONA

### La API no inicia
```bash
# Verifica que estás en el directorio correcto
pwd  # Debe mostrar: /mnt/c/Users/aleja/solicitudes-api

# Verifica que tienes Python
python --version

# Verifica que tienes las dependencias
pip install -r requirements.txt

# Inicia la API
python wsgi.py
```

### No se crean los logs
```bash
# Crea el directorio manualmente
mkdir -p logs

# Verifica permisos
ls -la logs/
```

### curl no funciona
- Verifica que la API está corriendo en Terminal 1
- Verifica que el puerto 5000 está disponible
- Prueba con: `curl http://localhost:5000/health`

---

**¡Disfruta practicando! 🎉**

**Tiempo total estimado**: 30-45 minutos
