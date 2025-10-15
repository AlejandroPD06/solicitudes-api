# Guía del Panel de Administración

## 🎯 ¿Cómo Funciona el Sistema?

Este sistema de gestión de solicitudes internas está compuesto por **dos partes principales**:

### 1. **API REST** (`/api/*`)
- Endpoints para aplicaciones frontend (web/móvil)
- Protegida con autenticación JWT
- Los **empleados** consumen esta API desde una aplicación frontend
- Permite crear solicitudes, ver estado, etc.

### 2. **Panel de Administración** (`/admin`)
- Interfaz web para **jefes** y **administradores**
- Gestión completa del sistema
- Dashboard con estadísticas en tiempo real
- CRUD de usuarios, solicitudes y notificaciones

---

## 👥 Roles y Permisos

### 🟢 Empleado
- **Acceso**: Solo API REST (necesitan una app frontend)
- **Permisos**:
  - Crear solicitudes
  - Ver sus propias solicitudes
  - Actualizar información de perfil
- **NO pueden acceder** al panel de admin

### 🟡 Jefe
- **Acceso**: API REST + Panel de Admin
- **Permisos**:
  - Todo lo de empleado +
  - Aprobar/rechazar solicitudes
  - Ver todas las solicitudes
  - Gestionar solicitudes de su área

### 🔴 Administrador
- **Acceso**: API REST + Panel de Admin
- **Permisos**: Control total del sistema
  - Gestionar usuarios (crear, editar, desactivar)
  - Gestionar todas las solicitudes
  - Ver notificaciones
  - Acceso completo a estadísticas

---

## 🔐 Credenciales de Acceso

### Panel de Administración
**URL**: http://localhost:5000/admin

**Usuario Administrador:**
- Email: `admin@solicitudes.com`
- Contraseña: `admin123`

**Usuario Jefe:**
- Email: `jefe@solicitudes.com`
- Contraseña: `jefe123`

**Usuario Empleado** (NO tiene acceso al admin):
- Email: `empleado@solicitudes.com`
- Contraseña: `empleado123`

---

## 🎨 Características del Panel de Admin

### Dashboard Principal
- **Estadísticas en tiempo real**:
  - Total de usuarios registrados
  - Total de solicitudes
  - Solicitudes pendientes de aprobación
  - Estado de notificaciones por email

- **Acciones rápidas**:
  - Gestionar usuarios
  - Revisar solicitudes
  - Monitorear notificaciones

### Gestión de Usuarios
- **Crear/editar usuarios**
- **Asignar roles**: empleado, jefe, administrador
- **Activar/desactivar cuentas**
- **Buscar y filtrar** por email, nombre, rol
- **Edición inline** de estado y rol

### Gestión de Solicitudes
- **Ver todas las solicitudes** del sistema
- **Aprobar o rechazar** solicitudes pendientes
- **Cambiar estados**: pendiente → aprobada/rechazada → en proceso → completada
- **Gestionar prioridades**: baja, media, alta, urgente
- **Filtrar por**:
  - Tipo: compra, mantenimiento, soporte técnico, otro
  - Estado
  - Prioridad
  - Usuario solicitante
- **Búsqueda** por título y descripción

### Gestión de Notificaciones
- **Monitorear emails enviados**
- **Ver notificaciones pendientes**
- **Estado de envío**: enviado/pendiente
- **Intentos de reenvío** en caso de fallo
- **Solo lectura** (no se pueden crear manualmente)

---

## 🚀 Flujo de Trabajo Típico

### Para Empleados:
1. Acceden a una **aplicación frontend** (React, Vue, etc.)
2. La app consume la **API REST** (`/api/*`)
3. Inician sesión y obtienen un **token JWT**
4. Crean solicitudes de compra, mantenimiento, etc.
5. Reciben **notificaciones por email** sobre el estado

### Para Jefes/Administradores:
1. Acceden al **Panel de Admin**: http://localhost:5000/admin
2. Inician sesión con sus credenciales
3. Ven el **dashboard** con estadísticas
4. Revisan **solicitudes pendientes**
5. **Aprueban o rechazan** solicitudes
6. El sistema envía **emails automáticos** al solicitante

---

## 📧 Sistema de Notificaciones

### Emails Automáticos
El sistema envía emails automáticamente cuando:
- ✉️ Se crea una nueva solicitud
- ✅ Se aprueba una solicitud
- ❌ Se rechaza una solicitud
- 🔄 Se actualiza el estado de una solicitud
- ⏰ Recordatorios programados

### Configuración de Email
Actualmente configurado con:
- **SMTP**: Gmail
- **Email**: alejandropd908@gmail.com
- Los emails se procesan **asincrónicamente** con Celery

---

## 🛡️ Seguridad

### Panel de Administración
- ✅ Autenticación con sesión
- ✅ Control de acceso basado en roles
- ✅ Solo jefes y administradores pueden acceder
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Logout seguro que limpia la sesión

### API REST
- ✅ Autenticación con JWT tokens
- ✅ Tokens expiran después de 24 horas
- ✅ Validación de roles en cada endpoint
- ✅ CORS configurado para seguridad

---

## 🎨 Diseño Minimalista

El panel de admin ha sido rediseñado con:
- **Estilo moderno y limpio**
- **Colores suaves y profesionales**
- **Tipografía Inter** para mejor legibilidad
- **Tarjetas con animaciones hover**
- **Gradientes sutiles**
- **Iconos emoji** para mejor UX
- **Responsive** para móviles y tablets

---

## 🔄 ¿Qué Falta Implementar?

Para tener un sistema completo, necesitarías:

### 1. **Frontend para Empleados**
```
Opción A: React/Vue/Angular SPA
Opción B: Flutter/React Native app móvil
Opción C: Vistas adicionales en Flask
```

El frontend consumiría estos endpoints:

```
POST /api/usuarios/login
GET  /api/usuarios/perfil
POST /api/solicitudes
GET  /api/solicitudes
GET  /api/solicitudes/{id}
PATCH /api/solicitudes/{id}
GET  /api/notificaciones
```

### 2. **Mejoras Opcionales**
- [ ] Dashboard para empleados
- [ ] Carga de archivos adjuntos
- [ ] Chat/comentarios en solicitudes
- [ ] Notificaciones push/websockets
- [ ] Reportes y exportación a Excel/PDF
- [ ] Historial de cambios (audit log)
- [ ] Recordatorios programados
- [ ] Integración con Slack/Teams

---

## 📱 Ejemplo de Uso de la API

### Login (obtener JWT token)
```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empleado@solicitudes.com",
    "password": "empleado123"
  }'
```

### Crear una Solicitud
```bash
curl -X POST http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <tu-token-jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Compra de laptops",
    "descripcion": "Se necesitan 5 laptops para el equipo",
    "prioridad": "alta",
    "fecha_requerida": "2025-11-01"
  }'
```

### Ver mis Solicitudes
```bash
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <tu-token-jwt>"
```

---

## 🆘 Soporte

### Usuarios de Prueba
Todos los usuarios tienen sus contraseñas en formato: `{rol}123`

### Reiniciar Base de Datos
```bash
docker compose exec api python manage.py reset-db
docker compose exec api python manage.py seed-db
```

### Ver Logs
```bash
# API
docker compose logs api -f

# Celery Worker
docker compose logs celery-worker -f

# Base de datos
docker compose logs postgres -f
```

### Acceder a la Base de Datos
```bash
docker compose exec postgres psql -U postgres -d solicitudes_db
```

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│         FRONTEND (Por Implementar)       │
│    React/Vue/Angular/Flutter/etc.       │
└──────────────┬──────────────────────────┘
               │ HTTP + JWT
               ▼
┌─────────────────────────────────────────┐
│           API REST (Flask)              │
│  /api/usuarios  /api/solicitudes        │
│  /api/notificaciones                    │
└──────┬──────────────────────┬───────────┘
       │                      │
       ▼                      ▼
┌─────────────┐      ┌────────────────┐
│  PostgreSQL │      │  Redis + Celery│
│   Database  │      │  (Async Tasks) │
└─────────────┘      └────────────────┘
                             │
                             ▼
                     ┌───────────────┐
                     │  SMTP Server  │
                     │    (Gmail)    │
                     └───────────────┘

┌─────────────────────────────────────────┐
│     PANEL DE ADMIN (Flask-Admin)        │
│         /admin (Solo Jefes/Admin)       │
└─────────────────────────────────────────┘
```

---

¡El sistema está completamente funcional y listo para usar! 🎉
