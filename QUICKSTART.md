# Inicio Rápido - API de Solicitudes Internas

## Configuración en 3 minutos ⚡

### 1. Configurar variables de entorno

```bash
cp .env.example .env
```

**Edita el archivo `.env` y cambia:**
- `SECRET_KEY` y `JWT_SECRET_KEY` (genera claves aleatorias)
- `MAIL_USERNAME` y `MAIL_PASSWORD` con tus credenciales de email

### 2. Levantar el proyecto

```bash
# Usando Make (recomendado)
make setup

# O usando Docker Compose directamente
docker-compose build
docker-compose up -d
docker-compose exec api python manage.py init-db
docker-compose exec api python manage.py seed-db
```

### 3. Verificar que funciona

```bash
curl http://localhost:5000/health
```

## URLs Importantes

- **API**: http://localhost:5000
- **Panel Admin**: http://localhost:5000/admin
- **Swagger/Docs**: http://localhost:5000/api/doc (si está habilitado)

## Usuarios de Prueba

| Email | Password | Rol |
|-------|----------|-----|
| admin@solicitudes.com | admin123 | administrador |
| jefe@solicitudes.com | jefe123 | jefe |
| empleado@solicitudes.com | empleado123 | empleado |

## Ejemplo de Uso

### 1. Login

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empleado@solicitudes.com",
    "password": "empleado123"
  }'
```

**Guarda el `access_token` de la respuesta**

### 2. Crear una solicitud

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

### 3. Listar solicitudes

```bash
curl -X GET http://localhost:5000/api/solicitudes \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

## Comandos Útiles

```bash
# Ver logs
make logs

# Reiniciar servicios
make restart

# Acceder a la shell de Flask
make shell

# Ejecutar pruebas
make test

# Limpiar todo
make clean
```

## Estructura de Endpoints

### Autenticación (`/api/usuarios`)
- `POST /registro` - Registrar usuario
- `POST /login` - Iniciar sesión
- `GET /perfil` - Obtener perfil
- `PUT /perfil` - Actualizar perfil
- `POST /cambiar-password` - Cambiar contraseña

### Solicitudes (`/api/solicitudes`)
- `POST /` - Crear solicitud
- `GET /` - Listar solicitudes
- `GET /{id}` - Obtener solicitud
- `PUT /{id}` - Actualizar solicitud
- `DELETE /{id}` - Eliminar solicitud
- `PATCH /{id}/estado` - Cambiar estado (jefe/admin)
- `GET /estadisticas` - Estadísticas (jefe/admin)

### Notificaciones (`/api/notificaciones`)
- `GET /` - Listar notificaciones
- `GET /{id}` - Obtener notificación
- `POST /{id}/reenviar` - Reenviar (admin)
- `GET /pendientes` - Listar pendientes (admin)
- `GET /estadisticas` - Estadísticas (jefe/admin)

## Tipos de Datos

### Tipos de Solicitud
- `compra` - Solicitudes de compra
- `mantenimiento` - Solicitudes de mantenimiento
- `soporte_tecnico` - Solicitudes de soporte técnico
- `otro` - Otras solicitudes

### Estados
- `pendiente` - Pendiente de revisión
- `aprobada` - Aprobada por jefe/admin
- `rechazada` - Rechazada
- `en_proceso` - En proceso
- `completada` - Completada

### Prioridades
- `baja` - Prioridad baja
- `media` - Prioridad media
- `alta` - Prioridad alta
- `urgente` - Urgente

### Roles
- `empleado` - Usuario estándar
- `jefe` - Puede aprobar/rechazar solicitudes
- `administrador` - Acceso completo

## Solución de Problemas

### La API no responde
```bash
docker-compose ps  # Verificar que los contenedores estén corriendo
docker-compose logs api  # Ver logs
```

### Error de conexión a la base de datos
```bash
docker-compose restart postgres
docker-compose exec api python manage.py init-db
```

### Los emails no se envían
```bash
docker-compose logs celery-worker  # Ver logs del worker
# Verificar configuración de email en .env
```

### Resetear todo
```bash
make clean
make setup
```

## Próximos Pasos

1. Crear tu frontend que consuma esta API
2. Configurar email de producción
3. Agregar autenticación más robusta en Flask-Admin
4. Implementar tests unitarios
5. Configurar CI/CD
6. Agregar monitoreo y logging avanzado

## Recursos

- [Documentación completa](./README.md)
- [Flask Docs](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Celery Docs](https://docs.celeryproject.org/)
