# 📚 Documentación del Sistema de Solicitudes

Bienvenido a la documentación completa del sistema. Aquí encontrarás toda la información necesaria para entender, usar y administrar el sistema.

---

## 📖 Guías Disponibles

### 🎯 [SISTEMA_COMPLETO.md](./SISTEMA_COMPLETO.md) ⭐ **EMPIEZA AQUÍ**
**La guía maestra de todo el sistema** (46 KB, ~1200 líneas)

Documento completo que explica:
- ✅ Arquitectura del sistema con diagramas
- ✅ Componentes y cómo interactúan
- ✅ Flujos de datos completos (login, crear usuario, etc.)
- ✅ Comandos para ver/probar cada componente
- ✅ API endpoints completos con ejemplos
- ✅ Base de datos (esquema, queries útiles)
- ✅ Autenticación y seguridad (JWT, Bcrypt)
- ✅ Casos de uso prácticos paso a paso
- ✅ Monitoreo y logs
- ✅ Troubleshooting común

**Cuándo usarlo:** Si quieres entender cómo funciona TODO el sistema o necesitas una referencia completa.

---

### 🔧 [COMO_FUNCIONA_LA_API.md](./COMO_FUNCIONA_LA_API.md)
**Explicación técnica detallada de la API** (21 KB, ~460 líneas)

Contiene:
- Arquitectura general (Frontend → Backend → DB)
- Stack tecnológico completo
- Flujo de creación de usuarios (6 pasos detallados)
- Sistema de autenticación JWT
- Estructura de tokens
- Modelo de datos con diagramas
- Seguridad (Bcrypt, JWT, CORS, roles)

**Cuándo usarlo:** Si eres desarrollador y quieres entender la arquitectura técnica.

---

### 🚀 [COMO_USAR_LA_API.md](./COMO_USAR_LA_API.md)
**Guía práctica de uso de la API** (25 KB, ~760 líneas)

Incluye:
- Ver logs en tiempo real
- Ejemplos con curl para todos los endpoints
- Configuración de Postman/Insomnia
- Scripts Python completos
- Ver base de datos directamente
- Tabla de todos los endpoints
- Ejemplos de debugging avanzado

**Cuándo usarlo:** Cuando quieras interactuar directamente con la API sin el frontend.

---

### 👥 [COMO_AGREGAR_USUARIOS.md](./COMO_AGREGAR_USUARIOS.md)
**3 métodos para agregar usuarios** (11 KB, ~460 líneas)

Métodos:
1. Desde la API con curl
2. Desde Python/Script
3. Desde Postman/Insomnia

Además:
- Tipos de roles y permisos
- Gestión de usuarios (cambiar rol, activar/desactivar)
- Ejemplos rápidos
- Solución de problemas

**Cuándo usarlo:** Cuando necesites crear usuarios nuevos o cambiar roles.

---

### 📚 [SWAGGER_DOCUMENTACION.md](./SWAGGER_DOCUMENTACION.md) ⭐ **NUEVA**
**Documentación interactiva de la API con Swagger** (16 KB, ~900 líneas)

Incluye:
- ✅ Interfaz web interactiva en `/api/docs`
- ✅ Probar endpoints desde el navegador
- ✅ Autenticación con JWT directamente en Swagger
- ✅ Ejemplos de request/response para cada endpoint
- ✅ Guía paso a paso de cómo usar Swagger UI
- ✅ Exportar especificación OpenAPI
- ✅ Comandos curl equivalentes
- ✅ Integración con Postman/Insomnia

**Cuándo usarlo:** Cuando quieras probar la API de forma visual e interactiva sin escribir código.

---

## 🗺️ Mapa de Navegación

```
¿Qué necesitas hacer?

📖 Entender TODO el sistema
   └─> SISTEMA_COMPLETO.md

🔧 Ver cómo funciona la API (técnico)
   └─> COMO_FUNCIONA_LA_API.md

🚀 Probar endpoints con comandos
   └─> COMO_USAR_LA_API.md

📚 Probar endpoints visualmente (Swagger)
   └─> SWAGGER_DOCUMENTACION.md
   └─> http://localhost:5000/api/docs

👥 Crear usuarios o cambiar roles
   └─> COMO_AGREGAR_USUARIOS.md

🐛 Resolver un problema
   └─> SISTEMA_COMPLETO.md → Sección "Troubleshooting"

📊 Ver logs o monitorear
   └─> SISTEMA_COMPLETO.md → Sección "Monitoreo y Logs"

💾 Consultas SQL
   └─> SISTEMA_COMPLETO.md → Sección "Base de Datos"
```

---

## ⚡ Comandos Rápidos

### Iniciar el sistema
```bash
# Backend
cd solicitudes-api
docker compose up -d

# Frontend
cd solicitudes-frontend
npm run dev
```

### Ver logs
```bash
# API
docker compose logs -f api

# Base de datos
docker compose logs -f db

# Todos los servicios
docker compose logs -f
```

### Probar API
```bash
# Swagger UI (interfaz visual)
http://localhost:5000/api/docs

# Health check
curl http://localhost:5000/health

# Login
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}'

# Script de prueba
cd solicitudes-api
python3 test_api.py
```

### Base de datos
```bash
# Conectarse
docker compose exec db psql -U postgres solicitudes_db

# Ver usuarios
docker compose exec db psql -U postgres solicitudes_db -c \
  "SELECT id, nombre, email, rol FROM usuarios;"
```

---

## 📂 Estructura de la Documentación

```
documentacion/
├── README.md                    ← Estás aquí (índice)
├── SISTEMA_COMPLETO.md          ← 🌟 Guía maestra
├── COMO_FUNCIONA_LA_API.md      ← Explicación técnica
├── COMO_USAR_LA_API.md          ← Guía práctica de uso
├── COMO_AGREGAR_USUARIOS.md     ← Gestión de usuarios
└── SWAGGER_DOCUMENTACION.md     ← 📚 Documentación Swagger/OpenAPI
```

---

## 🎯 Casos de Uso por Rol

### Soy Desarrollador
1. Lee [SISTEMA_COMPLETO.md](./SISTEMA_COMPLETO.md) secciones:
   - Arquitectura del Sistema
   - Componentes del Sistema
   - Flujo de Datos Completo
2. Luego [COMO_FUNCIONA_LA_API.md](./COMO_FUNCIONA_LA_API.md)
3. Para testing:
   - Visual: [SWAGGER_DOCUMENTACION.md](./SWAGGER_DOCUMENTACION.md) o http://localhost:5000/api/docs
   - Comandos: [COMO_USAR_LA_API.md](./COMO_USAR_LA_API.md)

### Soy Administrador del Sistema
1. Lee [SISTEMA_COMPLETO.md](./SISTEMA_COMPLETO.md) secciones:
   - Comandos por Componente
   - Monitoreo y Logs
   - Troubleshooting
2. Para usuarios: [COMO_AGREGAR_USUARIOS.md](./COMO_AGREGAR_USUARIOS.md)

### Soy QA/Tester
1. [SWAGGER_DOCUMENTACION.md](./SWAGGER_DOCUMENTACION.md) → Testing visual interactivo
2. [COMO_USAR_LA_API.md](./COMO_USAR_LA_API.md) → Comandos curl y scripts
3. [SISTEMA_COMPLETO.md](./SISTEMA_COMPLETO.md) → "Casos de Uso Prácticos"

### Solo quiero usar el sistema
- Abre http://localhost:5173
- Credenciales por defecto en [COMO_AGREGAR_USUARIOS.md](./COMO_AGREGAR_USUARIOS.md)

---

## 🔍 Búsqueda Rápida

### ¿Cómo...?

| Pregunta | Archivo | Sección |
|----------|---------|---------|
| Ver logs de la API | SISTEMA_COMPLETO.md | Monitoreo y Logs |
| Crear un usuario | COMO_AGREGAR_USUARIOS.md | Desde la API con curl |
| Conectarme a PostgreSQL | SISTEMA_COMPLETO.md | Base de Datos |
| Probar endpoints visualmente | SWAGGER_DOCUMENTACION.md | Interfaz Swagger UI |
| Probar un endpoint con curl | COMO_USAR_LA_API.md | Probar Endpoints con curl |
| Entender JWT | COMO_FUNCIONA_LA_API.md | Sistema de Autenticación |
| Ver usuarios en DB | SISTEMA_COMPLETO.md | Base de Datos → Comandos SQL |
| Resolver error de token | SISTEMA_COMPLETO.md | Troubleshooting |
| Cambiar rol de usuario | COMO_AGREGAR_USUARIOS.md | Gestión de Usuarios |
| Usar Swagger | SWAGGER_DOCUMENTACION.md | Guía paso a paso |

---

## 📞 Soporte

Si tienes preguntas que no están cubiertas en la documentación:

1. **Ver logs**: `docker compose logs -f api`
2. **Revisar base de datos**: `docker compose exec db psql -U postgres solicitudes_db`
3. **Health check**: `curl http://localhost:5000/health`
4. **Sección Troubleshooting** en SISTEMA_COMPLETO.md

---

## 📊 Estadísticas de Documentación

| Archivo | Tamaño | Líneas | Última actualización |
|---------|--------|--------|---------------------|
| SISTEMA_COMPLETO.md | 46 KB | ~1200 | 2025-10-15 |
| COMO_USAR_LA_API.md | 25 KB | ~760 | 2025-10-15 |
| COMO_FUNCIONA_LA_API.md | 21 KB | ~460 | 2025-10-15 |
| SWAGGER_DOCUMENTACION.md | 16 KB | ~900 | 2025-10-15 |
| COMO_AGREGAR_USUARIOS.md | 11 KB | ~460 | 2025-10-15 |

**Total:** ~119 KB de documentación completa

---

**¡Buena lectura! 📚**
