# 🔧 Cómo Funciona la API de Solicitudes

Esta guía técnica explica el funcionamiento interno de la API, con énfasis en la gestión de usuarios.

---

## 📋 Índice

1. [Arquitectura General](#arquitectura-general)
2. [Flujo de Creación de Usuarios](#flujo-de-creación-de-usuarios)
3. [Sistema de Autenticación](#sistema-de-autenticación)
4. [Endpoints de Usuarios](#endpoints-de-usuarios)
5. [Base de Datos](#base-de-datos)
6. [Seguridad](#seguridad)

---

## 🏗️ Arquitectura General

### Stack Tecnológico

```
┌─────────────────────────────────────┐
│         Frontend (React)            │
│      http://localhost:5173          │
└──────────────┬──────────────────────┘
               │ HTTP/REST API
               │ JWT Bearer Token
┌──────────────▼──────────────────────┐
│      Backend (Flask)                │
│      http://localhost:5000          │
│                                     │
│  ┌───────────────────────────┐    │
│  │  Flask Blueprints         │    │
│  │  - auth_bp (usuarios)     │    │
│  │  - solicitudes_bp         │    │
│  │  - notificaciones_bp      │    │
│  └───────────────────────────┘    │
│                                     │
│  ┌───────────────────────────┐    │
│  │  Services                 │    │
│  │  - auth_service           │    │
│  │  - solicitudes_service    │    │
│  └───────────────────────────┘    │
│                                     │
│  ┌───────────────────────────┐    │
│  │  Models (SQLAlchemy)      │    │
│  │  - Usuario                │    │
│  │  - Solicitud              │    │
│  │  - Notificacion           │    │
│  └───────────────────────────┘    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      PostgreSQL Database            │
│      Tablas: usuarios, solicitudes  │
└─────────────────────────────────────┘
```

### Componentes Clave

1. **Flask Application** (`app/__init__.py`)
   - Inicializa la aplicación
   - Configura extensiones (SQLAlchemy, JWT, CORS)
   - Registra blueprints

2. **Blueprints** (`app/routes/`)
   - `auth_bp`: Autenticación y gestión de usuarios
   - `solicitudes_bp`: CRUD de solicitudes
   - `notificaciones_bp`: Sistema de notificaciones

3. **Services** (`app/services/`)
   - Lógica de negocio separada de las rutas
   - Validaciones y transformaciones
   - Interacción con la base de datos

4. **Models** (`app/models/`)
   - Definición de tablas (ORM SQLAlchemy)
   - Métodos de instancia y clase
   - Relaciones entre tablas

---

## 👤 Flujo de Creación de Usuarios

### Paso a Paso: ¿Qué sucede cuando creas un usuario?

#### 1️⃣ **Request del Frontend**

```javascript
// GestionUsuarios.jsx - línea 54-80
const handleCreateUsuario = async (e) => {
  e.preventDefault();

  const token = localStorage.getItem('access_token');
  await axios.post(
    'http://localhost:5000/api/usuarios/registro',
    {
      email: 'nuevo@empresa.com',
      password: 'password123',
      nombre: 'Juan',
      apellido: 'Pérez',
      rol: 'empleado'
    },
    { headers: { Authorization: `Bearer ${token}` } }
  );
};
```

**¿Qué envía?**
- URL: `POST /api/usuarios/registro`
- Headers: `Authorization: Bearer <token>` (JWT del admin)
- Body: JSON con datos del usuario

---

#### 2️⃣ **Recepción en el Blueprint**

```python
# app/routes/auth.py - líneas 18-61
@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()

    # Validar campos requeridos
    campos_requeridos = ['email', 'password', 'nombre']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    # Registrar usuario
    usuario, error = registrar_usuario(
        email=data['email'],
        password=data['password'],
        nombre=data['nombre'],
        apellido=data.get('apellido'),
        rol=data.get('rol', 'empleado')
    )

    if error:
        return jsonify({'error': error}), 400

    # Crear tokens
    tokens = crear_tokens(usuario)

    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict(),
        **tokens
    }), 201
```

**¿Qué hace?**
1. Extrae los datos JSON del request
2. Valida que existan los campos obligatorios (email, password, nombre)
3. Llama al servicio `registrar_usuario()`
4. Genera tokens JWT para el nuevo usuario
5. Devuelve respuesta con usuario creado + tokens

---

#### 3️⃣ **Servicio de Registro**

```python
# app/services/auth_service.py
def registrar_usuario(email, password, nombre, apellido=None, rol='empleado'):
    """
    Registrar un nuevo usuario en el sistema.

    Args:
        email (str): Email del usuario (único)
        password (str): Contraseña en texto plano (será hasheada)
        nombre (str): Nombre del usuario
        apellido (str, opcional): Apellido del usuario
        rol (str): Rol del usuario (empleado, jefe, administrador)

    Returns:
        tuple: (usuario, error)
            - usuario: Objeto Usuario si fue exitoso, None si falló
            - error: String con mensaje de error, None si fue exitoso
    """

    # 1. Verificar si el email ya existe
    if Usuario.query.filter_by(email=email).first():
        return None, 'El email ya está registrado'

    # 2. Validar rol
    roles_validos = ['empleado', 'jefe', 'administrador']
    if rol not in roles_validos:
        return None, f'Rol inválido. Debe ser uno de: {", ".join(roles_validos)}'

    # 3. Crear instancia de Usuario
    usuario = Usuario(
        email=email,
        nombre=nombre,
        apellido=apellido,
        rol=rol,
        activo=True
    )

    # 4. Hash de contraseña (Bcrypt automáticamente con el setter)
    usuario.password = password  # Llama a @password.setter que hashea

    # 5. Guardar en base de datos
    try:
        db.session.add(usuario)
        db.session.commit()
        return usuario, None
    except Exception as e:
        db.session.rollback()
        return None, f'Error al crear usuario: {str(e)}'
```

**¿Qué hace?**
1. **Validación de duplicados**: Busca si el email ya existe
2. **Validación de rol**: Verifica que sea empleado, jefe o administrador
3. **Creación de instancia**: Crea objeto Usuario con los datos
4. **Hash de contraseña**: Usa Bcrypt para hashear la contraseña (seguridad)
5. **Persistencia**: Guarda en PostgreSQL usando SQLAlchemy

---

#### 4️⃣ **Modelo Usuario**

```python
# app/models/usuario.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class Usuario(db.Model):
    """Modelo de usuario con autenticación y roles."""

    __tablename__ = 'usuarios'

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    rol = db.Column(db.String(20), default='empleado', nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    solicitudes = db.relationship('Solicitud', backref='usuario', lazy=True)

    @property
    def password(self):
        """No permitir lectura de contraseña."""
        raise AttributeError('La contraseña no es un atributo legible')

    @password.setter
    def password(self, password):
        """Hashear contraseña al asignarla."""
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        """Verificar si la contraseña coincide con el hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convertir usuario a diccionario (para JSON)."""
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rol': self.rol,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

**¿Qué hace?**
- **Define la tabla**: Estructura de la tabla `usuarios` en PostgreSQL
- **Hash automático**: El setter `@password.setter` hashea con Bcrypt
- **Verificación**: `verificar_password()` compara hash sin revelar contraseña
- **Serialización**: `to_dict()` convierte el objeto a JSON para la API

---

#### 5️⃣ **Base de Datos PostgreSQL**

```sql
-- Tabla generada por SQLAlchemy
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    rol VARCHAR(20) NOT NULL DEFAULT 'empleado',
    activo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

-- Ejemplo de fila insertada:
INSERT INTO usuarios VALUES (
    4,
    'nuevo@empresa.com',
    '$2b$12$K8Z.../hash...', -- Bcrypt hash
    'Juan',
    'Pérez',
    'empleado',
    true,
    '2025-10-15 16:29:48.365083'
);
```

---

#### 6️⃣ **Respuesta al Frontend**

```json
{
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 4,
    "email": "nuevo@empresa.com",
    "nombre": "Juan",
    "apellido": "Pérez",
    "rol": "empleado",
    "activo": true,
    "created_at": "2025-10-15T16:29:48.365083"
  },
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "Bearer"
}
```

**¿Qué contiene?**
- **usuario**: Datos del usuario creado (sin contraseña)
- **access_token**: JWT para autenticar requests (expira en 1 hora)
- **refresh_token**: JWT para renovar el access_token (expira en 30 días)

---

## 🔐 Sistema de Autenticación

### JWT (JSON Web Tokens)

```python
# app/services/auth_service.py
from flask_jwt_extended import create_access_token, create_refresh_token

def crear_tokens(usuario):
    """Crear tokens JWT para un usuario."""
    identity = str(usuario.id)

    return {
        'access_token': create_access_token(identity=identity),
        'refresh_token': create_refresh_token(identity=identity),
        'token_type': 'Bearer'
    }
```

### Estructura de un JWT

```
Header (algoritmo):
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload (datos):
{
  "sub": "4",              # ID del usuario
  "iat": 1760545788,       # Issued at
  "exp": 1760549388,       # Expira en 1 hora
  "type": "access",        # Tipo de token
  "fresh": false
}

Signature (firma):
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)
```

### Protección de Endpoints

```python
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import rol_requerido

# Requiere estar autenticado
@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil():
    usuario_id = get_jwt_identity()
    # ...

# Requiere rol específico
@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@rol_requerido('jefe', 'administrador')
def listar_usuarios():
    # Solo jefes y administradores pueden listar usuarios
    # ...
```

---

## 🔌 Endpoints de Usuarios

### Tabla Completa de Rutas

| Método | Endpoint | Autenticación | Rol Requerido | Descripción |
|--------|----------|---------------|---------------|-------------|
| `POST` | `/api/usuarios/registro` | Opcional | - | Crear nuevo usuario |
| `POST` | `/api/usuarios/login` | No | - | Iniciar sesión |
| `GET` | `/api/usuarios/perfil` | Sí | - | Obtener mi perfil |
| `PUT` | `/api/usuarios/perfil` | Sí | - | Actualizar mi perfil |
| `POST` | `/api/usuarios/cambiar-password` | Sí | - | Cambiar mi contraseña |
| `GET` | `/api/usuarios/usuarios` | Sí | jefe, admin | Listar usuarios |
| `GET` | `/api/usuarios/usuarios/:id` | Sí | jefe, admin | Ver usuario específico |
| `PUT` | `/api/usuarios/usuarios/:id` | Sí | admin | Actualizar usuario |
| `DELETE` | `/api/usuarios/usuarios/:id` | Sí | admin | Eliminar usuario |

### Ejemplos de Uso

#### Crear Usuario (Sin Autenticación - Registro Público)

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

**Nota**: Por defecto crea usuarios con rol `empleado`. Para crear con otro rol, debe estar autenticado como administrador.

#### Crear Usuario con Rol (Como Administrador)

```bash
curl -X POST http://localhost:5000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "email": "jefe@empresa.com",
    "password": "jefe123",
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "rol": "jefe"
  }'
```

#### Listar Usuarios

```bash
curl -X GET http://localhost:5000/api/usuarios/usuarios \
  -H "Authorization: Bearer eyJhbGc..."
```

#### Cambiar Rol de Usuario

```bash
curl -X PUT http://localhost:5000/api/usuarios/usuarios/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{"rol": "jefe"}'
```

#### Desactivar Usuario

```bash
curl -X PUT http://localhost:5000/api/usuarios/usuarios/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{"activo": false}'
```

---

## 🗄️ Base de Datos

### Modelo de Datos

```
┌─────────────────────────┐
│       usuarios          │
├─────────────────────────┤
│ id (PK)                 │
│ email (UNIQUE)          │
│ password_hash           │
│ nombre                  │
│ apellido                │
│ rol (empleado/jefe/admin)│
│ activo (boolean)        │
│ created_at              │
└────────┬────────────────┘
         │ 1:N
         │
┌────────▼────────────────┐
│      solicitudes        │
├─────────────────────────┤
│ id (PK)                 │
│ usuario_id (FK)         │
│ titulo                  │
│ descripcion             │
│ prioridad               │
│ estado                  │
│ created_at              │
└─────────────────────────┘
```

### Conexión a la Base de Datos

```python
# config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:password@db:5432/solicitudes_db'

# app/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Crea tablas si no existen

    return app
```

### Migraciones

```bash
# Crear migración
flask db migrate -m "Agregar campo telefono a usuarios"

# Aplicar migraciones
flask db upgrade

# Revertir migración
flask db downgrade
```

---

## 🔒 Seguridad

### 1. Hashing de Contraseñas

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Al crear/actualizar
password_hash = generate_password_hash('password123')
# Resultado: '$2b$12$K8Z...muy_largo_hash...'

# Al verificar login
is_valid = check_password_hash(password_hash, 'password123')
# True si coincide, False si no
```

**Características de Bcrypt:**
- Salt automático (aleatorio por usuario)
- Cost factor configurable (12 por defecto)
- Slow hashing (previene ataques de fuerza bruta)

### 2. JWT Tokens

```python
# Configuración en config.py
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Debe ser aleatorio y secreto
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

**Buenas prácticas:**
- Secret key en variables de entorno
- Access token de corta duración (1 hora)
- Refresh token de larga duración (30 días)
- No almacenar información sensible en el payload

### 3. CORS (Cross-Origin Resource Sharing)

```python
# app/__init__.py
from flask_cors import CORS

CORS(app, origins=['http://localhost:5173'])
```

**Configuración:**
- Solo permite requests desde el frontend (localhost:5173)
- Previene ataques CSRF desde otros dominios

### 4. Validación de Roles

```python
# app/services/auth_service.py
def rol_requerido(*roles_permitidos):
    """Decorador para requerir roles específicos."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            usuario = obtener_usuario_actual()

            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            if usuario.rol not in roles_permitidos:
                return jsonify({'error': 'Permisos insuficientes'}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

**Uso:**
```python
@rol_requerido('administrador')
def eliminar_usuario(usuario_id):
    # Solo administradores pueden ejecutar esta función
```

---

## 🔍 Debugging y Logs

### Ver logs del contenedor

```bash
docker compose logs -f api
```

### Logs importantes

```python
# La API registra automáticamente:
[2025-10-15 16:29:48] INFO: Nuevo usuario registrado: nuevo@empresa.com
[2025-10-15 16:30:15] INFO: Login exitoso: nuevo@empresa.com
[2025-10-15 16:31:22] WARNING: Intento de acceso no autorizado a /api/usuarios/usuarios
[2025-10-15 16:32:10] ERROR: Error al crear usuario: Email ya registrado
```

---

## 📊 Resumen del Flujo Completo

```
1. Frontend (React)
   └─> Envía POST /api/usuarios/registro con datos
       │
2. Flask Blueprint (auth.py)
   └─> Valida campos requeridos
       │
3. Auth Service (auth_service.py)
   └─> Verifica email único
   └─> Valida rol
   └─> Crea instancia Usuario
       │
4. Modelo Usuario (usuario.py)
   └─> Hashea contraseña con Bcrypt
   └─> Define estructura de tabla
       │
5. SQLAlchemy
   └─> Ejecuta INSERT en PostgreSQL
       │
6. PostgreSQL
   └─> Almacena fila en tabla usuarios
       │
7. Respuesta
   └─> Genera JWT tokens
   └─> Serializa usuario a JSON
   └─> Devuelve 201 Created
       │
8. Frontend
   └─> Recibe usuario + tokens
   └─> Guarda tokens en localStorage
   └─> Actualiza lista de usuarios
```

---

## 🎓 Conceptos Clave

| Concepto | Explicación |
|----------|-------------|
| **Blueprint** | Módulo de Flask para organizar rutas (similar a router en Express) |
| **ORM** | Object-Relational Mapping - SQLAlchemy traduce objetos Python a SQL |
| **JWT** | JSON Web Token - Token firmado para autenticación sin estado |
| **Bcrypt** | Algoritmo de hashing para contraseñas (lento por diseño, más seguro) |
| **Decorator** | `@jwt_required()` - Envuelve funciones para agregar funcionalidad |
| **Migration** | Script para modificar estructura de base de datos versionada |
| **CORS** | Política de seguridad del navegador para requests entre dominios |

---

## 🚀 Próximos Pasos

Para extender la funcionalidad de usuarios:

1. **Verificación de email**: Enviar código de confirmación
2. **Recuperación de contraseña**: Reset por email
3. **2FA**: Autenticación de dos factores
4. **Logs de auditoría**: Registrar cambios en usuarios
5. **Permisos granulares**: Más allá de roles (RBAC)

---

**¿Preguntas?** Revisa los comentarios en el código o consulta la documentación de Flask en https://flask.palletsprojects.com
