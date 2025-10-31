# Cómo Practicar Validación y Trackeo de Errores

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Iniciar la API

```bash
cd /mnt/c/Users/aleja/solicitudes-api
python wsgi.py
```

Deberías ver:
```
 * Running on http://127.0.0.1:5000
```

### Paso 2: Ejecutar el Script de Pruebas Automatizado

En otra terminal:

```bash
cd /mnt/c/Users/aleja/solicitudes-api
./test_validacion.sh
```

Este script ejecutará **10 tests automáticos** que demuestran:
- ✅ Validación de datos
- ✅ Códigos HTTP correctos
- ✅ Estructura de respuestas
- ✅ Trackeo con request_id

### Paso 3: Ver los Logs en Tiempo Real

En otra terminal:

```bash
cd /mnt/c/Users/aleja/solicitudes-api
tail -f logs/solicitudes_api.log
```

Ahora vuelve a ejecutar el script y verás los logs aparecer en tiempo real! 📊

---

## 📚 Opciones de Práctica

### Opción 1: Script Automatizado (Recomendado para empezar)

**Ventajas**: Rápido, visual, muestra todos los casos

```bash
./test_validacion.sh
```

### Opción 2: curl Manual (Aprendizaje profundo)

**Ventajas**: Entiendes cada request

Lee y sigue los ejercicios en: `PRACTICA_VALIDACION_TRACKEO.md`

Ejemplo:
```bash
# Probar validación de email
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"sin-arroba","password":"123456","nombre":"Juan"}' \
  | jq
```

### Opción 3: Postman (Interfaz gráfica)

**Ventajas**: Interfaz visual, guardar requests, tests automáticos

Lee la sección "Parte 5: Usando Postman" en `PRACTICA_VALIDACION_TRACKEO.md`

---

## 🎯 Ejercicios Paso a Paso

### Ejercicio 1: Provocar Cada Tipo de Error

Objetivo: Entender la diferencia entre códigos HTTP

```bash
# 1. Error 400 (JSON mal formado)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"invalid json'

# 2. Error 422 (Validación - email inválido)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"123456","nombre":"Juan"}'

# 3. Error 409 (Conflicto - email duplicado)
# Primero crea un usuario
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456","nombre":"Juan"}'

# Luego intenta crearlo otra vez
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456","nombre":"Pedro"}'

# 4. Error 401 (Credenciales incorrectas)
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"incorrecta"}'
```

**Pregunta para ti**: ¿Cuál es la diferencia entre 400 y 422?
**Respuesta**: 400 = JSON roto, 422 = JSON válido pero datos incorrectos

---

### Ejercicio 2: Trackear un Error Específico

Objetivo: Usar request_id para encontrar errores en logs

```bash
# 1. Provocar un error y capturar la respuesta
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}' > error.json

# 2. Ver la respuesta
cat error.json | jq

# 3. Extraer el request_id
REQUEST_ID=$(cat error.json | jq -r '.request_id')
echo "Request ID: $REQUEST_ID"

# 4. Buscar en los logs
grep "$REQUEST_ID" logs/solicitudes_api.log

# 5. Ver contexto (10 líneas antes y después)
grep -A 10 -B 10 "$REQUEST_ID" logs/solicitudes_api.log
```

**Beneficio**: En producción puedes decirle al usuario "Dame tu request_id" y encontrar exactamente qué pasó.

---

### Ejercicio 3: Comparar Respuestas Antes vs Después

Objetivo: Ver la mejora en la estructura de respuestas

**Antes** (estructura simple):
```json
{
  "error": "El campo nombre es requerido"
}
```

**Después** (estructura profesional):
```json
{
  "success": false,
  "timestamp": "2025-10-31T15:30:45.123Z",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "errors": {
        "nombre": ["El nombre es requerido"]
      }
    }
  }
}
```

Provoca el mismo error y compara las respuestas!

---

### Ejercicio 4: Validación Múltiple

Objetivo: Ver cómo se retornan múltiples errores a la vez

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}' \
  | jq '.error.details.errors'
```

**Resultado esperado**:
```json
{
  "email": ["El formato del email no es válido"],
  "password": ["La contraseña debe tener al menos 6 caracteres"],
  "nombre": ["El nombre es requerido"]
}
```

**Observa**: Todos los errores en una sola respuesta = mejor UX

---

### Ejercicio 5: Flujo Completo de Usuario

Objetivo: Practicar un flujo real de principio a fin

```bash
# 1. Intenta registrar con datos inválidos (422)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test","password":"123456","nombre":"Juan"}'

# 2. Corrige el email y registra exitosamente (201)
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"miusuario@test.com","password":"123456","nombre":"Juan"}' \
  > registro.json

# 3. Extrae el token
TOKEN=$(cat registro.json | jq -r '.data.access_token')
echo "Token: $TOKEN"

# 4. Accede a tu perfil (200)
curl -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN" \
  | jq

# 5. Actualiza tu perfil (200)
curl -X PUT http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Carlos","apellido":"Pérez"}' \
  | jq

# 6. Intenta login con password incorrecta (401)
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"miusuario@test.com","password":"incorrecta"}' \
  | jq

# 7. Login correcto (200)
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"miusuario@test.com","password":"123456"}' \
  | jq
```

---

## 🔍 Comandos Útiles para Trackeo

### Ver logs en tiempo real
```bash
tail -f logs/solicitudes_api.log
```

### Ver solo errores
```bash
grep "ERROR" logs/solicitudes_api.log
```

### Ver errores de validación
```bash
grep "VALIDATION_ERROR" logs/solicitudes_api.log
```

### Ver errores de base de datos
```bash
grep "DATABASE_ERROR" logs/errors.log
```

### Buscar por request_id
```bash
grep "a1b2c3d4-e5f6-7890-abcd-ef1234567890" logs/solicitudes_api.log
```

### Contar errores por tipo
```bash
grep -o "\"code\": \"[^\"]*\"" logs/solicitudes_api.log | sort | uniq -c
```

### Ver últimos 50 errores
```bash
grep "ERROR" logs/solicitudes_api.log | tail -50
```

---

## 📊 Tabla de Códigos HTTP para Referencia

| Código | Nombre | Cuándo Usar | Ejemplo |
|--------|--------|-------------|---------|
| 200 | OK | GET/PUT exitoso | Ver perfil |
| 201 | Created | POST exitoso | Registro |
| 204 | No Content | DELETE exitoso | Eliminar usuario |
| 400 | Bad Request | JSON mal formado | `{"invalid` |
| 401 | Unauthorized | Auth fallida | Password incorrecta |
| 403 | Forbidden | Sin permisos | Empleado → /usuarios |
| 404 | Not Found | No existe | Usuario ID 999 |
| 409 | Conflict | Conflicto | Email duplicado |
| 422 | Validation Error | Datos inválidos | Email sin @ |
| 500 | Internal Error | Error servidor | Error de BD |

---

## 🎓 Desafíos de Práctica

### Desafío 1: Provocar todos los errores
- [ ] 400 Bad Request
- [ ] 422 Validation Error (al menos 3 diferentes)
- [ ] 409 Conflict
- [ ] 401 Unauthorized
- [ ] 403 Forbidden (requiere crear admin y empleado)
- [ ] 404 Not Found

### Desafío 2: Trackeo completo
- [ ] Provocar un error
- [ ] Copiar el request_id
- [ ] Encontrarlo en logs
- [ ] Ver el contexto completo

### Desafío 3: Crear colección de Postman
- [ ] Crear carpeta "Validación"
- [ ] Agregar request para cada tipo de error
- [ ] Agregar tests automáticos
- [ ] Exportar y compartir

### Desafío 4: Flujo completo
- [ ] Registro con datos inválidos → corregir → éxito
- [ ] Login fallido → corregir → éxito
- [ ] Acceder al perfil con token
- [ ] Actualizar perfil
- [ ] Trackear todos los request_ids

---

## 💡 Preguntas Frecuentes

### ¿Qué es un request_id?
Un ID único generado para cada request que te permite encontrar esa request específica en los logs.

### ¿Por qué 422 y no 400 para validación?
- **400**: Algo está MAL FORMADO (JSON roto, sintaxis incorrecta)
- **422**: JSON está bien, pero los DATOS no cumplen las reglas

### ¿Cuándo usar 409 vs 422?
- **409**: Conflicto de ESTADO (email ya existe, solicitud ya procesada)
- **422**: Datos INVÁLIDOS (email sin @, password muy corta)

### ¿Cómo sé si mi error es 4xx o 5xx?
- **4xx**: Error del CLIENTE (datos incorrectos, sin permisos, etc.)
- **5xx**: Error del SERVIDOR (base de datos, exception no manejada)

### ¿Puedo ver los logs en Windows?
Sí, usa PowerShell:
```powershell
Get-Content logs\solicitudes_api.log -Wait -Tail 50
```

---

## 📖 Recursos Adicionales

1. **PRACTICA_VALIDACION_TRACKEO.md** - Guía completa con todos los ejercicios
2. **EJEMPLOS_RESPUESTAS_API.md** - 11 ejemplos antes/después
3. **IMPLEMENTACION_CODIGOS_HTTP.md** - Documentación técnica
4. **test_validacion.sh** - Script automatizado de pruebas

---

## 🎯 Próximos Pasos

1. ✅ Ejecuta `./test_validacion.sh` (5 minutos)
2. ✅ Lee `EJEMPLOS_RESPUESTAS_API.md` (10 minutos)
3. ✅ Practica con curl siguiendo `PRACTICA_VALIDACION_TRACKEO.md` (30 minutos)
4. ✅ Crea tu colección de Postman (20 minutos)
5. ✅ Completa los 4 desafíos (60 minutos)

**Tiempo total de práctica**: ~2 horas

---

## ✨ Conclusión

Ahora tienes todas las herramientas para:
- ✅ Entender códigos HTTP
- ✅ Provocar y capturar errores
- ✅ Trackear errores con request_id
- ✅ Leer y analizar logs
- ✅ Validar datos automáticamente

¡Practica y conviértete en un experto en validación y trackeo de errores! 🚀

---

**¿Necesitas ayuda?**
- Lee la documentación en los archivos MD
- Ejecuta el script de pruebas automatizado
- Experimenta con curl o Postman
- Revisa los logs para entender qué pasó
