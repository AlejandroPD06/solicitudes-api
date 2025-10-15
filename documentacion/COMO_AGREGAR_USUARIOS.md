# 👥 Guía Completa: Cómo Agregar Usuarios y Administradores

Esta guía te muestra **3 formas** de agregar usuarios al sistema.

---

## 📋 Índice

1. [Desde la API con curl](#1-desde-la-api-con-curl)
2. [Desde Python/Script](#2-desde-pythonscript)
3. [Desde Postman/Insomnia](#3-desde-postmaninsomnia)
4. [Tipos de Roles](#tipos-de-roles)
5. [Gestión de Usuarios](#gestión-de-usuarios)

---

## 1. Desde la API con curl

### ✅ Método 1A: Registro Público (Solo para Empleados)

Este endpoint está disponible públicamente y crea usuarios con rol **empleado** por defecto.

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@empresa.com",
    "password": "password123",
    "nombre": "Juan",
    "apellido": "Pérez"
  }'
```

**Respuesta exitosa:**
```json
{
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 4,
    "email": "nuevo@empresa.com",
    "nombre": "Juan",
    "apellido": "Pérez",
    "rol": "empleado",
    "activo": true
  }
}
```

---

### 🔐 Método 1B: Crear Usuario con Rol Específico (Solo Administradores)

Para crear usuarios con roles específicos (jefe o administrador), necesitas estar autenticado como **administrador**.

**Paso 1: Login como Admin**
```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@solicitudes.com",
    "password": "admin123"
  }'
```

**Guardar el token:**
```bash
# Copiar el access_token de la respuesta
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Paso 2: Crear Usuario con Rol**
```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "nuevo.jefe@empresa.com",
    "password": "password123",
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "rol": "jefe"
  }'
```

**Roles disponibles:**
- `empleado` - Usuario básico
- `jefe` - Puede aprobar/rechazar solicitudes
- `administrador` - Control total del sistema

---

## 2. Desde Python/Script

### 📝 Script para Crear Usuarios Múltiples

Guarda este código como `crear_usuarios.py`:

```python
#!/usr/bin/env python3
import requests
import json

# Configuración
API_URL = "http://localhost:5000/api"

# Datos de usuarios a crear
usuarios = [
    {
        "email": "maria.lopez@empresa.com",
        "password": "password123",
        "nombre": "María",
        "apellido": "López",
        "rol": "empleado"
    },
    {
        "email": "pedro.gonzalez@empresa.com",
        "password": "password123",
        "nombre": "Pedro",
        "apellido": "González",
        "rol": "jefe"
    },
    {
        "email": "ana.martinez@empresa.com",
        "password": "password123",
        "nombre": "Ana",
        "apellido": "Martínez",
        "rol": "administrador"
    }
]

def login_admin():
    """Login como administrador para obtener token"""
    response = requests.post(
        f"{API_URL}/usuarios/login",
        json={
            "email": "admin@solicitudes.com",
            "password": "admin123"
        }
    )
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"❌ Error en login: {response.text}")
        return None

def crear_usuario(token, usuario_data):
    """Crear un usuario"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{API_URL}/usuarios/registro",
        json=usuario_data,
        headers=headers
    )

    if response.status_code == 201:
        user = response.json()['usuario']
        print(f"✅ Usuario creado: {user['email']} - {user['rol']}")
        return True
    else:
        print(f"❌ Error creando {usuario_data['email']}: {response.text}")
        return False

def main():
    print("🚀 Iniciando creación de usuarios...\n")

    # Login
    token = login_admin()
    if not token:
        return

    print(f"✅ Token obtenido\n")

    # Crear usuarios
    exitosos = 0
    for usuario in usuarios:
        if crear_usuario(token, usuario):
            exitosos += 1

    print(f"\n📊 Resumen: {exitosos}/{len(usuarios)} usuarios creados exitosamente")

if __name__ == "__main__":
    main()
```

**Ejecutar:**
```bash
python3 crear_usuarios.py
```

---

## 3. Desde Postman/Insomnia

### Configuración en Postman

**Paso 1: Crear Colección**

1. Abre Postman
2. Click en "New Collection" → nombre: "Solicitudes API"
3. Agrega la variable `{{base_url}}` = `http://localhost:5000/api`

**Paso 2: Login como Admin**

```
POST {{base_url}}/usuarios/login

Body (JSON):
{
  "email": "admin@solicitudes.com",
  "password": "admin123"
}

Tests (guardar token automáticamente):
pm.test("Login exitoso", function () {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
});
```

**Paso 3: Crear Usuario**

```
POST {{base_url}}/usuarios/registro

Headers:
Authorization: Bearer {{access_token}}

Body (JSON):
{
  "email": "nuevo@empresa.com",
  "password": "password123",
  "nombre": "Nuevo",
  "apellido": "Usuario",
  "rol": "empleado"
}
```

---

## 📌 Tipos de Roles

### 👔 Empleado (`empleado`)
**Permisos:**
- ✅ Crear solicitudes
- ✅ Ver sus propias solicitudes
- ✅ Editar sus solicitudes pendientes
- ❌ Ver solicitudes de otros
- ❌ Aprobar/rechazar solicitudes

**Casos de uso:**
- Usuarios regulares del sistema
- Personal que necesita hacer solicitudes

---

### 👨‍💼 Jefe (`jefe`)
**Permisos:**
- ✅ Todo lo que puede hacer un empleado
- ✅ Ver TODAS las solicitudes del sistema
- ✅ Aprobar o rechazar solicitudes
- ✅ Ver estadísticas generales
- ❌ Gestionar usuarios

**Casos de uso:**
- Supervisores
- Gerentes de área
- Personas que aprueban solicitudes

---

### 👑 Administrador (`administrador`)
**Permisos:**
- ✅ Todo lo que puede hacer un jefe
- ✅ Gestionar usuarios (crear, editar, eliminar)
- ✅ Cambiar roles de usuarios
- ✅ Acceso completo al sistema
- ✅ Ver panel de administración

**Casos de uso:**
- Administradores del sistema
- TI/Sistemas
- Personal de RR.HH.

---

## 🔧 Gestión de Usuarios

### Ver Todos los Usuarios (Solo Admin)

```bash
curl -X GET http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer $TOKEN"
```

---

### Cambiar Rol de un Usuario (Solo Admin)

```bash
curl -X PUT http://localhost:5000/api/usuarios/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "rol": "jefe"
  }'
```

---

### Desactivar un Usuario (Solo Admin)

```bash
curl -X PUT http://localhost:5000/api/usuarios/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activo": false
  }'
```

---

### Cambiar Contraseña (Cualquier Usuario)

```bash
curl -X POST http://localhost:5000/api/usuarios/cambiar-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "password_actual": "password123",
    "password_nueva": "nueva_password456"
  }'
```

---

## 🎯 Ejemplos Rápidos

### Crear un Jefe

```bash
# 1. Login como admin
TOKEN=$(curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 2. Crear jefe
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "jefe.nuevo@empresa.com",
    "password": "jefe123",
    "nombre": "Roberto",
    "apellido": "Silva",
    "rol": "jefe"
  }'
```

---

### Crear un Administrador

```bash
# Usando el mismo TOKEN del ejemplo anterior
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "admin.nuevo@empresa.com",
    "password": "admin123",
    "nombre": "Lucía",
    "apellido": "Fernández",
    "rol": "administrador"
  }'
```

---

### Crear Múltiples Empleados

```bash
# Array de emails
emails=("emp1@empresa.com" "emp2@empresa.com" "emp3@empresa.com")
nombres=("Carlos" "Diana" "Eduardo")
apellidos=("Ruiz" "Torres" "Vega")

# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Crear usuarios
for i in ${!emails[@]}; do
  echo "Creando: ${emails[$i]}"
  curl -s -X POST http://localhost:5000/api/usuarios/registro \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{
      \"email\": \"${emails[$i]}\",
      \"password\": \"password123\",
      \"nombre\": \"${nombres[$i]}\",
      \"apellido\": \"${apellidos[$i]}\",
      \"rol\": \"empleado\"
    }" | python3 -m json.tool
  echo "---"
done
```

---

## ⚠️ Importante

1. **Contraseñas Seguras:** En producción, usa contraseñas fuertes
2. **Email Único:** Cada email solo puede usarse una vez
3. **Roles:** Solo los administradores pueden asignar roles diferentes a "empleado"
4. **Tokens:** Los tokens JWT expiran después de 1 hora
5. **Activación:** Todos los usuarios se crean activos por defecto

---

## 🆘 Solución de Problemas

### "Email already registered"
**Problema:** El email ya existe en la base de datos
**Solución:** Usa otro email o actualiza el usuario existente

### "Unauthorized"
**Problema:** Token inválido o expirado
**Solución:** Haz login nuevamente para obtener un token nuevo

### "Permission denied"
**Problema:** Tu usuario no tiene permisos para esta acción
**Solución:** Asegúrate de estar usando una cuenta de administrador

---

## 📚 Próximos Pasos

Una vez que hayas creado usuarios, puedes:

1. **Iniciar sesión** con las credenciales creadas
2. **Crear solicitudes** como empleado
3. **Aprobar solicitudes** como jefe o administrador
4. **Gestionar el sistema** como administrador

---

**¿Necesitas ayuda?** Revisa los logs de la API en:
```bash
docker compose logs -f api
```
