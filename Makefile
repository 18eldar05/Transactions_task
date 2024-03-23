up:
#	poetry install
	docker compose up -d
	python3 manage.py migrate
	gunicorn --reload -b coolsite.wsgi