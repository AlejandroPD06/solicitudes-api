# 📚 Documentación Swagger de la API

Documentación interactiva completa de todos los endpoints de la API usando Swagger/OpenAPI.

---

## 🎯 ¿Qué es Swagger?

Swagger es una interfaz web interactiva que te permite:
- Ver todos los endpoints disponibles
- Ver ejemplos de request/response
- Probar endpoints directamente desde el navegador
- Autenticarte con JWT tokens
- Generar especificaciones OpenAPI

---

## 🚀 Cómo Acceder a Swagger

### Opción 1: Interfaz Web Interactiva (Recomendado)

```
http://localhost:5000/api/docs
```

**Abre tu navegador y visita esta URL**. Verás una interfaz gráfica completa con todos los endpoints.

### Opción 2: Especificación JSON (Para herramientas)

```bash
curl http://localhost:5000/apispec.json
```

Obtiene la especificación OpenAPI completa en formato JSON (útil para Postman, Insomnia, etc).

---

## 📖 Endpoints Documentados

### 🔐 Autenticación
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/api/usuarios/login` | Iniciar sesión | No |
| POST | `/api/usuarios/registro` | Registrar nuevo usuario | No |
| GET | `/api/usuarios/perfil` | Obtener perfil actual | Sí |
| PUT | `/api/usuarios/perfil` | Actualizar perfil actual | Sí |
| POST | `/api/usuarios/cambiar-password` | Cambiar contraseña | Sí |

### 👥 Gestión de Usuarios (Admin/Jefe)
| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| GET | `/api/usuarios/usuarios` | Listar usuarios | Jefe, Admin |
| GET | `/api/usuarios/usuarios/:id` | Obtener usuario específico | Jefe, Admin |
| PUT | `/api/usuarios/usuarios/:id` | Actualizar usuario | Admin |
| DELETE | `/api/usuarios/usuarios/:id` | Eliminar usuario | Admin |

---

## 🔧 Ejemplo de Uso Paso a Paso

### 1. Abrir Swagger UI

Abre tu navegador en:
```
http://localhost:5000/api/docs
```

### 2. Hacer Login

1. Busca el endpoint **`POST /api/usuarios/login`** en la sección "Autenticación"
2. Haz clic en el endpoint para expandirlo
3. Haz clic en el botón **"Try it out"**
4. Ingresa las credenciales en el campo de texto:

```json
{
  "email": "admin@solicitudes.com",
  "password": "admin123"
}
```

5. Haz clic en **"Execute"**
6. En la respuesta, copia el valor de `access_token`

**Ejemplo de respuesta:**
```json
{
  "message": "Login exitoso",
  "usuario": {
    "id": 1,
    "email": "admin@solicitudes.com",
    "nombre": "Admin",
    "rol": "administrador"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

### 3. Autenticarse en Swagger

1. En la parte superior derecha de la página, busca el botón **"Authorize"** (🔓 candado)
2. Haz clic en él
3. En el campo que aparece, ingresa:
```
Bearer TU_ACCESS_TOKEN_AQUI
```
**Importante:** Debes incluir la palabra "Bearer" seguida de un espacio y luego tu token.

4. Haz clic en **"Authorize"**
5. Haz clic en **"Close"**

Ahora el candado se verá cerrado (🔒) y podrás acceder a todos los endpoints protegidos.

### 4. Probar un Endpoint Protegido

Ejemplo: Listar usuarios

1. Busca el endpoint **`GET /api/usuarios/usuarios`** en la sección "Usuarios"
2. Haz clic en **"Try it out"**
3. (Opcional) Configura filtros en los query parameters:
   - `rol`: empleado, jefe, o administrador
   - `activo`: true o false
   - `page`: número de página
   - `per_page`: cantidad por página

4. Haz clic en **"Execute"**
5. Verás la respuesta con la lista de usuarios

**Ejemplo de respuesta:**
```json
{
  "usuarios": [
    {
      "id": 1,
      "email": "admin@solicitudes.com",
      "nombre": "Admin",
      "rol": "administrador",
      "activo": true
    }
  ],
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "per_page": 10
}
```

---

## 📝 Ejemplos Rápidos por Endpoint

### Login
```bash
# Desde Swagger
Endpoint: POST /api/usuarios/login
Body:
{
  "email": "admin@solicitudes.com",
  "password": "admin123"
}

# Desde curl
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}'
```

### Registrar Usuario
```bash
# Desde Swagger
Endpoint: POST /api/usuarios/registro
Body:
{
  "email": "nuevo@solicitudes.com",
  "password": "password123",
  "nombre": "Juan",
  "apellido": "Pérez",
  "rol": "empleado"
}

# Desde curl
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN" \
  -d '{
    "email":"nuevo@solicitudes.com",
    "password":"password123",
    "nombre":"Juan",
    "apellido":"Pérez",
    "rol":"empleado"
  }'
```

### Obtener Perfil
```bash
# Desde Swagger (necesita autorización)
Endpoint: GET /api/usuarios/perfil
Headers: Authorization: Bearer TU_TOKEN

# Desde curl
curl http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer TU_TOKEN"
```

### Actualizar Perfil
```bash
# Desde Swagger (necesita autorización)
Endpoint: PUT /api/usuarios/perfil
Body:
{
  "nombre": "Nuevo Nombre",
  "apellido": "Nuevo Apellido"
}

# Desde curl
curl -X PUT http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nuevo Nombre","apellido":"Nuevo Apellido"}'
```

### Cambiar Contraseña
```bash
# Desde Swagger (necesita autorización)
Endpoint: POST /api/usuarios/cambiar-password
Body:
{
  "password_actual": "password123",
  "password_nueva": "newpassword456"
}

# Desde curl
curl -X POST http://localhost:5000/api/usuarios/cambiar-password \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password_actual":"password123",
    "password_nueva":"newpassword456"
  }'
```

### Listar Usuarios (Admin/Jefe)
```bash
# Desde Swagger (necesita autorización)
Endpoint: GET /api/usuarios/usuarios
Query params:
- rol: empleado
- activo: true
- page: 1
- per_page: 10

# Desde curl
curl "http://localhost:5000/api/usuarios/usuarios?rol=empleado&page=1&per_page=10" \
  -H "Authorization: Bearer TU_TOKEN"
```

### Obtener Usuario por ID (Admin/Jefe)
```bash
# Desde Swagger (necesita autorización)
Endpoint: GET /api/usuarios/usuarios/{usuario_id}
Path param: usuario_id = 5

# Desde curl
curl http://localhost:5000/api/usuarios/usuarios/5 \
  -H "Authorization: Bearer TU_TOKEN"
```

### Actualizar Usuario (Admin)
```bash
# Desde Swagger (necesita autorización)
Endpoint: PUT /api/usuarios/usuarios/{usuario_id}
Path param: usuario_id = 5
Body:
{
  "nombre": "Nuevo Nombre",
  "rol": "jefe",
  "activo": true
}

# Desde curl
curl -X PUT http://localhost:5000/api/usuarios/usuarios/5 \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nuevo Nombre","rol":"jefe","activo":true}'
```

### Eliminar Usuario (Admin)
```bash
# Desde Swagger (necesita autorización)
Endpoint: DELETE /api/usuarios/usuarios/{usuario_id}
Path param: usuario_id = 5

# Desde curl
curl -X DELETE http://localhost:5000/api/usuarios/usuarios/5 \
  -H "Authorization: Bearer TU_TOKEN"
```

---

## 🎨 Características de la Interfaz Swagger

### 1. **Navegación por Tags**
Los endpoints están organizados en categorías:
- 🔐 **Autenticación** - Login, registro, perfil
- 👥 **Usuarios** - Gestión de usuarios (admin)
- 📋 **Solicitudes** - CRUD de solicitudes
- 🔔 **Notificaciones** - Sistema de notificaciones
- ⚕️ **Sistema** - Health check y utilidades

### 2. **Colores de Métodos HTTP**
- 🟢 **GET** - Verde (consultas)
- 🔵 **POST** - Azul (crear)
- 🟠 **PUT** - Naranja (actualizar)
- 🔴 **DELETE** - Rojo (eliminar)

### 3. **Información de Cada Endpoint**
Para cada endpoint verás:
- **Descripción** - Qué hace el endpoint
- **Parameters** - Parámetros requeridos/opcionales
- **Request Body** - Estructura del JSON de entrada
- **Responses** - Posibles respuestas con códigos HTTP
- **Examples** - Valores de ejemplo
- **Security** - Si requiere autenticación

### 4. **Try it out (Probar)**
El botón "Try it out" te permite:
- Editar los valores de ejemplo
- Ejecutar la petición real
- Ver el request HTTP completo (curl)
- Ver la respuesta en tiempo real

### 5. **Botón Authorize**
- Ubicado arriba a la derecha
- Te permite ingresar tu JWT token una sola vez
- Se aplica automáticamente a todos los endpoints protegidos

---

## 🔒 Seguridad y Autenticación

### Tipos de Endpoints

1. **Públicos (sin 🔒)**
   - `/api/usuarios/login`
   - `/api/usuarios/registro`
   - No requieren token

2. **Protegidos (con 🔒)**
   - Todos los demás endpoints
   - Requieren JWT token válido
   - Token expira en 1 hora

### Formato del Token

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Roles y Permisos

- **empleado** - Puede crear y ver sus propias solicitudes
- **jefe** - Puede aprobar/rechazar solicitudes + listar usuarios
- **administrador** - Acceso completo, puede gestionar usuarios

---

## 🛠️ Configuración Técnica

### Archivos Modificados

1. **`requirements.txt:9`**
   ```txt
   flasgger==0.9.7.1
   ```

2. **`app/__init__.py:63-110`**
   - Configuración de Swagger
   - Template personalizado
   - Definición de seguridad JWT

3. **`app/routes/auth.py`**
   - Documentación de todos los endpoints de autenticación
   - Documentación de gestión de usuarios

### Configuración de Swagger

```python
swagger_config = {
    "specs_route": "/api/docs"  # URL de la interfaz
}

swagger_template = {
    "info": {
        "title": "API de Solicitudes",
        "description": "Documentación interactiva...",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
```

### Formato de Documentación en Endpoints

```python
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión en el sistema
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login exitoso
    """
    # Código del endpoint...
```

---

## 📊 Exportar Documentación

### Opción 1: Descargar Especificación OpenAPI

```bash
# Descargar como JSON
curl http://localhost:5000/apispec.json > api-spec.json

# Descargar como YAML (con conversión)
curl http://localhost:5000/apispec.json | python3 -c "import sys, yaml, json; yaml.dump(json.load(sys.stdin), sys.stdout)" > api-spec.yaml
```

### Opción 2: Importar a Otras Herramientas

**Postman:**
1. File → Import
2. Link: `http://localhost:5000/apispec.json`

**Insomnia:**
1. Application → Preferences → Data
2. Import Data → From URL
3. URL: `http://localhost:5000/apispec.json`

---

## 🐛 Troubleshooting

### Problema: No puedo acceder a /api/docs

**Solución:**
```bash
# Verificar que la API esté corriendo
curl http://localhost:5000/health

# Si no responde, iniciar Docker
cd /mnt/c/Users/aleja/solicitudes-api
docker compose up -d

# Verificar logs
docker compose logs -f api
```

### Problema: "Could not resolve host"

**Solución:**
- Asegúrate de que Docker esté corriendo
- Verifica que el contenedor `solicitudes-api` esté activo:
  ```bash
  docker compose ps
  ```

### Problema: "Unauthorized" en endpoints protegidos

**Solución:**
1. Haz login en `/api/usuarios/login`
2. Copia el `access_token`
3. Haz clic en **"Authorize"** (candado verde)
4. Ingresa: `Bearer TU_TOKEN`
5. Intenta de nuevo

### Problema: Token expirado

**Solución:**
- Los tokens expiran en 1 hora
- Haz login nuevamente para obtener un nuevo token
- Actualiza la autorización en Swagger

### Problema: No veo mis endpoints personalizados

**Solución:**
- Asegúrate de que el endpoint tenga docstring con formato YAML
- Debe incluir la línea `---` después de la descripción
- Reconstruye el contenedor: `docker compose up -d --build`

---

## 💡 Tips y Mejores Prácticas

### 1. **Mantén el token a mano**
Guarda tu token en un archivo de texto mientras desarrollas:
```bash
# Hacer login y guardar token
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' \
  | jq -r '.access_token' > token.txt

# Usar el token guardado
TOKEN=$(cat token.txt)
curl http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN"
```

### 2. **Usa la pestaña de Models**
En la parte inferior de Swagger, hay una sección "Models" que muestra:
- Todos los esquemas de datos
- Estructura completa de objetos
- Tipos de datos

### 3. **Copia el comando curl**
Después de hacer "Execute", Swagger muestra el comando curl equivalente. Útil para:
- Automatizar tests
- Compartir con el equipo
- Debugging

### 4. **Filtra por tag**
Si solo quieres ver endpoints de autenticación:
- Colapsa los demás tags
- O busca usando Ctrl+F

### 5. **Prueba diferentes códigos de error**
Prueba casos de error para ver las respuestas:
- Email incorrecto en login (401)
- Token inválido (401)
- Datos faltantes (400)
- Recurso no encontrado (404)

---

## 🔗 Enlaces Útiles

### URLs del Sistema
```
Frontend:       http://localhost:5173
Backend API:    http://localhost:5000
Swagger UI:     http://localhost:5000/api/docs
API Spec:       http://localhost:5000/apispec.json
Health Check:   http://localhost:5000/health
```

### Credenciales por Defecto
```
Admin:
  Email: admin@solicitudes.com
  Password: admin123

Jefe:
  Email: jefe@solicitudes.com
  Password: jefe123

Empleado:
  Email: empleado@solicitudes.com
  Password: empleado123
```

### Documentación Relacionada
- [SISTEMA_COMPLETO.md](./SISTEMA_COMPLETO.md) - Documentación completa del sistema
- [COMO_USAR_LA_API.md](./COMO_USAR_LA_API.md) - Guía práctica de la API
- [COMO_AGREGAR_USUARIOS.md](./COMO_AGREGAR_USUARIOS.md) - Gestión de usuarios

---

## 📈 Ventajas de Usar Swagger

✅ **Documentación siempre actualizada** - Se genera del código fuente
✅ **Testing interactivo** - No necesitas Postman ni curl
✅ **Onboarding rápido** - Nuevos desarrolladores entienden la API rápido
✅ **Estándar OpenAPI** - Compatible con miles de herramientas
✅ **Ejemplos automáticos** - Cada endpoint tiene ejemplos claros
✅ **Validación en tiempo real** - Ves errores antes de enviar
✅ **Exportable** - Puedes compartir la especificación

---

## 📞 Soporte

Si tienes problemas con Swagger:

1. **Revisa los logs:**
   ```bash
   docker compose logs -f api
   ```

2. **Verifica la especificación:**
   ```bash
   curl http://localhost:5000/apispec.json | python3 -m json.tool
   ```

3. **Reconstruye el contenedor:**
   ```bash
   docker compose down
   docker compose up -d --build
   ```

---

**¡Listo para explorar tu API! 🚀**

Abre [http://localhost:5000/api/docs](http://localhost:5000/api/docs) y comienza a probar tus endpoints.
