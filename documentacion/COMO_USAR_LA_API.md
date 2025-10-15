# 🔌 Guía Completa: Cómo Usar la API Directamente

Esta guía te enseña a interactuar directamente con la API sin el frontend, ver logs, probar endpoints y entender qué está pasando.

---

## 📋 Índice

1. [Ver Logs de la API](#ver-logs-de-la-api)
2. [Probar Endpoints con curl](#probar-endpoints-con-curl)
3. [Usar Postman/Insomnia](#usar-postmaninsomnia)
4. [Scripts Python para Pruebas](#scripts-python-para-pruebas)
5. [Ver Base de Datos Directamente](#ver-base-de-datos-directamente)
6. [Todos los Endpoints Disponibles](#todos-los-endpoints-disponibles)

---

## 📊 Ver Logs de la API

### Opción 1: Ver Logs en Tiempo Real

```bash
# Desde solicitudes-api/
docker compose logs -f api
```

**Qué verás:**
```
api  | [2025-10-15 16:50:23] INFO: POST /api/usuarios/login - 200
api  | [2025-10-15 16:50:25] INFO: GET /api/usuarios/usuarios - 200
api  | [2025-10-15 16:51:10] INFO: POST /api/usuarios/registro - 201
api  | [2025-10-15 16:51:15] WARNING: GET /api/usuarios/usuarios - 403 Forbidden
```

**Presiona Ctrl+C para salir**

---

### Opción 2: Ver Últimas 50 Líneas

```bash
docker compose logs --tail=50 api
```

---

### Opción 3: Ver Solo Errores

```bash
docker compose logs api | grep -i error
```

---

### Opción 4: Ver Logs de Todos los Servicios

```bash
# API + Base de datos + Redis
docker compose logs -f
```

---

## 🧪 Probar Endpoints con curl

### 1. Health Check (Sin Autenticación)

```bash
curl http://localhost:5000/health
```

**Respuesta:**
```json
{
  "service": "solicitudes-api",
  "status": "healthy"
}
```

---

### 2. Login (Obtener Token)

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@solicitudes.com",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login exitoso",
  "token_type": "Bearer",
  "usuario": {
    "activo": true,
    "apellido": "Sistema",
    "email": "admin@solicitudes.com",
    "id": 1,
    "nombre": "Admin",
    "rol": "administrador"
  }
}
```

**💡 Guarda el access_token para los siguientes comandos**

---

### 3. Listar Todos los Usuarios (Requiere Token)

```bash
# Reemplaza <TOKEN> con el access_token del login
curl -X GET http://localhost:5000/api/usuarios/usuarios \
  -H "Authorization: Bearer <TOKEN>"
```

**Respuesta:**
```json
{
  "current_page": 1,
  "pages": 1,
  "per_page": 10,
  "total": 5,
  "usuarios": [
    {
      "activo": true,
      "apellido": "Sistema",
      "created_at": "2025-10-15T14:41:37.158453",
      "email": "admin@solicitudes.com",
      "id": 1,
      "nombre": "Admin",
      "rol": "administrador"
    },
    ...
  ]
}
```

---

### 4. Crear Nuevo Usuario (Requiere Token de Admin)

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "email": "nuevo@empresa.com",
    "password": "password123",
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "rol": "empleado"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGc...",
  "message": "Usuario registrado exitosamente",
  "refresh_token": "eyJhbGc...",
  "token_type": "Bearer",
  "usuario": {
    "activo": true,
    "apellido": "Rodríguez",
    "created_at": "2025-10-15T17:30:15.123456",
    "email": "nuevo@empresa.com",
    "id": 6,
    "nombre": "Carlos",
    "rol": "empleado"
  }
}
```

---

### 5. Ver Usuario Específico

```bash
# Ver usuario con ID 3
curl -X GET http://localhost:5000/api/usuarios/usuarios/3 \
  -H "Authorization: Bearer <TOKEN>"
```

**Respuesta:**
```json
{
  "usuario": {
    "activo": true,
    "apellido": "García",
    "created_at": "2025-10-15T14:41:37.158459",
    "email": "empleado@solicitudes.com",
    "id": 3,
    "nombre": "María",
    "rol": "empleado"
  }
}
```

---

### 6. Cambiar Rol de Usuario (Solo Admin)

```bash
# Cambiar usuario 3 a "jefe"
curl -X PUT http://localhost:5000/api/usuarios/usuarios/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "rol": "jefe"
  }'
```

**Respuesta:**
```json
{
  "message": "Usuario actualizado exitosamente",
  "usuario": {
    "activo": true,
    "apellido": "García",
    "email": "empleado@solicitudes.com",
    "id": 3,
    "nombre": "María",
    "rol": "jefe"
  }
}
```

---

### 7. Desactivar Usuario (Solo Admin)

```bash
curl -X PUT http://localhost:5000/api/usuarios/usuarios/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "activo": false
  }'
```

---

### 8. Listar Solicitudes

```bash
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <TOKEN>"
```

---

### 9. Crear Nueva Solicitud

```bash
curl -X POST http://localhost:5000/api/solicitudes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "titulo": "Vacaciones de verano",
    "descripcion": "Solicito 2 semanas de vacaciones",
    "prioridad": "media"
  }'
```

---

### 10. Aprobar Solicitud (Jefe o Admin)

```bash
# Aprobar solicitud ID 5
curl -X PUT http://localhost:5000/api/solicitudes/5/estado \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "estado": "aprobada",
    "comentario": "Aprobado, disfruta tus vacaciones"
  }'
```

---

## 🎨 Usar Postman/Insomnia

### Configurar Postman

#### 1. Crear Colección

1. Abre Postman
2. Click en "New" → "Collection"
3. Nombre: "Solicitudes API"

#### 2. Configurar Variables

Click en la colección → pestaña "Variables":

```
Variable: base_url
Initial Value: http://localhost:5000/api
Current Value: http://localhost:5000/api

Variable: token
Initial Value: (vacío)
Current Value: (se llenará automáticamente)
```

#### 3. Crear Request de Login

**Request 1: Login**
```
Method: POST
URL: {{base_url}}/usuarios/login

Headers:
Content-Type: application/json

Body (raw, JSON):
{
  "email": "admin@solicitudes.com",
  "password": "admin123"
}

Tests (para guardar token automáticamente):
const response = pm.response.json();
pm.collectionVariables.set("token", response.access_token);
console.log("Token guardado:", response.access_token.substring(0, 20) + "...");
```

#### 4. Crear Request de Listar Usuarios

**Request 2: Listar Usuarios**
```
Method: GET
URL: {{base_url}}/usuarios/usuarios

Headers:
Authorization: Bearer {{token}}
```

#### 5. Crear Request de Crear Usuario

**Request 3: Crear Usuario**
```
Method: POST
URL: {{base_url}}/usuarios/registro

Headers:
Authorization: Bearer {{token}}
Content-Type: application/json

Body (raw, JSON):
{
  "email": "test@example.com",
  "password": "test123",
  "nombre": "Test",
  "apellido": "User",
  "rol": "empleado"
}
```

---

## 🐍 Scripts Python para Pruebas

### Script 1: Login y Listar Usuarios

Guarda como `test_api.py`:

```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000/api"

def login(email, password):
    """Login y obtener token"""
    response = requests.post(
        f"{BASE_URL}/usuarios/login",
        json={"email": email, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login exitoso como {data['usuario']['nombre']}")
        return data['access_token']
    else:
        print(f"❌ Error en login: {response.text}")
        return None

def listar_usuarios(token):
    """Listar todos los usuarios"""
    response = requests.get(
        f"{BASE_URL}/usuarios/usuarios",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\n👥 Total usuarios: {data['total']}")
        print("\nListado de usuarios:")
        print("-" * 80)

        for usuario in data['usuarios']:
            print(f"ID: {usuario['id']:2d} | {usuario['nombre']:15s} | {usuario['email']:30s} | {usuario['rol']:15s} | {'✅' if usuario['activo'] else '❌'}")

        return data['usuarios']
    else:
        print(f"❌ Error listando usuarios: {response.text}")
        return []

def crear_usuario(token, email, password, nombre, apellido, rol="empleado"):
    """Crear nuevo usuario"""
    response = requests.post(
        f"{BASE_URL}/usuarios/registro",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": email,
            "password": password,
            "nombre": nombre,
            "apellido": apellido,
            "rol": rol
        }
    )

    if response.status_code == 201:
        data = response.json()
        print(f"\n✅ Usuario creado: {data['usuario']['email']}")
        return data['usuario']
    else:
        print(f"\n❌ Error creando usuario: {response.json().get('error', 'Error desconocido')}")
        return None

def main():
    print("🚀 Prueba de API - Sistema de Solicitudes\n")

    # Login como admin
    token = login("admin@solicitudes.com", "admin123")

    if not token:
        print("No se pudo obtener token. Saliendo...")
        return

    # Listar usuarios
    usuarios = listar_usuarios(token)

    # Crear un usuario nuevo
    print("\n" + "="*80)
    print("Creando nuevo usuario...")
    print("="*80)

    crear_usuario(
        token,
        email="python.test@empresa.com",
        password="test123",
        nombre="Python",
        apellido="Test",
        rol="empleado"
    )

    # Listar usuarios nuevamente
    print("\n" + "="*80)
    print("Listado actualizado:")
    print("="*80)
    listar_usuarios(token)

if __name__ == "__main__":
    main()
```

**Ejecutar:**
```bash
python3 test_api.py
```

**Salida esperada:**
```
🚀 Prueba de API - Sistema de Solicitudes

✅ Login exitoso como Admin

👥 Total usuarios: 5

Listado de usuarios:
--------------------------------------------------------------------------------
ID:  1 | Admin           | admin@solicitudes.com          | administrador   | ✅
ID:  2 | Juan            | jefe@solicitudes.com           | jefe            | ✅
ID:  3 | María           | empleado@solicitudes.com       | empleado        | ✅
ID:  4 | Test            | test@test.com                  | empleado        | ✅
ID:  5 | Gaby            | test@calculadora.com           | empleado        | ✅

================================================================================
Creando nuevo usuario...
================================================================================

✅ Usuario creado: python.test@empresa.com

================================================================================
Listado actualizado:
================================================================================

👥 Total usuarios: 6
...
```

---

### Script 2: CRUD Completo de Usuarios

Guarda como `crud_usuarios.py`:

```python
#!/usr/bin/env python3
import requests
import sys

BASE_URL = "http://localhost:5000/api"

class APIClient:
    def __init__(self):
        self.token = None
        self.base_url = BASE_URL

    def login(self, email, password):
        """Login y guardar token"""
        response = requests.post(
            f"{self.base_url}/usuarios/login",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            self.token = response.json()['access_token']
            return True
        return False

    def headers(self):
        """Headers con autorización"""
        return {"Authorization": f"Bearer {self.token}"}

    def get_usuarios(self):
        """GET - Listar usuarios"""
        response = requests.get(
            f"{self.base_url}/usuarios/usuarios",
            headers=self.headers()
        )
        return response.json() if response.status_code == 200 else None

    def get_usuario(self, usuario_id):
        """GET - Ver usuario específico"""
        response = requests.get(
            f"{self.base_url}/usuarios/usuarios/{usuario_id}",
            headers=self.headers()
        )
        return response.json() if response.status_code == 200 else None

    def crear_usuario(self, email, password, nombre, apellido, rol="empleado"):
        """POST - Crear usuario"""
        response = requests.post(
            f"{self.base_url}/usuarios/registro",
            headers=self.headers(),
            json={
                "email": email,
                "password": password,
                "nombre": nombre,
                "apellido": apellido,
                "rol": rol
            }
        )
        return response.json() if response.status_code == 201 else None

    def actualizar_usuario(self, usuario_id, **kwargs):
        """PUT - Actualizar usuario"""
        response = requests.put(
            f"{self.base_url}/usuarios/usuarios/{usuario_id}",
            headers=self.headers(),
            json=kwargs
        )
        return response.json() if response.status_code == 200 else None

    def eliminar_usuario(self, usuario_id):
        """DELETE - Eliminar usuario"""
        response = requests.delete(
            f"{self.base_url}/usuarios/usuarios/{usuario_id}",
            headers=self.headers()
        )
        return response.status_code == 200

def menu():
    """Menú interactivo"""
    client = APIClient()

    print("=" * 80)
    print("API CLIENT - Sistema de Solicitudes")
    print("=" * 80)

    # Login
    if not client.login("admin@solicitudes.com", "admin123"):
        print("❌ Error en login")
        sys.exit(1)

    print("✅ Login exitoso\n")

    while True:
        print("\n" + "=" * 80)
        print("MENÚ PRINCIPAL")
        print("=" * 80)
        print("1. Listar usuarios")
        print("2. Ver usuario específico")
        print("3. Crear usuario")
        print("4. Cambiar rol de usuario")
        print("5. Activar/desactivar usuario")
        print("6. Eliminar usuario")
        print("0. Salir")
        print("=" * 80)

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            # Listar usuarios
            data = client.get_usuarios()
            if data:
                print(f"\n👥 Total: {data['total']} usuarios\n")
                for u in data['usuarios']:
                    estado = "✅" if u['activo'] else "❌"
                    print(f"{estado} [{u['id']}] {u['nombre']} {u['apellido']} - {u['email']} ({u['rol']})")

        elif opcion == "2":
            # Ver usuario específico
            uid = input("ID del usuario: ").strip()
            data = client.get_usuario(uid)
            if data:
                u = data['usuario']
                print(f"\n📋 Detalles del usuario:")
                print(f"   ID: {u['id']}")
                print(f"   Nombre: {u['nombre']} {u['apellido']}")
                print(f"   Email: {u['email']}")
                print(f"   Rol: {u['rol']}")
                print(f"   Activo: {'Sí' if u['activo'] else 'No'}")
                print(f"   Creado: {u['created_at']}")

        elif opcion == "3":
            # Crear usuario
            print("\n➕ Crear nuevo usuario")
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            print("Rol (1=empleado, 2=jefe, 3=admin): ", end="")
            rol_num = input().strip()

            roles = {"1": "empleado", "2": "jefe", "3": "administrador"}
            rol = roles.get(rol_num, "empleado")

            result = client.crear_usuario(email, password, nombre, apellido, rol)
            if result:
                print(f"\n✅ Usuario creado con ID: {result['usuario']['id']}")

        elif opcion == "4":
            # Cambiar rol
            uid = input("ID del usuario: ").strip()
            print("Nuevo rol (1=empleado, 2=jefe, 3=admin): ", end="")
            rol_num = input().strip()

            roles = {"1": "empleado", "2": "jefe", "3": "administrador"}
            rol = roles.get(rol_num)

            if rol:
                result = client.actualizar_usuario(uid, rol=rol)
                if result:
                    print(f"\n✅ Rol actualizado a: {rol}")

        elif opcion == "5":
            # Activar/desactivar
            uid = input("ID del usuario: ").strip()
            estado = input("Activar (s/n): ").strip().lower()
            activo = estado == 's'

            result = client.actualizar_usuario(uid, activo=activo)
            if result:
                print(f"\n✅ Usuario {'activado' if activo else 'desactivado'}")

        elif opcion == "6":
            # Eliminar
            uid = input("ID del usuario: ").strip()
            confirmar = input(f"¿Eliminar usuario {uid}? (s/n): ").strip().lower()

            if confirmar == 's':
                if client.eliminar_usuario(uid):
                    print(f"\n✅ Usuario {uid} eliminado")
                else:
                    print(f"\n❌ Error eliminando usuario")

        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break

        else:
            print("\n⚠️ Opción inválida")

if __name__ == "__main__":
    menu()
```

**Ejecutar:**
```bash
python3 crud_usuarios.py
```

---

## 🗄️ Ver Base de Datos Directamente

### Conectarse a PostgreSQL

```bash
# Desde solicitudes-api/
docker compose exec db psql -U postgres solicitudes_db
```

**Ahora estás en la consola de PostgreSQL:**

```sql
-- Ver todas las tablas
\dt

-- Ver usuarios
SELECT id, email, nombre, apellido, rol, activo FROM usuarios;

-- Ver solicitudes
SELECT id, titulo, estado, prioridad, usuario_id FROM solicitudes;

-- Ver usuario con sus solicitudes
SELECT
    u.nombre,
    u.email,
    s.titulo,
    s.estado
FROM usuarios u
LEFT JOIN solicitudes s ON u.id = s.usuario_id
WHERE u.id = 1;

-- Contar usuarios por rol
SELECT rol, COUNT(*) as cantidad
FROM usuarios
GROUP BY rol;

-- Salir
\q
```

---

### Ver Datos con Herramientas Gráficas

**DBeaver / pgAdmin / TablePlus:**

```
Host: localhost
Port: 5432
Database: solicitudes_db
Username: postgres
Password: postgres
```

---

## 📚 Todos los Endpoints Disponibles

### Autenticación y Usuarios

| Método | Endpoint | Autenticación | Rol | Descripción |
|--------|----------|---------------|-----|-------------|
| `POST` | `/api/usuarios/registro` | Opcional | - | Crear usuario (empleado) o con rol (admin) |
| `POST` | `/api/usuarios/login` | No | - | Iniciar sesión |
| `GET` | `/api/usuarios/perfil` | Sí | - | Ver mi perfil |
| `PUT` | `/api/usuarios/perfil` | Sí | - | Actualizar mi perfil |
| `POST` | `/api/usuarios/cambiar-password` | Sí | - | Cambiar mi contraseña |
| `GET` | `/api/usuarios/usuarios` | Sí | jefe, admin | Listar todos los usuarios |
| `GET` | `/api/usuarios/usuarios/:id` | Sí | jefe, admin | Ver usuario específico |
| `PUT` | `/api/usuarios/usuarios/:id` | Sí | admin | Actualizar usuario (rol, activo) |
| `DELETE` | `/api/usuarios/usuarios/:id` | Sí | admin | Eliminar usuario |

### Solicitudes

| Método | Endpoint | Autenticación | Rol | Descripción |
|--------|----------|---------------|-----|-------------|
| `GET` | `/api/solicitudes` | Sí | - | Listar mis solicitudes (o todas si jefe/admin) |
| `GET` | `/api/solicitudes/:id` | Sí | - | Ver solicitud específica |
| `POST` | `/api/solicitudes` | Sí | - | Crear nueva solicitud |
| `PUT` | `/api/solicitudes/:id` | Sí | - | Actualizar mi solicitud (solo pendientes) |
| `DELETE` | `/api/solicitudes/:id` | Sí | - | Eliminar mi solicitud (solo pendientes) |
| `PUT` | `/api/solicitudes/:id/estado` | Sí | jefe, admin | Aprobar/rechazar solicitud |

### Sistema

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| `GET` | `/health` | No | Health check |
| `GET` | `/api/notificaciones` | Sí | Ver mis notificaciones |

---

## 🔍 Debugging Avanzado

### Ver todas las requests en tiempo real

```bash
# Terminal 1: Ver logs de API
docker compose logs -f api

# Terminal 2: Hacer requests
curl http://localhost:5000/api/usuarios/usuarios \
  -H "Authorization: Bearer <TOKEN>"
```

**En los logs verás:**
```
api  | [2025-10-15 17:45:30] INFO: GET /api/usuarios/usuarios
api  | [2025-10-15 17:45:30] INFO: Usuario autenticado: admin@solicitudes.com (ID: 1, Rol: administrador)
api  | [2025-10-15 17:45:30] INFO: Query: SELECT * FROM usuarios
api  | [2025-10-15 17:45:30] INFO: Retornando 5 usuarios
api  | [2025-10-15 17:45:30] INFO: Response 200 - 0.032s
```

---

### Inspeccionar una Request Completa

```bash
# Con verbose (-v) para ver headers
curl -v http://localhost:5000/health

# Resultado:
> GET /health HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.68.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Werkzeug/2.3.0 Python/3.11.0
< Date: Wed, 15 Oct 2025 17:50:00 GMT
< Content-Type: application/json
< Content-Length: 58
<
{"service":"solicitudes-api","status":"healthy"}
```

---

## 🎯 Casos de Uso Comunes

### 1. Probar todo el flujo de un usuario nuevo

```bash
# 1. Crear usuario
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","nombre":"Test","apellido":"User"}'

# 2. Login con ese usuario
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# 3. Crear solicitud con su token
curl -X POST http://localhost:5000/api/solicitudes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_DEL_NUEVO_USUARIO>" \
  -d '{"titulo":"Mi primera solicitud","descripcion":"Test","prioridad":"media"}'

# 4. Ver sus solicitudes
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <TOKEN_DEL_NUEVO_USUARIO>"
```

---

## 📊 Resumen de Herramientas

| Herramienta | Uso | Comando |
|------------|-----|---------|
| **curl** | Pruebas rápidas en terminal | `curl -X GET http://...` |
| **Postman** | Colecciones organizadas, UI gráfica | Descarga en postman.com |
| **Python** | Automatización, scripts, tests | `python3 script.py` |
| **Docker logs** | Ver qué está pasando en la API | `docker compose logs -f api` |
| **psql** | Consultar base de datos directamente | `docker compose exec db psql...` |

---

## 🚀 Siguiente Nivel

### Automatizar Tests con pytest

```python
# test_usuarios.py
import pytest
import requests

BASE_URL = "http://localhost:5000/api"

@pytest.fixture
def admin_token():
    response = requests.post(
        f"{BASE_URL}/usuarios/login",
        json={"email": "admin@solicitudes.com", "password": "admin123"}
    )
    return response.json()['access_token']

def test_listar_usuarios(admin_token):
    response = requests.get(
        f"{BASE_URL}/usuarios/usuarios",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'usuarios' in response.json()
    assert len(response.json()['usuarios']) > 0

def test_crear_usuario(admin_token):
    response = requests.post(
        f"{BASE_URL}/usuarios/registro",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "email": "pytest@test.com",
            "password": "test123",
            "nombre": "Pytest",
            "apellido": "Test",
            "rol": "empleado"
        }
    )
    assert response.status_code == 201
    assert response.json()['usuario']['email'] == "pytest@test.com"
```

**Ejecutar:**
```bash
pip install pytest requests
pytest test_usuarios.py -v
```

---

**¿Qué quieres probar ahora?**
- Ver logs en tiempo real mientras usas el frontend
- Crear un script Python personalizado
- Configurar Postman con todos los endpoints
- Ver la base de datos directamente
