# Ejemplos de Uso de la API

Colección completa de ejemplos de curl para probar todos los endpoints de la API.

## Variables

```bash
# Configurar estas variables primero
export API_URL="http://localhost:5000"
export TOKEN="tu_access_token_aqui"
```

---

## 1. Health Check

```bash
curl -X GET $API_URL/health
```

---

## 2. Autenticación

### Registrar nuevo usuario

```bash
curl -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@ejemplo.com",
    "password": "password123",
    "nombre": "Nuevo",
    "apellido": "Usuario",
    "rol": "empleado"
  }'
```

### Login

```bash
curl -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empleado@solicitudes.com",
    "password": "empleado123"
  }' | jq
```

**Guardar el token:**
```bash
export TOKEN=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}' \
  | jq -r '.access_token')

echo "Token guardado: $TOKEN"
```

### Obtener perfil

```bash
curl -X GET $API_URL/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Actualizar perfil

```bash
curl -X PUT $API_URL/api/usuarios/perfil \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Nombre Actualizado",
    "apellido": "Apellido Actualizado"
  }' | jq
```

### Cambiar contraseña

```bash
curl -X POST $API_URL/api/usuarios/cambiar-password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password_actual": "empleado123",
    "password_nueva": "nueva_password123"
  }' | jq
```

---

## 3. Gestión de Usuarios (Jefe/Admin)

### Login como jefe

```bash
export TOKEN_JEFE=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jefe@solicitudes.com","password":"jefe123"}' \
  | jq -r '.access_token')
```

### Listar todos los usuarios

```bash
curl -X GET "$API_URL/api/usuarios/usuarios" \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq
```

### Listar usuarios con filtros

```bash
# Filtrar por rol
curl -X GET "$API_URL/api/usuarios/usuarios?rol=empleado" \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq

# Filtrar por estado activo
curl -X GET "$API_URL/api/usuarios/usuarios?activo=true" \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq

# Con paginación
curl -X GET "$API_URL/api/usuarios/usuarios?page=1&per_page=5" \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq
```

### Obtener usuario específico

```bash
curl -X GET "$API_URL/api/usuarios/usuarios/1" \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq
```

### Actualizar usuario (Admin)

```bash
export TOKEN_ADMIN=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' \
  | jq -r '.access_token')

curl -X PUT "$API_URL/api/usuarios/usuarios/3" \
  -H "Authorization: Bearer $TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{
    "rol": "jefe",
    "activo": true
  }' | jq
```

---

## 4. Solicitudes

### Crear solicitud

```bash
curl -X POST $API_URL/api/solicitudes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Compra de laptops HP",
    "descripcion": "Se requieren 5 laptops HP para el equipo de desarrollo web",
    "prioridad": "alta",
    "fecha_requerida": "2025-02-15"
  }' | jq
```

**Otros tipos de solicitudes:**

```bash
# Mantenimiento
curl -X POST $API_URL/api/solicitudes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "mantenimiento",
    "titulo": "Mantenimiento de servidores",
    "descripcion": "Mantenimiento preventivo de servidores de producción",
    "prioridad": "media"
  }' | jq

# Soporte técnico
curl -X POST $API_URL/api/solicitudes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "soporte_tecnico",
    "titulo": "Problema con impresora",
    "descripcion": "La impresora del 3er piso no funciona",
    "prioridad": "baja"
  }' | jq
```

### Listar solicitudes

```bash
# Todas mis solicitudes
curl -X GET $API_URL/api/solicitudes \
  -H "Authorization: Bearer $TOKEN" | jq

# Con filtros
curl -X GET "$API_URL/api/solicitudes?estado=pendiente&prioridad=alta" \
  -H "Authorization: Bearer $TOKEN" | jq

# Con paginación
curl -X GET "$API_URL/api/solicitudes?page=1&per_page=10" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Obtener solicitud específica

```bash
curl -X GET $API_URL/api/solicitudes/1 \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Actualizar solicitud

```bash
curl -X PUT $API_URL/api/solicitudes/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Compra de laptops HP EliteBook",
    "descripcion": "Se requieren 5 laptops HP EliteBook G9 para el equipo",
    "prioridad": "urgente"
  }' | jq
```

### Eliminar solicitud

```bash
curl -X DELETE $API_URL/api/solicitudes/1 \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 5. Gestión de Estado de Solicitudes (Jefe/Admin)

### Aprobar solicitud

```bash
curl -X PATCH $API_URL/api/solicitudes/1/estado \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "aprobada",
    "comentarios": "Aprobado por presupuesto disponible. Proceder con la compra."
  }' | jq
```

### Rechazar solicitud

```bash
curl -X PATCH $API_URL/api/solicitudes/2/estado \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "rechazada",
    "comentarios": "No hay presupuesto disponible en este momento."
  }' | jq
```

### Marcar como en proceso

```bash
curl -X PATCH $API_URL/api/solicitudes/3/estado \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "en_proceso",
    "comentarios": "Estamos trabajando en esto."
  }' | jq
```

### Marcar como completada

```bash
curl -X PATCH $API_URL/api/solicitudes/4/estado \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "completada",
    "comentarios": "Solicitud completada exitosamente."
  }' | jq
```

---

## 6. Estadísticas (Jefe/Admin)

### Estadísticas de solicitudes

```bash
curl -X GET $API_URL/api/solicitudes/estadisticas \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq
```

---

## 7. Notificaciones

### Listar notificaciones

```bash
curl -X GET $API_URL/api/notificaciones \
  -H "Authorization: Bearer $TOKEN" | jq

# Con filtros
curl -X GET "$API_URL/api/notificaciones?enviado=true&tipo=solicitud_aprobada" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Obtener notificación específica

```bash
curl -X GET $API_URL/api/notificaciones/1 \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Reenviar notificación (Admin)

```bash
curl -X POST $API_URL/api/notificaciones/1/reenviar \
  -H "Authorization: Bearer $TOKEN_ADMIN" | jq
```

### Listar notificaciones pendientes (Admin)

```bash
curl -X GET "$API_URL/api/notificaciones/pendientes?max_intentos=3" \
  -H "Authorization: Bearer $TOKEN_ADMIN" | jq
```

### Estadísticas de notificaciones (Jefe/Admin)

```bash
curl -X GET $API_URL/api/notificaciones/estadisticas \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq
```

---

## 8. Ejemplos Completos de Flujos

### Flujo completo: Empleado crea solicitud y jefe la aprueba

```bash
# 1. Login como empleado
export TOKEN_EMP=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}' \
  | jq -r '.access_token')

# 2. Crear solicitud
SOLICITUD=$(curl -s -X POST $API_URL/api/solicitudes \
  -H "Authorization: Bearer $TOKEN_EMP" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Compra de monitores",
    "descripcion": "Se requieren 3 monitores 4K para el equipo",
    "prioridad": "media"
  }')

SOLICITUD_ID=$(echo $SOLICITUD | jq -r '.solicitud.id')
echo "Solicitud creada con ID: $SOLICITUD_ID"

# 3. Login como jefe
export TOKEN_JEFE=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jefe@solicitudes.com","password":"jefe123"}' \
  | jq -r '.access_token')

# 4. Ver la solicitud
curl -s -X GET $API_URL/api/solicitudes/$SOLICITUD_ID \
  -H "Authorization: Bearer $TOKEN_JEFE" | jq

# 5. Aprobar la solicitud
curl -s -X PATCH $API_URL/api/solicitudes/$SOLICITUD_ID/estado \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "aprobada",
    "comentarios": "Aprobado. Proceder con la compra."
  }' | jq

# 6. Empleado verifica el estado
curl -s -X GET $API_URL/api/solicitudes/$SOLICITUD_ID \
  -H "Authorization: Bearer $TOKEN_EMP" | jq
```

---

## 9. Scripts Útiles

### Script para crear múltiples solicitudes de prueba

```bash
#!/bin/bash

TOKEN=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}' \
  | jq -r '.access_token')

for i in {1..5}; do
  curl -s -X POST $API_URL/api/solicitudes \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"tipo\": \"compra\",
      \"titulo\": \"Solicitud de prueba #$i\",
      \"descripcion\": \"Esta es la solicitud de prueba número $i\",
      \"prioridad\": \"media\"
    }" | jq '.solicitud.id'

  echo "Solicitud #$i creada"
  sleep 1
done
```

### Script para verificar todas las solicitudes pendientes

```bash
#!/bin/bash

TOKEN_JEFE=$(curl -s -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jefe@solicitudes.com","password":"jefe123"}' \
  | jq -r '.access_token')

curl -s -X GET "$API_URL/api/solicitudes?estado=pendiente" \
  -H "Authorization: Bearer $TOKEN_JEFE" \
  | jq '.solicitudes[] | {id, titulo, prioridad, usuario}'
```

---

## Notas

- Todos los ejemplos usan `jq` para formatear el JSON. Si no lo tienes instalado, elimina `| jq`
- Reemplaza `$API_URL` con tu URL si es diferente
- Los tokens expiran después de 1 hora por defecto
- Para producción, usa HTTPS en lugar de HTTP
