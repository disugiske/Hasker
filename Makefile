prod:
	docker-compose -f docker-compose.yaml up --build
	docker-compose -f docker-compose.yaml exec web python receive.py
migrate:
	docker-compose -f docker-compose.yaml exec web python manage.py migrate