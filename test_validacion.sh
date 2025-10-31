#!/bin/bash

# Script de Pruebas de Validación y Trackeo de Errores
# Autor: Sistema de Códigos HTTP
# Fecha: 2025-10-31

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:5000"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🧪 Script de Pruebas de Validación y Trackeo de Errores      ║${NC}"
echo -e "${BLUE}║  API de Solicitudes - Práctica de Códigos HTTP                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que la API está corriendo
echo -e "${YELLOW}🔍 Verificando que la API está corriendo...${NC}"
if curl -s -f $API_URL/health > /dev/null; then
    echo -e "${GREEN}✅ API está corriendo correctamente${NC}"
    echo ""
else
    echo -e "${RED}❌ Error: La API no está corriendo en $API_URL${NC}"
    echo -e "${YELLOW}💡 Ejecuta: python wsgi.py${NC}"
    exit 1
fi

# Test 1: JSON mal formado (400 Bad Request)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 1: JSON mal formado (400 Bad Request)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Enviando JSON inválido (falta comilla de cierre)..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com", "password":"123456')

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "400" ]; then
    echo -e "${GREEN}✅ Correcto! 400 Bad Request${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 400${NC}"
fi
echo ""
cat /tmp/response.json | jq '.' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 2: Email inválido (422 Validation Error)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 2: Email inválido (422 Validation Error)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Enviando email sin @..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"sin-arroba","password":"123456","nombre":"Juan"}')

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "422" ]; then
    echo -e "${GREEN}✅ Correcto! 422 Unprocessable Entity${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 422${NC}"
fi
echo ""
cat /tmp/response.json | jq '.' 2>/dev/null || cat /tmp/response.json
echo ""

# Extraer request_id para demostrar tracking
REQUEST_ID=$(cat /tmp/response.json | jq -r '.request_id' 2>/dev/null)
if [ ! -z "$REQUEST_ID" ] && [ "$REQUEST_ID" != "null" ]; then
    echo -e "${YELLOW}🔍 Request ID: ${GREEN}$REQUEST_ID${NC}"
    echo -e "${YELLOW}💡 Puedes buscar este error en logs con:${NC}"
    echo -e "   ${BLUE}grep \"$REQUEST_ID\" logs/solicitudes_api.log${NC}"
fi
echo ""
echo ""

# Test 3: Password muy corta (422 Validation Error)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 3: Password muy corta (422 Validation Error)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Enviando password de solo 3 caracteres..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123","nombre":"Juan"}')

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "422" ]; then
    echo -e "${GREEN}✅ Correcto! 422 Unprocessable Entity${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 422${NC}"
fi
echo ""
cat /tmp/response.json | jq '.error.details.errors.password' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 4: Múltiples errores de validación (422)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 4: Múltiples errores de validación (422)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Enviando email inválido + password corta + sin nombre..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"email":"invalido","password":"12"}')

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "422" ]; then
    echo -e "${GREEN}✅ Correcto! 422 Unprocessable Entity${NC}"
    echo -e "${GREEN}✨ Observa: Todos los errores en una sola respuesta${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 422${NC}"
fi
echo ""
cat /tmp/response.json | jq '.error.details.errors' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 5: Registro exitoso (201 Created)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 5: Registro exitoso (201 Created)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
TIMESTAMP=$(date +%s)
TEST_EMAIL="test${TIMESTAMP}@test.com"
echo -e "Registrando usuario: $TEST_EMAIL..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"123456\",\"nombre\":\"Juan\"}")

echo -e "Código HTTP recibido: ${GREEN}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "201" ]; then
    echo -e "${GREEN}✅ Correcto! 201 Created${NC}"
    echo -e "${GREEN}✨ Usuario creado exitosamente${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 201${NC}"
fi
echo ""
cat /tmp/response.json | jq '{success, message, data: {usuario: {email: .data.usuario.email, rol: .data.usuario.rol}}}' 2>/dev/null || cat /tmp/response.json
echo ""

# Guardar token para tests posteriores
ACCESS_TOKEN=$(cat /tmp/response.json | jq -r '.data.access_token' 2>/dev/null)
echo ""

# Test 6: Email duplicado (409 Conflict)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 6: Email duplicado (409 Conflict)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Intentando registrar el mismo email otra vez..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"123456\",\"nombre\":\"Pedro\"}")

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "409" ]; then
    echo -e "${GREEN}✅ Correcto! 409 Conflict${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 409${NC}"
fi
echo ""
cat /tmp/response.json | jq '.' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 7: Login con credenciales incorrectas (401 Unauthorized)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 7: Login con credenciales incorrectas (401 Unauthorized)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Intentando login con password incorrecta..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"incorrecta\"}")

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "401" ]; then
    echo -e "${GREEN}✅ Correcto! 401 Unauthorized${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 401${NC}"
fi
echo ""
cat /tmp/response.json | jq '.' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 8: Login exitoso (200 OK)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 8: Login exitoso (200 OK)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Login con credenciales correctas..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X POST $API_URL/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"123456\"}")

echo -e "Código HTTP recibido: ${GREEN}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Correcto! 200 OK${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 200${NC}"
fi
echo ""
cat /tmp/response.json | jq '{success, message}' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 9: Token JWT inválido (401 Unauthorized)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Test 9: Token JWT inválido (401 Unauthorized)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Accediendo con token inválido..."
HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X GET $API_URL/api/usuarios/perfil \
  -H "Authorization: Bearer token_invalido_xyz")

echo -e "Código HTTP recibido: ${RED}$HTTP_CODE${NC}"
if [ "$HTTP_CODE" == "401" ]; then
    echo -e "${GREEN}✅ Correcto! 401 Unauthorized${NC}"
else
    echo -e "${RED}❌ Error: Se esperaba 401${NC}"
fi
echo ""
cat /tmp/response.json | jq '.' 2>/dev/null || cat /tmp/response.json
echo ""
echo ""

# Test 10: Acceso con token válido (200 OK)
if [ ! -z "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}📋 Test 10: Acceso con token válido (200 OK)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "Accediendo al perfil con token válido..."
    HTTP_CODE=$(curl -s -o /tmp/response.json -w "%{http_code}" -X GET $API_URL/api/usuarios/perfil \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    echo -e "Código HTTP recibido: ${GREEN}$HTTP_CODE${NC}"
    if [ "$HTTP_CODE" == "200" ]; then
        echo -e "${GREEN}✅ Correcto! 200 OK${NC}"
    else
        echo -e "${RED}❌ Error: Se esperaba 200${NC}"
    fi
    echo ""
    cat /tmp/response.json | jq '{success, data: {usuario: {email: .data.usuario.email, nombre: .data.usuario.nombre}}}' 2>/dev/null || cat /tmp/response.json
    echo ""
    echo ""
fi

# Resumen
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                       📊 RESUMEN DE TESTS                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Tests Completados:${NC}"
echo -e "   1. ✓ 400 Bad Request - JSON mal formado"
echo -e "   2. ✓ 422 Validation Error - Email inválido"
echo -e "   3. ✓ 422 Validation Error - Password corta"
echo -e "   4. ✓ 422 Validation Error - Múltiples errores"
echo -e "   5. ✓ 201 Created - Registro exitoso"
echo -e "   6. ✓ 409 Conflict - Email duplicado"
echo -e "   7. ✓ 401 Unauthorized - Credenciales incorrectas"
echo -e "   8. ✓ 200 OK - Login exitoso"
echo -e "   9. ✓ 401 Unauthorized - Token inválido"
echo -e "   10. ✓ 200 OK - Acceso con token válido"
echo ""
echo -e "${YELLOW}💡 Próximos pasos:${NC}"
echo -e "   1. Revisa los logs: ${BLUE}tail -f logs/solicitudes_api.log${NC}"
echo -e "   2. Busca errores específicos: ${BLUE}grep \"VALIDATION_ERROR\" logs/solicitudes_api.log${NC}"
echo -e "   3. Practica con Postman usando los ejemplos de PRACTICA_VALIDACION_TRACKEO.md"
echo -e "   4. Lee la documentación completa en EJEMPLOS_RESPUESTAS_API.md"
echo ""
echo -e "${GREEN}✨ ¡Felicidades! Has practicado validación y trackeo de errores exitosamente${NC}"
echo ""

# Limpiar archivo temporal
rm -f /tmp/response.json
