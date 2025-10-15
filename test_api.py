#!/usr/bin/env python3
"""Script de prueba para la API de Solicitudes"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def login(email, password):
    """Login y obtener token"""
    print(f"\n🔐 Login como: {email}")
    response = requests.post(f"{BASE_URL}/usuarios/login", json={"email": email, "password": password})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login exitoso! Usuario: {data['usuario']['nombre']}")
        return data['access_token']
    else:
        print(f"❌ Error en login")
        return None

def listar_usuarios(token):
    """Listar todos los usuarios"""
    print("\n" + "="*80)
    print("📋 LISTANDO USUARIOS")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/usuarios/usuarios", headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n👥 Total: {data['total']} usuarios\n")
        print(f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Rol':<15} {'Estado'}")
        print("-"*80)
        
        for u in data['usuarios']:
            estado = "✅" if u['activo'] else "❌"
            print(f"{u['id']:<5} {u['nombre']:<20} {u['email']:<30} {u['rol']:<15} {estado}")
        
        return data['usuarios']
    else:
        print(f"❌ Error: {response.json().get('error', 'Error desconocido')}")
        return []

def crear_usuario(token, email, password, nombre, apellido, rol="empleado"):
    """Crear nuevo usuario"""
    print(f"\n➕ Creando usuario: {nombre} {apellido} ({email})")
    
    response = requests.post(
        f"{BASE_URL}/usuarios/registro",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"email": email, "password": password, "nombre": nombre, "apellido": apellido, "rol": rol}
    )
    
    if response.status_code == 201:
        usuario = response.json()['usuario']
        print(f"✅ Usuario creado con ID: {usuario['id']}")
        return usuario
    else:
        print(f"❌ Error: {response.json().get('error', 'Error desconocido')}")
        return None

def main():
    print("="*80)
    print("  🚀 PRUEBA DE API - Sistema de Solicitudes")
    print("="*80)
    
    # Login
    token = login("admin@solicitudes.com", "admin123")
    if not token:
        return
    
    # Listar usuarios
    listar_usuarios(token)
    
    # Crear usuario de prueba
    timestamp = datetime.now().strftime('%H%M%S')
    nuevo = crear_usuario(token, f"test.{timestamp}@test.com", "test123", "Test", f"User{timestamp}", "empleado")
    
    # Listar de nuevo
    if nuevo:
        print("\n" + "="*80)
        print("📊 LISTADO ACTUALIZADO")
        print("="*80)
        listar_usuarios(token)
    
    print("\n✅ Prueba completada!\n")

if __name__ == "__main__":
    main()
