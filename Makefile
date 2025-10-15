.PHONY: help build up down restart logs shell db-init db-seed db-reset test clean

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes Docker
	docker-compose build

up: ## Levantar todos los servicios
	docker-compose up -d

down: ## Detener todos los servicios
	docker-compose down

restart: ## Reiniciar todos los servicios
	docker-compose restart

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-api: ## Ver logs solo de la API
	docker-compose logs -f api

logs-worker: ## Ver logs solo del worker de Celery
	docker-compose logs -f celery-worker

shell: ## Acceder a la shell de Flask
	docker-compose exec api flask shell

bash: ## Acceder al bash del contenedor API
	docker-compose exec api bash

db-init: ## Inicializar la base de datos
	docker-compose exec api python manage.py init-db

db-seed: ## Poblar la base de datos con datos de prueba
	docker-compose exec api python manage.py seed-db

db-reset: ## Resetear la base de datos (CUIDADO: elimina todos los datos)
	docker-compose exec api python manage.py reset-db

db-drop: ## Eliminar todas las tablas
	docker-compose exec api python manage.py drop-db

test: ## Ejecutar tests
	docker-compose exec api pytest

test-api: ## Ejecutar script de prueba de API
	python test_api.py

ps: ## Ver estado de los servicios
	docker-compose ps

clean: ## Limpiar contenedores y volúmenes
	docker-compose down -v
	docker system prune -f

setup: build up db-init db-seed ## Setup completo (build, up, init, seed)
	@echo "✅ Proyecto configurado exitosamente!"
	@echo "La API está disponible en http://localhost:5000"
	@echo "El panel de admin está en http://localhost:5000/admin"

dev: ## Modo desarrollo (reconstruir y levantar)
	docker-compose up --build

stop: ## Detener servicios sin eliminarlos
	docker-compose stop

start: ## Iniciar servicios detenidos
	docker-compose start
