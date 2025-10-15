# 📚 Documentación Completa del Sistema de Solicitudes

Esta es la guía completa que explica cómo funciona todo el sistema, desde la arquitectura hasta los comandos prácticos para administrarlo.

---

## 📋 Tabla de Contenidos

1. [Arquitectura del Sistema](#-arquitectura-del-sistema)
2. [Componentes del Sistema](#-componentes-del-sistema)
3. [Flujo de Datos Completo](#-flujo-de-datos-completo)
4. [Comandos por Componente](#-comandos-por-componente)
5. [API Endpoints Completos](#-api-endpoints-completos)
6. [Base de Datos](#-base-de-datos)
7. [Autenticación y Seguridad](#-autenticación-y-seguridad)
8. [Casos de Uso Prácticos](#-casos-de-uso-prácticos)
9. [Monitoreo y Logs](#-monitoreo-y-logs)
10. [Troubleshooting](#-troubleshooting)

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         NAVEGADOR                               │
│                    http://localhost:5173                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              React Frontend (Vite)                        │ │
│  │  - React 19                                               │ │
│  │  - React Router (navegación)                              │ │
│  │  - Axios (HTTP client)                                    │ │
│  │  - Context API (estado global)                            │ │
│  │  - CSS Modules (estilos)                                  │ │
│  └───────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTP/REST API
                           │ JSON
                           │ JWT Bearer Token
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER CONTAINERS                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           API Backend (Flask)                            │  │
│  │           http://localhost:5000                          │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Flask Application                                 │  │  │
│  │  │  - Flask 3.0                                       │  │  │
│  │  │  - Flask-SQLAlchemy (ORM)                          │  │  │
│  │  │  - Flask-JWT-Extended (auth)                       │  │  │
│  │  │  - Flask-CORS                                      │  │  │
│  │  │  - Werkzeug (WSGI)                                 │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Blueprints (Módulos)                              │  │  │
│  │  │  - auth_bp: /api/usuarios/*                        │  │  │
│  │  │  - solicitudes_bp: /api/solicitudes/*              │  │  │
│  │  │  - notificaciones_bp: /api/notificaciones/*        │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Services (Lógica de Negocio)                      │  │  │
│  │  │  - auth_service.py                                 │  │  │
│  │  │  - solicitudes_service.py                          │  │  │
│  │  │  - notificaciones_service.py                       │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Models (ORM)                                      │  │  │
│  │  │  - Usuario                                         │  │  │
│  │  │  - Solicitud                                       │  │  │
│  │  │  - Notificacion                                    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                      │
│                         │ SQL Queries                          │
│                         │ SQLAlchemy ORM                       │
│                         ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           PostgreSQL Database                            │  │
│  │           localhost:5432                                 │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Tables:                                           │  │  │
│  │  │  - usuarios (users con roles)                      │  │  │
│  │  │  - solicitudes (requests)                          │  │  │
│  │  │  - notificaciones (notifications)                  │  │  │
│  │  │  - alembic_version (migrations)                    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Redis Cache                                    │  │
│  │           localhost:6379                                 │  │
│  │  - Session storage                                       │  │
│  │  - Task queue (Celery)                                   │  │
│  │  - Cache de consultas                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Celery Worker                                  │  │
│  │  - Tareas asíncronas                                     │  │
│  │  - Envío de emails                                       │  │
│  │  - Notificaciones                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Stack Tecnológico Completo

**Frontend:**
- React 19.0.0
- React Router DOM 7.1.1
- Axios 1.7.9
- Vite 7.1.10

**Backend:**
- Python 3.11
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- PostgreSQL 15
- Redis 7.2
- Celery 5.3.4

**DevOps:**
- Docker 24.0
- Docker Compose 2.23
- WSL2 (Windows Subsystem for Linux)

---

## 🔧 Componentes del Sistema

### 1. Frontend (React)

**Ubicación:** `solicitudes-frontend/`

**Propósito:** Interfaz de usuario para interactuar con el sistema

**Tecnologías:**
- **React 19**: Biblioteca UI con hooks
- **React Router**: Navegación entre páginas
- **Axios**: Cliente HTTP para llamadas API
- **Context API**: Manejo de estado global (autenticación)

**Estructura:**
```
solicitudes-frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── Navbar.jsx       # Barra de navegación
│   │   └── ProtectedRoute.jsx # Rutas protegidas
│   ├── pages/               # Páginas de la aplicación
│   │   ├── Login.jsx        # Página de inicio de sesión
│   │   ├── Dashboard.jsx    # Dashboard principal
│   │   ├── Solicitudes.jsx  # Lista de solicitudes
│   │   ├── NuevaSolicitud.jsx # Crear solicitud
│   │   ├── DetalleSolicitud.jsx # Ver/aprobar solicitud
│   │   └── GestionUsuarios.jsx # Admin: gestionar usuarios
│   ├── context/             # Context API
│   │   └── AuthContext.jsx  # Contexto de autenticación
│   ├── api/                 # Configuración de API
│   │   └── client.js        # Cliente Axios configurado
│   └── App.jsx              # Componente raíz con rutas
└── package.json             # Dependencias
```

**Comandos:**
```bash
# Ver estructura del frontend
cd solicitudes-frontend
tree -L 2 src/

# Ver dependencias
cat package.json

# Ver rutas configuradas
grep -A 3 "Route path" src/App.jsx

# Iniciar servidor de desarrollo
npm run dev

# Ver logs del servidor
# (Los logs aparecen en la terminal donde ejecutaste npm run dev)
```

---

### 2. Backend API (Flask)

**Ubicación:** `solicitudes-api/`

**Propósito:** API REST que maneja toda la lógica de negocio

**Tecnologías:**
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para base de datos
- **JWT**: Autenticación con tokens
- **Bcrypt**: Hash de contraseñas

**Estructura:**
```
solicitudes-api/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── routes/              # Blueprints (rutas)
│   │   ├── auth.py          # /api/usuarios/*
│   │   ├── solicitudes.py   # /api/solicitudes/*
│   │   └── notificaciones.py # /api/notificaciones/*
│   ├── models/              # Modelos de base de datos
│   │   ├── usuario.py       # Modelo Usuario
│   │   ├── solicitud.py     # Modelo Solicitud
│   │   └── notificacion.py  # Modelo Notificacion
│   ├── services/            # Lógica de negocio
│   │   ├── auth_service.py
│   │   └── solicitudes_service.py
│   └── utils/               # Utilidades
├── migrations/              # Migraciones de BD
├── config.py               # Configuración
├── run.py                  # Entry point
└── docker-compose.yml      # Docker configuration
```

**Comandos:**
```bash
# Ver estructura del backend
cd solicitudes-api
tree -L 2 app/

# Ver modelos de base de datos
cat app/models/usuario.py

# Ver blueprints (rutas)
ls -la app/routes/

# Ver configuración
cat config.py | grep -v "^#"

# Ver logs en tiempo real
docker compose logs -f api

# Ver últimos 100 logs
docker compose logs --tail=100 api

# Entrar al contenedor de la API
docker compose exec api bash

# Ver variables de entorno
docker compose exec api env | grep -E "DATABASE|JWT|FLASK"
```

---

### 3. Base de Datos (PostgreSQL)

**Ubicación:** Contenedor Docker `db`

**Propósito:** Almacenar todos los datos del sistema

**Tablas:**
- `usuarios`: Usuarios del sistema
- `solicitudes`: Solicitudes creadas
- `notificaciones`: Notificaciones del sistema
- `alembic_version`: Control de migraciones

**Comandos:**
```bash
# Conectarse a PostgreSQL
docker compose exec db psql -U postgres solicitudes_db

# Dentro de PostgreSQL:

# Ver todas las tablas
\dt

# Describir estructura de tabla usuarios
\d usuarios

# Ver todos los usuarios
SELECT id, nombre, email, rol, activo FROM usuarios;

# Contar usuarios por rol
SELECT rol, COUNT(*) as cantidad FROM usuarios GROUP BY rol;

# Ver solicitudes con usuario
SELECT 
    u.nombre,
    u.email,
    s.titulo,
    s.estado,
    s.created_at
FROM usuarios u
JOIN solicitudes s ON u.id = s.usuario_id
ORDER BY s.created_at DESC
LIMIT 10;

# Ver estadísticas
SELECT 
    estado,
    COUNT(*) as cantidad
FROM solicitudes
GROUP BY estado;

# Salir
\q
```

**Backup y Restore:**
```bash
# Hacer backup
docker compose exec db pg_dump -U postgres solicitudes_db > backup.sql

# Restaurar backup
docker compose exec -T db psql -U postgres solicitudes_db < backup.sql
```

---

### 4. Redis (Cache y Queue)

**Ubicación:** Contenedor Docker `redis`

**Propósito:** 
- Cache de sesiones
- Cola de tareas para Celery
- Cache de consultas frecuentes

**Comandos:**
```bash
# Conectarse a Redis
docker compose exec redis redis-cli

# Dentro de Redis:

# Ver todas las claves
KEYS *

# Ver información del servidor
INFO

# Ver estadísticas de memoria
INFO memory

# Ver clientes conectados
CLIENT LIST

# Limpiar toda la cache
FLUSHALL

# Salir
EXIT
```

---

### 5. Celery (Tareas Asíncronas)

**Ubicación:** Contenedor Docker `celery`

**Propósito:**
- Envío de emails
- Tareas programadas
- Procesamiento en background

**Comandos:**
```bash
# Ver logs de Celery
docker compose logs -f celery

# Ver tareas activas
docker compose exec celery celery -A app.celery inspect active

# Ver tareas programadas
docker compose exec celery celery -A app.celery inspect scheduled

# Ver estadísticas
docker compose exec celery celery -A app.celery inspect stats
```

---

## 🔄 Flujo de Datos Completo

### Flujo 1: Login de Usuario

```
┌─────────────┐
│  USUARIO    │
│  (Navegador)│
└──────┬──────┘
       │
       │ 1. Ingresa email y password
       │    en formulario de login
       ▼
┌─────────────────────────────┐
│  Frontend (Login.jsx)       │
│  http://localhost:5173      │
└──────┬──────────────────────┘
       │
       │ 2. POST /api/usuarios/login
       │    Body: {email, password}
       ▼
┌─────────────────────────────┐
│  API (auth.py)              │
│  http://localhost:5000      │
│                             │
│  @auth_bp.route('/login')   │
└──────┬──────────────────────┘
       │
       │ 3. Buscar usuario en BD
       │    autenticar_usuario()
       ▼
┌─────────────────────────────┐
│  Service (auth_service.py)  │
│                             │
│  def autenticar_usuario():  │
│    - Buscar por email       │
│    - Verificar password     │
│    - Verificar que esté     │
│      activo                 │
└──────┬──────────────────────┘
       │
       │ 4. SELECT * FROM usuarios
       │    WHERE email = ?
       ▼
┌─────────────────────────────┐
│  PostgreSQL                 │
│                             │
│  Table: usuarios            │
└──────┬──────────────────────┘
       │
       │ 5. Usuario encontrado
       │    {id, email, password_hash, rol}
       ▼
┌─────────────────────────────┐
│  Service (auth_service.py)  │
│                             │
│  check_password_hash()      │
│  - Comparar hash de Bcrypt  │
└──────┬──────────────────────┘
       │
       │ 6. Password válida
       │    crear_tokens()
       ▼
┌─────────────────────────────┐
│  JWT Service                │
│                             │
│  create_access_token()      │
│  - Genera JWT con user_id   │
│  - Expira en 1 hora         │
│                             │
│  create_refresh_token()     │
│  - Expira en 30 días        │
└──────┬──────────────────────┘
       │
       │ 7. Response 200
       │    {
       │      access_token: "eyJ...",
       │      refresh_token: "eyJ...",
       │      usuario: {...}
       │    }
       ▼
┌─────────────────────────────┐
│  Frontend (Login.jsx)       │
│                             │
│  Recibe tokens y usuario    │
└──────┬──────────────────────┘
       │
       │ 8. Guardar en localStorage
       │    localStorage.setItem('access_token')
       │    setUser(usuario)
       ▼
┌─────────────────────────────┐
│  Context (AuthContext)      │
│                             │
│  Estado global actualizado  │
└──────┬──────────────────────┘
       │
       │ 9. Redireccionar
       │    navigate('/dashboard')
       ▼
┌─────────────────────────────┐
│  Dashboard                  │
│  Usuario autenticado ✅     │
└─────────────────────────────┘
```

### Flujo 2: Crear Usuario (Desde Frontend Admin)

```
┌─────────────┐
│  ADMIN      │
│  (Navegador)│
└──────┬──────┘
       │
       │ 1. Click "Nuevo Usuario"
       │    Completa formulario
       ▼
┌─────────────────────────────┐
│  GestionUsuarios.jsx        │
│                             │
│  handleCreateUsuario()      │
└──────┬──────────────────────┘
       │
       │ 2. POST /api/usuarios/registro
       │    Headers: Authorization: Bearer <token>
       │    Body: {email, password, nombre, apellido, rol}
       ▼
┌─────────────────────────────┐
│  API (auth.py)              │
│  @auth_bp.route('/registro')│
└──────┬──────────────────────┘
       │
       │ 3. Validar campos requeridos
       │    email, password, nombre
       ▼
┌─────────────────────────────┐
│  Service (auth_service.py)  │
│  registrar_usuario()        │
│                             │
│  1. Verificar email único   │
│  2. Validar rol             │
│  3. Crear instancia Usuario │
│  4. Hash de password        │
└──────┬──────────────────────┘
       │
       │ 4. SELECT * FROM usuarios
       │    WHERE email = ?
       ▼
┌─────────────────────────────┐
│  PostgreSQL                 │
│                             │
│  Verificar duplicado        │
└──────┬──────────────────────┘
       │
       │ 5. Email no existe ✅
       ▼
┌─────────────────────────────┐
│  Modelo (usuario.py)        │
│                             │
│  usuario = Usuario()        │
│  usuario.password = "..."   │
│  -> llama @password.setter  │
│  -> genera hash con Bcrypt  │
└──────┬──────────────────────┘
       │
       │ 6. INSERT INTO usuarios
       │    (email, password_hash, nombre, apellido, rol, activo)
       │    VALUES (?, ?, ?, ?, ?, true)
       ▼
┌─────────────────────────────┐
│  PostgreSQL                 │
│                             │
│  Nuevo registro insertado   │
│  RETURNING id               │
└──────┬──────────────────────┘
       │
       │ 7. Usuario creado
       │    usuario.id = 8
       ▼
┌─────────────────────────────┐
│  Service                    │
│  crear_tokens(usuario)      │
└──────┬──────────────────────┘
       │
       │ 8. Response 201
       │    {
       │      message: "Usuario registrado...",
       │      usuario: {...},
       │      access_token: "...",
       │      refresh_token: "..."
       │    }
       ▼
┌─────────────────────────────┐
│  Frontend                   │
│  setSuccess()               │
│  loadUsuarios()             │
│  setShowModal(false)        │
└──────┬──────────────────────┘
       │
       │ 9. Actualizar tabla
       ▼
┌─────────────────────────────┐
│  Tabla de usuarios          │
│  Nuevo usuario visible ✅   │
└─────────────────────────────┘
```

---

## 🎯 Comandos por Componente

### Docker

```bash
# Ver estado de todos los contenedores
docker ps

# Ver logs de todos los servicios
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f api
docker compose logs -f db
docker compose logs -f redis

# Reiniciar un servicio
docker compose restart api

# Reiniciar todos los servicios
docker compose restart

# Detener todos los servicios
docker compose down

# Iniciar todos los servicios
docker compose up -d

# Ver uso de recursos
docker stats

# Limpiar recursos no usados
docker system prune -a
```

### Frontend

```bash
# Cambiar al directorio
cd solicitudes-frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview

# Limpiar caché
rm -rf node_modules/.vite dist

# Ver estructura de rutas
cat src/App.jsx | grep -E "Route path"

# Ver contexto de autenticación
cat src/context/AuthContext.jsx

# Ver componentes
ls -la src/components/

# Ver páginas
ls -la src/pages/
```

### Backend API

```bash
# Ver logs en tiempo real
docker compose logs -f api

# Ejecutar comando dentro del contenedor
docker compose exec api bash

# Ver rutas registradas
docker compose exec api python -c "from app import create_app; app = create_app(); print(app.url_map)"

# Ver variables de entorno
docker compose exec api env | sort

# Ejecutar shell de Python
docker compose exec api python

# Correr tests
docker compose exec api pytest

# Ver estructura del proyecto
docker compose exec api tree -L 2 /app
```

### Base de Datos

```bash
# Conectarse a PostgreSQL
docker compose exec db psql -U postgres solicitudes_db

# Dentro de psql:
\dt                          # Ver tablas
\d usuarios                  # Ver estructura de tabla
\du                          # Ver usuarios de PostgreSQL
\l                           # Ver todas las bases de datos

# Queries útiles (desde psql):

# Ver todos los usuarios del sistema
SELECT id, nombre, email, rol, activo, created_at FROM usuarios ORDER BY id;

# Contar por rol
SELECT rol, COUNT(*) FROM usuarios GROUP BY rol;

# Ver solicitudes recientes
SELECT id, titulo, estado, usuario_id, created_at 
FROM solicitudes 
ORDER BY created_at DESC 
LIMIT 10;

# Buscar usuario por email
SELECT * FROM usuarios WHERE email LIKE '%test%';

# Ver usuarios inactivos
SELECT * FROM usuarios WHERE activo = false;

# Desde fuera de psql (una sola línea):
docker compose exec db psql -U postgres solicitudes_db -c "SELECT COUNT(*) FROM usuarios;"
```

### Redis

```bash
# Conectarse a Redis CLI
docker compose exec redis redis-cli

# Dentro de redis-cli:
KEYS *                       # Ver todas las claves
GET session:123              # Ver valor de una clave
TTL session:123              # Ver tiempo de vida
INFO                         # Información del servidor
DBSIZE                       # Cantidad de claves
FLUSHALL                     # Limpiar todo (¡cuidado!)

# Desde fuera de redis-cli:
docker compose exec redis redis-cli KEYS '*'
docker compose exec redis redis-cli INFO stats
```

---

## 📡 API Endpoints Completos

### Autenticación y Usuarios

| Método | Endpoint | Auth | Rol Requerido | Descripción | Body |
|--------|----------|------|---------------|-------------|------|
| `POST` | `/api/usuarios/registro` | Opcional | - (admin para roles) | Crear usuario | `{email, password, nombre, apellido, rol?}` |
| `POST` | `/api/usuarios/login` | No | - | Iniciar sesión | `{email, password}` |
| `GET` | `/api/usuarios/perfil` | Sí | - | Ver mi perfil | - |
| `PUT` | `/api/usuarios/perfil` | Sí | - | Actualizar mi perfil | `{nombre?, apellido?}` |
| `POST` | `/api/usuarios/cambiar-password` | Sí | - | Cambiar contraseña | `{password_actual, password_nueva}` |
| `GET` | `/api/usuarios/usuarios` | Sí | jefe, admin | Listar usuarios | Query: `?rol=&activo=&page=&per_page=` |
| `GET` | `/api/usuarios/usuarios/:id` | Sí | jefe, admin | Ver usuario | - |
| `PUT` | `/api/usuarios/usuarios/:id` | Sí | admin | Actualizar usuario | `{nombre?, apellido?, rol?, activo?}` |
| `DELETE` | `/api/usuarios/usuarios/:id` | Sí | admin | Eliminar usuario | - |

### Solicitudes

| Método | Endpoint | Auth | Rol Requerido | Descripción | Body |
|--------|----------|------|---------------|-------------|------|
| `GET` | `/api/solicitudes` | Sí | - | Listar solicitudes | Query: `?estado=&prioridad=&page=` |
| `GET` | `/api/solicitudes/:id` | Sí | - | Ver solicitud | - |
| `POST` | `/api/solicitudes` | Sí | - | Crear solicitud | `{titulo, descripcion, prioridad, tipo?, fecha_requerida?}` |
| `PUT` | `/api/solicitudes/:id` | Sí | - (solo propias) | Actualizar solicitud | `{titulo?, descripcion?, prioridad?}` |
| `DELETE` | `/api/solicitudes/:id` | Sí | - (solo propias pendientes) | Eliminar solicitud | - |
| `PUT` | `/api/solicitudes/:id/estado` | Sí | jefe, admin | Aprobar/rechazar | `{estado, comentario?}` |

### Sistema

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| `GET` | `/health` | No | Health check |
| `GET` | `/api/notificaciones` | Sí | Ver notificaciones |
| `PUT` | `/api/notificaciones/:id/leida` | Sí | Marcar como leída |

---

## 💾 Base de Datos

### Esquema de Tablas

#### Tabla: `usuarios`

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    rol VARCHAR(20) NOT NULL DEFAULT 'empleado',
    activo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);
CREATE INDEX idx_usuarios_activo ON usuarios(activo);
```

**Roles válidos:** `empleado`, `jefe`, `administrador`

#### Tabla: `solicitudes`

```sql
CREATE TABLE solicitudes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    aprobador_id INTEGER REFERENCES usuarios(id),
    tipo VARCHAR(50) DEFAULT 'general',
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    prioridad VARCHAR(20) NOT NULL DEFAULT 'media',
    comentarios TEXT,
    fecha_requerida DATE,
    fecha_aprobacion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_solicitudes_usuario ON solicitudes(usuario_id);
CREATE INDEX idx_solicitudes_estado ON solicitudes(estado);
CREATE INDEX idx_solicitudes_prioridad ON solicitudes(prioridad);
```

**Estados válidos:** `pendiente`, `aprobada`, `rechazada`, `en_proceso`, `completada`
**Prioridades:** `baja`, `media`, `alta`, `urgente`

#### Tabla: `notificaciones`

```sql
CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    solicitud_id INTEGER REFERENCES solicitudes(id),
    tipo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notificaciones_usuario ON notificaciones(usuario_id);
CREATE INDEX idx_notificaciones_leida ON notificaciones(leida);
```

### Comandos SQL Útiles

```bash
# Conectarse
docker compose exec db psql -U postgres solicitudes_db
```

```sql
-- ============================================
-- USUARIOS
-- ============================================

-- Ver todos los usuarios
SELECT id, nombre, apellido, email, rol, activo 
FROM usuarios 
ORDER BY id;

-- Buscar usuario por email
SELECT * FROM usuarios WHERE email = 'admin@solicitudes.com';

-- Contar usuarios por rol
SELECT rol, COUNT(*) as cantidad 
FROM usuarios 
GROUP BY rol;

-- Crear usuario manualmente (NO recomendado, usar API)
-- La contraseña debe estar hasheada con Bcrypt
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol, activo)
VALUES ('test@test.com', '$2b$12$...hash...', 'Test', 'User', 'empleado', true);

-- Cambiar rol de usuario
UPDATE usuarios 
SET rol = 'jefe' 
WHERE id = 3;

-- Desactivar usuario
UPDATE usuarios 
SET activo = false 
WHERE id = 5;

-- Eliminar usuario (cuidado con foreign keys)
DELETE FROM usuarios WHERE id = 10;

-- ============================================
-- SOLICITUDES
-- ============================================

-- Ver todas las solicitudes con usuario
SELECT 
    s.id,
    s.titulo,
    s.estado,
    s.prioridad,
    u.nombre || ' ' || u.apellido as solicitante,
    s.created_at
FROM solicitudes s
JOIN usuarios u ON s.usuario_id = u.id
ORDER BY s.created_at DESC;

-- Solicitudes pendientes
SELECT * FROM solicitudes WHERE estado = 'pendiente';

-- Solicitudes por usuario
SELECT * FROM solicitudes WHERE usuario_id = 1;

-- Estadísticas de solicitudes
SELECT 
    estado,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM solicitudes), 2) as porcentaje
FROM solicitudes
GROUP BY estado;

-- Solicitudes por prioridad
SELECT prioridad, COUNT(*) 
FROM solicitudes 
GROUP BY prioridad 
ORDER BY 
    CASE prioridad
        WHEN 'urgente' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baja' THEN 4
    END;

-- Solicitudes aprobadas en el último mes
SELECT * FROM solicitudes 
WHERE estado = 'aprobada' 
AND fecha_aprobacion >= NOW() - INTERVAL '1 month';

-- ============================================
-- CONSULTAS COMPLEJAS
-- ============================================

-- Dashboard de un jefe: Ver todas las solicitudes pendientes
SELECT 
    s.id,
    s.titulo,
    s.prioridad,
    s.created_at,
    u.nombre || ' ' || u.apellido as solicitante,
    u.email
FROM solicitudes s
JOIN usuarios u ON s.usuario_id = u.id
WHERE s.estado = 'pendiente'
ORDER BY 
    CASE s.prioridad
        WHEN 'urgente' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baja' THEN 4
    END,
    s.created_at ASC;

-- Historial de un usuario
SELECT 
    s.titulo,
    s.estado,
    s.created_at,
    CASE 
        WHEN s.aprobador_id IS NOT NULL 
        THEN (SELECT nombre || ' ' || apellido FROM usuarios WHERE id = s.aprobador_id)
        ELSE 'Pendiente'
    END as aprobador
FROM solicitudes s
WHERE s.usuario_id = 1
ORDER BY s.created_at DESC;

-- Usuarios más activos
SELECT 
    u.nombre || ' ' || u.apellido as usuario,
    COUNT(s.id) as total_solicitudes,
    SUM(CASE WHEN s.estado = 'aprobada' THEN 1 ELSE 0 END) as aprobadas,
    SUM(CASE WHEN s.estado = 'rechazada' THEN 1 ELSE 0 END) as rechazadas
FROM usuarios u
LEFT JOIN solicitudes s ON u.id = s.usuario_id
GROUP BY u.id, u.nombre, u.apellido
HAVING COUNT(s.id) > 0
ORDER BY total_solicitudes DESC;
```

---

## 🔐 Autenticación y Seguridad

### JWT (JSON Web Tokens)

**Estructura de un Token:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDU0Nzg2NiwianRpIjoiOGVkOWYzNjktY2I1ZS00YjdjLThkYTgtNWQ4NmY1NzFkYzc3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NjA1NDc4NjYsImV4cCI6MTc2MDU1MTQ2Nn0.signature
         Header                                    Payload                                                                                                                                    Signature
```

**Decodificar un token (sin verificar firma):**
```bash
# Copiar token del login
TOKEN="eyJhbGc..."

# Decodificar payload (parte 2)
echo $TOKEN | cut -d'.' -f2 | base64 -d | python3 -m json.tool
```

**Resultado:**
```json
{
  "fresh": false,
  "iat": 1760547866,        # Issued at
  "jti": "8ed9f369-...",    # JWT ID único
  "type": "access",          # Tipo de token
  "sub": "1",                # Subject (ID del usuario)
  "nbf": 1760547866,        # Not before
  "exp": 1760551466         # Expiration (1 hora después)
}
```

### Hashing de Contraseñas

**Algoritmo:** Bcrypt con cost factor 12

```python
# Al crear usuario:
from werkzeug.security import generate_password_hash

password = "password123"
hash = generate_password_hash(password)
# Resultado: $2b$12$K8Z.../hash_aleatorio_muy_largo...

# Al verificar login:
from werkzeug.security import check_password_hash

is_valid = check_password_hash(hash, "password123")  # True
is_valid = check_password_hash(hash, "wrongpass")    # False
```

### Verificar Seguridad

```bash
# Ver si las contraseñas están hasheadas
docker compose exec db psql -U postgres solicitudes_db -c \
  "SELECT email, LEFT(password_hash, 20) || '...' as hash_preview FROM usuarios LIMIT 3;"

# Resultado esperado:
#       email              |     hash_preview
# -------------------------+----------------------
#  admin@solicitudes.com   | $2b$12$K8Z...
#  jefe@solicitudes.com    | $2b$12$abc...

# Ver configuración de JWT
docker compose exec api python -c "from config import Config; print(f'JWT expires in: {Config.JWT_ACCESS_TOKEN_EXPIRES}')"
```

---

## 🎯 Casos de Uso Prácticos

### Caso 1: Empleado crea una solicitud

```bash
# 1. Login como empleado
curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}' > /tmp/empleado_login.json

# 2. Extraer token
EMPLEADO_TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/empleado_login.json'))['access_token'])")

# 3. Crear solicitud
curl -s -X POST http://localhost:5000/api/solicitudes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EMPLEADO_TOKEN" \
  -d '{
    "titulo": "Solicitud de vacaciones",
    "descripcion": "Solicito 2 semanas de vacaciones del 1 al 15 de enero",
    "prioridad": "media",
    "tipo": "vacaciones",
    "fecha_requerida": "2025-01-01"
  }' | python3 -m json.tool

# 4. Ver mis solicitudes
curl -s -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer $EMPLEADO_TOKEN" | python3 -m json.tool
```

### Caso 2: Jefe aprueba la solicitud

```bash
# 1. Login como jefe
curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jefe@solicitudes.com","password":"jefe123"}' > /tmp/jefe_login.json

# 2. Extraer token
JEFE_TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/jefe_login.json'))['access_token'])")

# 3. Ver todas las solicitudes pendientes
curl -s -X GET "http://localhost:5000/api/solicitudes?estado=pendiente" \
  -H "Authorization: Bearer $JEFE_TOKEN" | python3 -m json.tool

# 4. Aprobar solicitud ID 5
curl -s -X PUT http://localhost:5000/api/solicitudes/5/estado \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JEFE_TOKEN" \
  -d '{
    "estado": "aprobada",
    "comentario": "Aprobado. Disfruta tus vacaciones."
  }' | python3 -m json.tool
```

### Caso 3: Admin gestiona usuarios

```bash
# 1. Login como admin
curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' > /tmp/admin_login.json

# 2. Extraer token
ADMIN_TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/admin_login.json'))['access_token'])")

# 3. Crear nuevo jefe
curl -s -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "nuevo.jefe@empresa.com",
    "password": "jefe123",
    "nombre": "Roberto",
    "apellido": "Silva",
    "rol": "jefe"
  }' | python3 -m json.tool

# 4. Cambiar rol de usuario existente (ID 4 a jefe)
curl -s -X PUT http://localhost:5000/api/usuarios/usuarios/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"rol": "jefe"}' | python3 -m json.tool

# 5. Desactivar usuario
curl -s -X PUT http://localhost:5000/api/usuarios/usuarios/5 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"activo": false}' | python3 -m json.tool

# 6. Ver estadísticas de usuarios
curl -s -X GET http://localhost:5000/api/usuarios/usuarios \
  -H "Authorization: Bearer $ADMIN_TOKEN" | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Total: {data['total']} usuarios\")"
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker compose logs -f

# Solo API
docker compose logs -f api

# Solo Base de Datos
docker compose logs -f db

# Múltiples servicios
docker compose logs -f api db

# Con marca de tiempo
docker compose logs -f --timestamps api

# Desde hace 10 minutos
docker compose logs --since 10m api
```

### Filtrar Logs

```bash
# Solo errores
docker compose logs api | grep -i error

# Solo warnings
docker compose logs api | grep -i warning

# Búsqueda específica
docker compose logs api | grep "POST /api/usuarios"

# Requests de un usuario
docker compose logs api | grep "usuario_id.*1"

# Últimas 100 líneas con errores
docker compose logs --tail=100 api | grep -i error
```

### Monitorear Recursos

```bash
# Ver uso de CPU y memoria
docker stats

# Solo servicios específicos
docker stats solicitudes-api solicitudes-db

# Una sola lectura (no continuo)
docker stats --no-stream

# Formato personalizado
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Health Checks

```bash
# Check de la API
curl http://localhost:5000/health

# Check de PostgreSQL
docker compose exec db pg_isready -U postgres

# Check de Redis
docker compose exec redis redis-cli ping

# Ver estado de todos los contenedores
docker compose ps
```

---

## 🔍 Troubleshooting

### Problema: API no responde

```bash
# 1. Verificar que el contenedor esté corriendo
docker ps | grep solicitudes-api

# 2. Ver logs de la API
docker compose logs --tail=50 api

# 3. Verificar puerto 5000
curl http://localhost:5000/health

# 4. Si no responde, reiniciar
docker compose restart api

# 5. Ver logs después del reinicio
docker compose logs -f api
```

### Problema: No puedo conectarme a la base de datos

```bash
# 1. Verificar que PostgreSQL esté corriendo
docker ps | grep db

# 2. Intentar conectarse
docker compose exec db psql -U postgres solicitudes_db

# 3. Ver logs de PostgreSQL
docker compose logs --tail=50 db

# 4. Verificar variables de entorno
docker compose exec api env | grep DATABASE

# 5. Reiniciar DB
docker compose restart db
```

### Problema: Token expirado

```bash
# Los tokens expiran después de 1 hora
# Solución: Hacer login nuevamente

curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])"
```

### Problema: Frontend no se actualiza

```bash
# 1. Limpiar caché de Vite
cd solicitudes-frontend
rm -rf node_modules/.vite dist .vite

# 2. Reiniciar servidor
pkill -f vite
npm run dev

# 3. Limpiar caché del navegador
# Ctrl + Shift + R (Windows/Linux)
# Cmd + Shift + R (Mac)
```

### Problema: "Email already registered"

```bash
# Ver si el email ya existe
docker compose exec db psql -U postgres solicitudes_db -c \
  "SELECT id, email, activo FROM usuarios WHERE email = 'test@test.com';"

# Si existe pero está inactivo, reactivarlo
docker compose exec db psql -U postgres solicitudes_db -c \
  "UPDATE usuarios SET activo = true WHERE email = 'test@test.com';"

# O usar otro email
```

### Problema: Permisos insuficientes

```bash
# Ver rol del usuario actual
curl -s -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN" | \
  python3 -c "import sys, json; print(f\"Rol: {json.load(sys.stdin)['usuario']['rol']}\")"

# Los permisos son:
# - empleado: Solo puede ver/crear sus solicitudes
# - jefe: Puede ver todas las solicitudes y aprobar/rechazar
# - administrador: Puede todo + gestionar usuarios
```

### Logs de Debugging

```bash
# Ver todas las queries SQL ejecutadas
docker compose logs api | grep "SELECT\|INSERT\|UPDATE\|DELETE"

# Ver requests HTTP
docker compose logs api | grep "GET\|POST\|PUT\|DELETE"

# Ver autenticaciones
docker compose logs api | grep "login\|token\|auth"

# Ver errores con contexto
docker compose logs api | grep -B 5 -A 5 "ERROR"
```

---

## 📖 Comandos Rápidos de Referencia

### Iniciar Sistema

```bash
cd solicitudes-api
docker compose up -d
cd ../solicitudes-frontend
npm run dev
```

### Detener Sistema

```bash
# Frontend: Ctrl+C en la terminal de npm

# Backend:
cd solicitudes-api
docker compose down
```

### Ver Estado

```bash
# Contenedores
docker ps

# Logs
docker compose logs -f api

# Base de datos
docker compose exec db psql -U postgres solicitudes_db
```

### Testing

```bash
# Health check
curl http://localhost:5000/health

# Login
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}'

# Script Python
cd solicitudes-api
python3 test_api.py
```

### Mantenimiento

```bash
# Backup de BD
docker compose exec db pg_dump -U postgres solicitudes_db > backup_$(date +%Y%m%d).sql

# Limpiar logs
docker compose logs --tail=0 -f > /dev/null

# Ver espacio usado
docker system df

# Limpiar recursos no usados
docker system prune -a
```

---

## 🎓 Conceptos Técnicos

| Concepto | Explicación |
|----------|-------------|
| **REST API** | Interfaz de programación que usa HTTP para CRUD (Create, Read, Update, Delete) |
| **JWT** | Token firmado que contiene información del usuario, usado para autenticación |
| **Bcrypt** | Algoritmo de hashing lento y seguro para contraseñas |
| **ORM** | Object-Relational Mapping - SQLAlchemy traduce objetos Python a SQL |
| **Blueprint** | Módulo de Flask para organizar rutas (similar a Router en Express) |
| **Middleware** | Función que se ejecuta antes/después de cada request |
| **CORS** | Cross-Origin Resource Sharing - permite requests desde dominios diferentes |
| **Docker Compose** | Herramienta para definir y correr aplicaciones multi-contenedor |
| **Migration** | Script versionado para cambiar la estructura de la base de datos |

---

## 📚 Recursos Adicionales

**Documentación oficial:**
- Flask: https://flask.palletsprojects.com
- React: https://react.dev
- PostgreSQL: https://www.postgresql.org/docs
- Docker: https://docs.docker.com

**Archivos del proyecto:**
- `COMO_FUNCIONA_LA_API.md` - Explicación técnica detallada
- `COMO_AGREGAR_USUARIOS.md` - Métodos para crear usuarios
- `COMO_USAR_LA_API.md` - Guía de uso de la API
- `test_api.py` - Script de prueba

---

**¿Preguntas?** Revisa los logs con `docker compose logs -f api` o conecta a la base de datos con `docker compose exec db psql -U postgres solicitudes_db`
