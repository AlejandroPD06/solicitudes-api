# 🎯 Microservicio API - Gestión de Solicitudes Internas

Sistema de gestión de solicitudes internas (compras, mantenimiento, soporte técnico) implementado como **microservicio API REST** con Flask.

---

## ✅ Cumplimiento de Requisitos - 100%

**Requisitos originales:**
> API en Flask, dockerizado, para digitalizar solicitudes internas con endpoints `/solicitudes`, `/usuarios`, `/notificaciones`, usando Flask-SQLAlchemy, PostgreSQL, Celery y correos automáticos.

| Requisito | Estado |
|-----------|--------|
| API Flask | ✅ Implementada |
| Docker | ✅ 5 servicios |
| Flask-SQLAlchemy | ✅ 3 modelos |
| PostgreSQL | ✅ Base de datos |
| Celery | ✅ Emails asíncronos |
| /solicitudes | ✅ CRUD + estados |
| /usuarios | ✅ Auth + roles |
| /notificaciones | ✅ Emails automáticos |

---

## 🚀 Inicio Rápido

```bash
# 1. Levantar servicios
docker compose up -d

# 2. Inicializar base de datos
docker compose exec api python manage.py reset-db
docker compose exec api python manage.py seed-db

# 3. Probar API
curl http://localhost:5000/health
```

**Usuarios de prueba:**
- `empleado@solicitudes.com` / `empleado123`
- `jefe@solicitudes.com` / `jefe123`
- `admin@solicitudes.com` / `admin123`

---

## 📡 API REST - Endpoints

### Base URL: `http://localhost:5000`

### Autenticación
```bash
POST /api/usuarios/login
Content-Type: application/json

{
  "email": "empleado@solicitudes.com",
  "password": "empleado123"
}

# Respuesta incluye access_token para usar en:
# Authorization: Bearer <access_token>
```

### Solicitudes
```bash
# Crear
POST /api/solicitudes
{
  "tipo": "compra",
  "titulo": "Laptops",
  "descripcion": "5 laptops Dell",
  "prioridad": "alta"
}

# Listar
GET /api/solicitudes
GET /api/solicitudes?estado=pendiente

# Aprobar/Rechazar (jefe/admin)
PATCH /api/solicitudes/{id}/estado
{
  "estado": "aprobada",
  "comentarios": "Aprobado"
}
```

**Estados:** `pendiente`, `aprobada`, `rechazada`, `en_proceso`, `completada`
**Tipos:** `compra`, `mantenimiento`, `soporte_tecnico`, `otro`
**Prioridades:** `baja`, `media`, `alta`, `urgente`

### Usuarios
```bash
# Registro
POST /api/usuarios/registro

# Perfil
GET /api/usuarios/perfil
PUT /api/usuarios/perfil

# Gestión (admin)
GET /api/usuarios
PUT /api/usuarios/{id}
```

**Roles:** `empleado`, `jefe`, `administrador`

### Notificaciones
```bash
GET /api/notificaciones
GET /api/notificaciones/{id}
```

**Emails automáticos:**
- Al crear solicitud
- Al aprobar/rechazar
- Al actualizar estado

---

## 🏗️ Arquitectura

```
Frontend Separado
(React/Vue/Angular)
        ↓ HTTP REST + JWT
┌───────────────────┐
│ Microservicio API │ ← Este proyecto
│ /api/solicitudes  │
│ /api/usuarios     │
│ /api/notificaciones│
└─────────┬─────────┘
          ↓
    PostgreSQL
```

---

## 🛠️ Stack Tecnológico

- **Flask** + **Flask-SQLAlchemy** + **PostgreSQL**
- **Flask-JWT-Extended** - Autenticación
- **Celery** + **Redis** - Emails asíncronos
- **Docker** + **Docker Compose**
- **Gunicorn** - WSGI server

---

## 📁 Estructura

```
solicitudes-api/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # API blueprints
│   ├── services/         # Business logic
│   └── tasks/            # Celery tasks
├── docker-compose.yml    # Servicios
├── Dockerfile
├── requirements.txt
└── .env                  # Config
```

---

## 🔐 Control de Acceso

| Acción | Empleado | Jefe | Admin |
|--------|----------|------|-------|
| Crear solicitud | ✅ | ✅ | ✅ |
| Ver mis solicitudes | ✅ | ✅ | ✅ |
| Ver todas | ❌ | ✅ | ✅ |
| Aprobar/Rechazar | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |

---

## 🔧 Comandos Útiles

```bash
# Ver servicios
docker compose ps

# Logs
docker compose logs -f api
docker compose logs -f celery-worker

# Base de datos
docker compose exec postgres psql -U postgres -d solicitudes_db

# Reiniciar
docker compose restart api
```

---

## 📧 Configuración Email

```env
# .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password  # Gmail App Password
```

---

## 📚 Documentación

- `VERIFICACION_REQUISITOS.md` - Verificación detallada
- `MICROSERVICIO_API.md` - Documentación completa

---

## ✅ Resumen

**El microservicio API está completo con:**

1. ✅ API REST en Flask
2. ✅ Dockerizado (5 servicios)
3. ✅ CRUD de solicitudes con estados
4. ✅ Autenticación JWT con roles
5. ✅ Notificaciones por email automáticas
6. ✅ Arquitectura de microservicio

**Listo para producción.** 🎉

El frontend debe ser una aplicación separada que consuma esta API.
