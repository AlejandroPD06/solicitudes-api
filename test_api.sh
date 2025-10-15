#!/bin/bash

echo "=== PRUEBA COMPLETA DEL MICROSERVICIO API ==="
echo ""

# 1. Health Check
echo "1. Health Check:"
curl -s http://localhost:5000/health | python3 -m json.tool
echo ""
echo ""

# 2. Login y obtener token
echo "2. Login (obtener JWT token):"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"empleado@solicitudes.com","password":"empleado123"}')

echo "$LOGIN_RESPONSE" | python3 -m json.tool
echo ""

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Token JWT: ${TOKEN:0:50}..."
echo ""
echo ""

# 3. Listar solicitudes
echo "3. GET /api/solicitudes (listar solicitudes del usuario):"
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/solicitudes | python3 -m json.tool
echo ""
echo ""

# 4. Crear solicitud
echo "4. POST /api/solicitudes (crear nueva solicitud):"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "compra",
    "titulo": "Test API Microservicio",
    "descripcion": "Solicitud creada via API REST para validar microservicio",
    "prioridad": "alta"
  }' \
  http://localhost:5000/api/solicitudes | python3 -m json.tool
echo ""
echo ""

# 5. Ver perfil
echo "5. GET /api/usuarios/perfil (ver mi perfil):"
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/usuarios/perfil | python3 -m json.tool
echo ""
echo ""

# 6. Login como admin
echo "6. Login como admin:"
ADMIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@solicitudes.com","password":"admin123"}')

ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Token Admin: ${ADMIN_TOKEN:0:50}..."
echo ""
echo ""

# 7. Listar notificaciones (admin)
echo "7. GET /api/notificaciones (listar notificaciones - admin):"
curl -s -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:5000/api/notificaciones | python3 -m json.tool | head -50
echo ""
echo ""

# 8. Estadísticas
echo "8. GET /api/solicitudes/estadisticas:"
curl -s -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:5000/api/solicitudes/estadisticas | python3 -m json.tool
echo ""
echo ""

echo "=== PRUEBA COMPLETADA ==="
