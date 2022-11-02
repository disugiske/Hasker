prod:
	docker-compose -f docker-compose.yaml up --build
migrate:
	docker-compose -f docker-compose.yaml exec web python manage.py migrate