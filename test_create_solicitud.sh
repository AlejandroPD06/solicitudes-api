#!/bin/bash
# Test de creación de solicitud

echo "=== TEST: Crear Solicitud desde Frontend ==="
echo ""

# 1. Login como empleado
echo "1. Obteniendo token de empleado..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "empleado@solicitudes.com", "password": "empleado123"}')

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Error: No se pudo obtener el token"
    echo "Respuesta: $LOGIN_RESPONSE"
    exit 1
fi

echo "✅ Token obtenido: ${TOKEN:0:50}..."
echo ""

# 2. Crear solicitud
echo "2. Creando solicitud de prueba..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/solicitudes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "titulo": "TEST - Solicitud desde script",
    "descripcion": "Esta es una solicitud de prueba para verificar sincronización",
    "tipo": "compra",
    "prioridad": "alta"
  }')

echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null

if echo "$CREATE_RESPONSE" | grep -q "error"; then
    echo "❌ Error al crear solicitud"
    exit 1
fi

echo ""
echo "✅ Solicitud creada exitosamente"
echo ""

# 3. Verificar en la base de datos
echo "3. Verificando en la base de datos..."
docker exec solicitudes-postgres psql -U postgres -d solicitudes_db -c "SELECT id, titulo, tipo, estado, created_at FROM solicitudes ORDER BY id DESC LIMIT 3;"

echo ""
echo "=== TEST COMPLETADO ==="
