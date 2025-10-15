# API de Gestión de Solicitudes Internas

Microservicio RESTful para la gestión de solicitudes internas (compras, mantenimiento, soporte técnico) construido con Flask, PostgreSQL y arquitectura de microservicios.

## Características

- **API REST completa** con autenticación JWT
- **Gestión de usuarios** con roles (empleado, jefe, administrador)
- **CRUD de solicitudes** con estados y prioridades
- **Notificaciones por email** asíncronas con Celery
- **Panel de administración** con Flask-Admin
- **Dockerizado** para fácil despliegue
- **Base de datos PostgreSQL**
- **Redis** para tareas asíncronas

## Arquitectura de Microservicios

Este proyecto sigue una arquitectura de microservicios donde:
- La API REST es independiente (no incluye frontend)
- La base de datos es gestionada exclusivamente por la API
- La comunicación se realiza mediante HTTP/REST
- El frontend debe ser un proyecto separado que consuma esta API

## Tecnologías

- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para base de datos
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-Admin** - Panel de administración
- **PostgreSQL** - Base de datos relacional
- **Celery** - Procesamiento asíncrono
- **Redis** - Message broker
- **Docker & Docker Compose** - Containerización

## Estructura del Proyecto

```
solicitudes-api/
├── app/
│   ├── __init__.py           # Factory pattern de Flask
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── solicitud.py
│   │   └── notificacion.py
│   ├── routes/               # Blueprints REST
│   │   ├── auth.py
│   │   ├── solicitudes.py
│   │   └── notificaciones.py
│   ├── services/             # Lógica de negocio
│   │   └── auth_service.py
│   ├── tasks/                # Tareas Celery
│   │   └── email_tasks.py
│   └── admin/                # Flask-Admin
│       └── views.py
├── config.py                 # Configuraciones
├── wsgi.py                   # Punto de entrada
├── manage.py                 # Comandos de gestión
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Servicios Docker
└── .env.example             # Variables de entorno

```

## Requisitos Previos

- Docker
- Docker Compose

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
cd solicitudes-api
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:

```env
# Cambiar las claves secretas
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-jwt-secret-key-aqui

# Configurar credenciales de email
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
```

**Nota sobre Gmail:**
Para usar Gmail, necesitas crear una "App Password":
1. Ve a https://myaccount.google.com/security
2. Activa "2-Step Verification"
3. Genera una "App Password" para la aplicación
4. Usa esa contraseña en `MAIL_PASSWORD`

### 3. Construir y levantar los servicios

```bash
docker-compose build
docker-compose up -d
```

Esto levantará:
- `postgres` - Base de datos PostgreSQL (puerto 5432)
- `redis` - Message broker (puerto 6379)
- `api` - API Flask (puerto 5000)
- `celery-worker` - Worker para emails
- `celery-beat` - Scheduler para tareas programadas

### 4. Inicializar la base de datos

```bash
# Crear las tablas
docker-compose exec api python manage.py init-db

# Poblar con datos de prueba (opcional)
docker-compose exec api python manage.py seed-db
```

### 5. Verificar que todo funciona

```bash
curl http://localhost:5000/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "solicitudes-api"
}
```

## Uso de la API

### Usuarios de Prueba (si ejecutaste seed-db)

| Email | Password | Rol |
|-------|----------|-----|
| admin@solicitudes.com | admin123 | administrador |
| jefe@solicitudes.com | jefe123 | jefe |
| empleado@solicitudes.com | empleado123 | empleado |

### Endpoints Principales

#### Autenticación

**Registro de usuario**
```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "password123",
    "nombre": "Juan",
    "apellido": "Pérez"
  }'
```

**Login**
```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empleado@solicitudes.com",
    "password": "empleado123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "usuario": {...}
}
```

**Obtener perfil**
```bash
curl -X GET http://localhost:5000/api/usuarios/perfil \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

#### Solicitudes

**Crear solicitud**
```bash
curl -X POST http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Compra de laptops",
    "descripcion": "Se requieren 5 laptops para el equipo",
    "prioridad": "alta"
  }'
```

**Listar solicitudes**
```bash
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

**Obtener solicitud específica**
```bash
curl -X GET http://localhost:5000/api/solicitudes/1 \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

**Actualizar solicitud**
```bash
curl -X PUT http://localhost:5000/api/solicitudes/1 \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Nuevo título",
    "prioridad": "urgente"
  }'
```

**Cambiar estado de solicitud** (solo jefe/admin)
```bash
curl -X PATCH http://localhost:5000/api/solicitudes/1/estado \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "aprobada",
    "comentarios": "Aprobado por presupuesto"
  }'
```

**Obtener estadísticas** (solo jefe/admin)
```bash
curl -X GET http://localhost:5000/api/solicitudes/estadisticas \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

#### Notificaciones

**Listar notificaciones**
```bash
curl -X GET http://localhost:5000/api/notificaciones \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

**Obtener estadísticas de notificaciones** (solo jefe/admin)
```bash
curl -X GET http://localhost:5000/api/notificaciones/estadisticas \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

### Panel de Administración

Accede al panel de Flask-Admin en: http://localhost:5000/admin

## Comandos de Gestión

```bash
# Inicializar base de datos
docker-compose exec api python manage.py init-db

# Resetear base de datos
docker-compose exec api python manage.py reset-db

# Poblar con datos de prueba
docker-compose exec api python manage.py seed-db

# Eliminar base de datos
docker-compose exec api python manage.py drop-db

# Acceder a la shell de Flask
docker-compose exec api flask shell

# Ver logs
docker-compose logs -f api
docker-compose logs -f celery-worker
```

## Modelos de Datos

### Usuario
```python
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "rol": "empleado",  # empleado, jefe, administrador
  "activo": true,
  "created_at": "2025-01-15T10:30:00"
}
```

### Solicitud
```python
{
  "id": 1,
  "tipo": "compra",  # compra, mantenimiento, soporte_tecnico, otro
  "titulo": "Compra de laptops",
  "descripcion": "Se requieren 5 laptops",
  "estado": "pendiente",  # pendiente, aprobada, rechazada, en_proceso, completada
  "prioridad": "alta",  # baja, media, alta, urgente
  "comentarios": null,
  "fecha_requerida": "2025-02-01",
  "usuario_id": 1,
  "aprobador_id": null,
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00",
  "fecha_aprobacion": null
}
```

### Notificación
```python
{
  "id": 1,
  "tipo": "solicitud_creada",
  "destinatario_email": "jefe@solicitudes.com",
  "asunto": "Nueva solicitud: Compra de laptops",
  "mensaje": "Se ha creado una nueva solicitud...",
  "enviado": true,
  "fecha_envio": "2025-01-15T10:31:00",
  "intentos": 1,
  "solicitud_id": 1
}
```

## Roles y Permisos

| Acción | Empleado | Jefe | Administrador |
|--------|----------|------|---------------|
| Crear solicitud | ✅ | ✅ | ✅ |
| Ver propias solicitudes | ✅ | ✅ | ✅ |
| Ver todas las solicitudes | ❌ | ✅ | ✅ |
| Actualizar propia solicitud | ✅ (solo pendiente) | ✅ | ✅ |
| Cambiar estado de solicitud | ❌ | ✅ | ✅ |
| Ver usuarios | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Acceder a estadísticas | ❌ | ✅ | ✅ |
| Panel de administración | ❌ | ❌ | ✅ |

## Desarrollo

### Ejecutar sin Docker

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar PostgreSQL y Redis localmente

4. Ejecutar la aplicación:
```bash
python wsgi.py
```

5. Ejecutar Celery worker:
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

### Testing

```bash
docker-compose exec api pytest
```

## Solución de Problemas

### Error de conexión a PostgreSQL
```bash
# Verificar que el contenedor está corriendo
docker-compose ps

# Ver logs
docker-compose logs postgres
```

### Emails no se envían
```bash
# Verificar logs del worker de Celery
docker-compose logs celery-worker

# Verificar configuración de email en .env
```

### Resetear completamente el proyecto
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec api python manage.py init-db
docker-compose exec api python manage.py seed-db
```

## Producción

Para desplegar en producción:

1. Cambiar las variables de entorno en `.env`:
   - `FLASK_ENV=production`
   - Cambiar `SECRET_KEY` y `JWT_SECRET_KEY`
   - Configurar base de datos de producción

2. Usar un servidor WSGI de producción (ya configurado con Gunicorn)

3. Configurar HTTPS con un proxy reverso (nginx, traefik)

4. Configurar backups de la base de datos

5. Monitorear logs y métricas

## Licencia

MIT

## Contacto

Para soporte o consultas sobre este proyecto, contacta al equipo de desarrollo.
