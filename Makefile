prod:
	docker-compose up -d
	timeout 10
	cd source
	python manage.py migrate
	python manage.py runserver
	python hasite/tasks/receive.py