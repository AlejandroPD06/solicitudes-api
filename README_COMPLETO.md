# 📋 Sistema de Gestión de Solicitudes Internas

Sistema completo de gestión de solicitudes internas con panel de administración y portal para empleados.

---

## 🚀 Sistema Completo Implementado

### ✅ Lo que Acabamos de Crear

1. **Panel de Administración** (`/admin`) - Para jefes y administradores
2. **Portal de Empleados** (`/app`) - Para todos los usuarios
3. **API REST** (`/api`) - Backend con JWT
4. **Sistema de Notificaciones por Email** (Celery + Redis)
5. **Base de Datos PostgreSQL**

---

## 🌐 Acceso al Sistema

### 🏠 **Página Principal**
```
http://localhost:5000
```
Redirige automáticamente al portal de empleados

### 👥 **Portal de Empleados** (Todos los usuarios)
```
URL: http://localhost:5000/app
```

**Credenciales de Prueba:**

**Empleado:**
- Email: `empleado@solicitudes.com`
- Contraseña: `empleado123`

**Jefe:**
- Email: `jefe@solicitudes.com`
- Contraseña: `jefe123`

**Administrador:**
- Email: `admin@solicitudes.com`
- Contraseña: `admin123`

**Funcionalidades del Portal:**
- ✅ Dashboard con estadísticas personales
- ✅ Ver todas mis solicitudes
- ✅ Crear nuevas solicitudes
- ✅ Ver detalles de cada solicitud
- ✅ Filtrar solicitudes por estado y tipo
- ✅ Editar mi perfil
- ✅ Cambiar contraseña

---

### 🎯 **Panel de Administración** (Solo Jefes y Administradores)
```
URL: http://localhost:5000/admin
```

**Credenciales:**

**Administrador:**
- Email: `admin@solicitudes.com`
- Contraseña: `admin123`

**Jefe:**
- Email: `jefe@solicitudes.com`
- Contraseña: `jefe123`

**Funcionalidades del Admin:**
- ✅ Dashboard con estadísticas globales
- ✅ Gestión de usuarios (CRUD)
- ✅ Gestión de solicitudes (aprobar/rechazar)
- ✅ Monitoreo de notificaciones
- ✅ Cambio de estados y prioridades
- ✅ Búsqueda y filtros avanzados

**⚠️ Nota:** Los empleados NO pueden acceder al panel de admin.

---

## 📱 Flujo de Trabajo Completo

### Para Empleados:

1. **Login** en http://localhost:5000
2. Ver su **Dashboard** con estadísticas
3. **Crear Solicitud**:
   - Tipo: compra, mantenimiento, soporte técnico, otro
   - Título y descripción
   - Prioridad: baja, media, alta, urgente
   - Fecha requerida (opcional)
4. Ver el estado en **Mis Solicitudes**
5. Recibir **email** cuando sea aprobada/rechazada

### Para Jefes/Administradores:

1. **Portal de Empleados** (mismo acceso que empleados)
   - Pueden crear solicitudes propias
   - Ver su dashboard personal

2. **Panel de Admin** en `/admin`
   - Ver todas las solicitudes pendientes
   - **Aprobar o rechazar** solicitudes
   - Cambiar **estados**: pendiente → aprobada/rechazada → en_proceso → completada
   - Agregar **comentarios**
   - Gestionar **usuarios**
   - Ver **notificaciones** enviadas

---

## 🎨 Características del Diseño

### Portal de Empleados

**Diseño Minimalista Moderno:**
- 🎨 Gradientes suaves (púrpura/azul)
- 📱 Responsive (móvil, tablet, desktop)
- ⚡ Animaciones suaves
- 🔤 Tipografía Inter profesional
- 🎯 UX intuitiva con emojis
- 🌈 Badges de colores por estado
- ⚙️ Filtros en tiempo real

**Páginas:**
1. **Login** - Diseño centrado con gradiente
2. **Dashboard** - Tarjetas de estadísticas
3. **Mis Solicitudes** - Lista con filtros
4. **Nueva Solicitud** - Formulario completo
5. **Detalle** - Vista completa con timeline
6. **Perfil** - Editar información personal

### Panel de Admin

**Diseño Profesional:**
- 📊 Dashboard con métricas en tiempo real
- 🎨 Mismo esquema de colores
- 📋 Tablas con edición inline
- 🔍 Búsqueda y filtros avanzados
- 👤 Avatar del usuario logueado
- 🚪 Botón de logout

---

## 🔐 Sistema de Autenticación

### Portal de Empleados
- **Sesiones** con Flask sessions
- Datos guardados en cookies seguras
- Logout que limpia la sesión
- Middleware para proteger rutas

### Panel de Admin
- **Sesiones** separadas del portal
- Control de acceso basado en roles
- Solo jefes y administradores

### API REST
- **JWT tokens** (24 horas de validez)
- Headers: `Authorization: Bearer <token>`
- Roles verificados en cada endpoint

---

## 📧 Sistema de Notificaciones

### Emails Automáticos

El sistema envía emails cuando:
- ✉️ Se crea una solicitud
- ✅ Se aprueba una solicitud
- ❌ Se rechaza una solicitud
- 🔄 Se actualiza el estado

### Configuración SMTP
```
Servidor: Gmail (smtp.gmail.com:587)
Email: alejandropd908@gmail.com
Método: TLS
```

### Procesamiento Asíncrono
- **Celery Worker** procesa emails en background
- **Redis** como message broker
- Reintentos automáticos en caso de fallo
- Registro de intentos en la base de datos

---

## 🗄️ Base de Datos

### Modelos

**Usuario:**
- id, email, password_hash
- nombre, apellido, rol
- activo, created_at, updated_at

**Solicitud:**
- id, tipo, titulo, descripcion
- estado, prioridad
- fecha_requerida, fecha_aprobacion
- usuario_id, aprobador_id
- comentarios
- created_at, updated_at

**Notificacion:**
- id, tipo, destinatario_email
- asunto, mensaje
- enviado, fecha_envio
- intentos, error_mensaje
- solicitud_id, created_at

### Datos de Prueba

```sql
-- 3 usuarios
admin@solicitudes.com (administrador)
jefe@solicitudes.com (jefe)
empleado@solicitudes.com (empleado)

-- 3 solicitudes de ejemplo
- Compra de laptops (pendiente)
- Mantenimiento de servidores (aprobada)
- Soporte para software (pendiente)
```

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos
- **Flask-Admin** - Panel de admin
- **Flask-JWT-Extended** - Autenticación JWT
- **Celery** - Tareas asíncronas
- **Redis** - Message broker
- **Flask-Mail** - Envío de emails
- **Gunicorn** - WSGI server

### Frontend
- **HTML5 + CSS3** - Diseño minimalista
- **Jinja2** - Templates
- **JavaScript vanilla** - Interactividad
- **Google Fonts (Inter)** - Tipografía

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **Migrations** - Alembic

---

## 📂 Estructura del Proyecto

```
solicitudes-api/
├── app/
│   ├── __init__.py              # Factory pattern
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── solicitud.py
│   │   └── notificacion.py
│   ├── routes/                  # Blueprints
│   │   ├── auth.py             # API REST - Autenticación
│   │   ├── solicitudes.py      # API REST - Solicitudes
│   │   ├── notificaciones.py   # API REST - Notificaciones
│   │   └── frontend.py         # 🆕 Portal Empleados
│   ├── admin/                   # Flask-Admin
│   │   └── views.py
│   ├── tasks/                   # Celery
│   │   └── email_tasks.py
│   └── templates/
│       ├── admin/               # Templates Admin
│       │   ├── index.html
│       │   ├── login.html
│       │   └── master.html
│       └── frontend/            # 🆕 Templates Empleados
│           ├── base.html
│           ├── login.html
│           ├── dashboard.html
│           ├── solicitudes.html
│           ├── nueva_solicitud.html
│           ├── detalle_solicitud.html
│           └── perfil.html
├── config.py                    # Configuración
├── manage.py                    # CLI commands
├── wsgi.py                      # Entry point
├── docker-compose.yml           # Servicios Docker
├── Dockerfile                   # Imagen de la API
├── requirements.txt             # Dependencias
├── .env                         # Variables de entorno
├── GUIA_ADMIN.md               # Guía del admin
└── README_COMPLETO.md          # 🆕 Este archivo
```

---

## 🔧 Comandos Útiles

### Gestión de Docker

```bash
# Iniciar todos los servicios
docker compose up -d

# Ver logs
docker compose logs -f api
docker compose logs -f celery-worker

# Reiniciar servicios
docker compose restart api
docker compose restart celery-worker

# Detener todo
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

### Gestión de Base de Datos

```bash
# Resetear base de datos
docker compose exec api python manage.py reset-db

# Crear datos de prueba
docker compose exec api python manage.py seed-db

# Acceder a PostgreSQL
docker compose exec postgres psql -U postgres -d solicitudes_db

# Ver usuarios
docker compose exec postgres psql -U postgres -d solicitudes_db -c "SELECT * FROM usuarios;"

# Ver solicitudes
docker compose exec postgres psql -U postgres -d solicitudes_db -c "SELECT * FROM solicitudes;"
```

### Limpiar Cache

```bash
# Limpiar cache de Python
docker compose exec api find /app -type d -name __pycache__ -exec rm -rf {} +

# Reiniciar después de limpiar
docker compose restart api
```

---

## 🧪 Probar el Sistema

### 1. Acceso al Portal de Empleados

```bash
# Abrir navegador en:
http://localhost:5000

# Login con:
empleado@solicitudes.com / empleado123
```

**Flujo de prueba:**
1. ✅ Login exitoso → Dashboard
2. ✅ Click en "Nueva Solicitud"
3. ✅ Completar formulario
4. ✅ Ver solicitud creada
5. ✅ Click en la solicitud → Ver detalles
6. ✅ Ir a "Mi Perfil" → Editar datos

### 2. Acceso al Panel de Admin

```bash
# Abrir navegador en:
http://localhost:5000/admin

# Login con:
admin@solicitudes.com / admin123
```

**Flujo de prueba:**
1. ✅ Login como admin → Dashboard
2. ✅ Ver estadísticas
3. ✅ Click en "Solicitudes"
4. ✅ Aprobar/rechazar solicitudes
5. ✅ Agregar comentarios
6. ✅ Ver notificaciones enviadas

### 3. Probar API REST

```bash
# 1. Login y obtener JWT token
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}'

# 2. Usar el token (reemplazar <TOKEN>)
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <TOKEN>"

# 3. Crear solicitud
curl -X POST http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Prueba desde API",
    "descripcion": "Solicitud de prueba",
    "prioridad": "media"
  }'
```

---

## 🎯 Casos de Uso

### Caso 1: Empleado Crea Solicitud de Compra

1. María (empleado) accede a http://localhost:5000
2. Login con `empleado@solicitudes.com`
3. Ve su dashboard (0 solicitudes)
4. Click en "Nueva Solicitud"
5. Completa:
   - Tipo: Compra
   - Título: "5 Laptops Dell XPS 15"
   - Descripción: "Para el equipo de desarrollo..."
   - Prioridad: Alta
   - Fecha requerida: 01/11/2025
6. Click "Crear Solicitud"
7. ✅ Solicitud creada
8. 📧 Email enviado automáticamente

### Caso 2: Jefe Aprueba Solicitud

1. Juan (jefe) accede a http://localhost:5000/admin
2. Login con `jefe@solicitudes.com`
3. Ve dashboard (1 solicitud pendiente)
4. Click en "Solicitudes"
5. Ve la solicitud de María
6. Click para editar
7. Cambia estado a "Aprobada"
8. Agrega comentario: "Aprobado, proceder con la compra"
9. Guarda cambios
10. ✅ Estado actualizado
11. 📧 Email enviado a María automáticamente

### Caso 3: Administrador Gestiona Usuarios

1. Admin accede a http://localhost:5000/admin
2. Login con `admin@solicitudes.com`
3. Click en "Usuarios"
4. Click "Create"
5. Completa:
   - Email: nuevo@empresa.com
   - Nombre: Carlos
   - Apellido: Rodríguez
   - Rol: Jefe
   - Activo: Sí
6. Guarda
7. ✅ Usuario creado
8. Carlos puede ahora acceder al sistema

---

## 🔄 Estados de Solicitud

```
pendiente → Primera vez creada
    ↓
aprobada / rechazada → Decisión del jefe/admin
    ↓
en_proceso → Se está trabajando en ella
    ↓
completada → Finalizada
```

**Estados:**
- 🟡 **Pendiente**: Esperando aprobación
- ✅ **Aprobada**: Autorizada para proceder
- ❌ **Rechazada**: No autorizada
- 🔄 **En Proceso**: Se está trabajando
- ✓ **Completada**: Finalizada

**Prioridades:**
- 🟢 **Baja**: No urgente
- 🟡 **Media**: Prioridad normal
- 🟠 **Alta**: Importante
- 🔴 **Urgente**: Requiere atención inmediata

**Tipos:**
- 💰 **Compra**: Adquisición de productos/servicios
- 🔧 **Mantenimiento**: Reparación/mantenimiento
- 💻 **Soporte Técnico**: Asistencia técnica
- 📝 **Otro**: Otros tipos de solicitudes

---

## 🚨 Solución de Problemas

### Error: "Internal Server Error" en Admin

```bash
# Limpiar cache y reiniciar
docker compose exec api find /app -type d -name __pycache__ -exec rm -rf {} +
docker compose restart api
```

### Error: No se envían emails

```bash
# Verificar Celery Worker
docker compose logs celery-worker

# Verificar configuración SMTP en .env
# Reiniciar worker
docker compose restart celery-worker
```

### Error: "Database not found"

```bash
# Recrear base de datos
docker compose exec api python manage.py reset-db
docker compose exec api python manage.py seed-db
```

### Problema: Cambios no se reflejan

```bash
# Limpiar cache
docker compose exec api find /app -type d -name __pycache__ -exec rm -rf {} +

# Reiniciar servicios
docker compose restart api celery-worker

# Hard restart (eliminar contenedores)
docker compose down
docker compose up -d
```

---

## 📚 Endpoints de la API REST

### Autenticación
```
POST /api/usuarios/registro     - Crear usuario
POST /api/usuarios/login        - Login (obtener JWT)
GET  /api/usuarios/perfil       - Ver mi perfil
PUT  /api/usuarios/perfil       - Actualizar perfil
POST /api/usuarios/cambiar-password - Cambiar contraseña
GET  /api/usuarios              - Listar usuarios (admin)
GET  /api/usuarios/{id}         - Ver usuario (admin)
PUT  /api/usuarios/{id}         - Actualizar usuario (admin)
DELETE /api/usuarios/{id}       - Eliminar usuario (admin)
```

### Solicitudes
```
POST   /api/solicitudes         - Crear solicitud
GET    /api/solicitudes         - Listar solicitudes
GET    /api/solicitudes/{id}    - Ver solicitud
PUT    /api/solicitudes/{id}    - Actualizar solicitud
DELETE /api/solicitudes/{id}    - Eliminar solicitud
PATCH  /api/solicitudes/{id}/estado - Cambiar estado
GET    /api/solicitudes/estadisticas - Estadísticas
```

### Notificaciones
```
GET /api/notificaciones         - Listar notificaciones
GET /api/notificaciones/{id}    - Ver notificación
```

---

## 🎉 ¡Sistema Completo Funcionando!

### ✅ Lo que Tienes Ahora

1. **Portal Web para Empleados** (/app)
   - Login/Logout
   - Dashboard personalizado
   - Crear solicitudes
   - Ver y filtrar solicitudes
   - Ver detalles
   - Editar perfil

2. **Panel de Administración** (/admin)
   - Login/Logout con autenticación
   - Dashboard con estadísticas
   - Gestión de usuarios
   - Aprobación de solicitudes
   - Monitoreo de notificaciones

3. **API REST Completa** (/api)
   - Autenticación JWT
   - CRUD de usuarios
   - CRUD de solicitudes
   - Control de acceso por roles

4. **Sistema de Notificaciones**
   - Emails automáticos
   - Procesamiento asíncrono
   - Registro de intentos

5. **Base de Datos**
   - PostgreSQL con modelos completos
   - Relaciones entre tablas
   - Datos de prueba

---

## 💡 Próximos Pasos (Opcional)

### Mejoras Sugeridas

- [ ] **Adjuntar archivos** a solicitudes
- [ ] **Comentarios** en las solicitudes
- [ ] **Notificaciones push** (WebSockets)
- [ ] **Reportes** en PDF/Excel
- [ ] **Búsqueda avanzada** con Elasticsearch
- [ ] **Dashboard** con gráficas (Chart.js)
- [ ] **App móvil** (React Native/Flutter)
- [ ] **Integración Slack/Teams**
- [ ] **Recordatorios automáticos**
- [ ] **Historial de cambios** (audit log)

---

## 📞 Soporte

### Archivos de Documentación
- `README_COMPLETO.md` - Esta guía completa
- `GUIA_ADMIN.md` - Guía del panel de administración

### Verificar que todo funciona

```bash
# 1. Ver estado de servicios
docker compose ps

# 2. Ver logs
docker compose logs api --tail=50

# 3. Probar health check
curl http://localhost:5000/health

# 4. Probar login empleado
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}'
```

---

¡Todo el sistema está completo y funcionando! 🎊

**URLs principales:**
- Portal Empleados: http://localhost:5000
- Panel Admin: http://localhost:5000/admin
- API REST: http://localhost:5000/api
- Health Check: http://localhost:5000/health
