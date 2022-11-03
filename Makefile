prod:
	docker-compose -f docker-compose.yaml up --build
migrate:
	docker-compose -f docker-compose.yaml exec web python manage.py migrate
worker:
	docker-compose -f docker-compose.yaml exec web python receive.py
down:
	docker-compose -f docker-compose.yaml down