APP_LIST ?= pages tools users main blog
.PHONY: collectstatic run test ci install install-dev migrations staticfiles

help:
	@echo "Available commands"
	@echo " - ci               : lints, migrations, tests, coverage"
	@echo " - install          : installs production requirements"
	@echo " - isort            : sorts all imports of the project"
	@echo " - lint             : lints the codebase"
	@echo " - runserver              : runs the development server"
	@echo " - shellplus        : runs the development shell"

collectstatic:
	python manage.py collectstatic --noinput

clean:
	echo "this command paste directly in terminal via make it doesn't work"
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy

install:
	uv sync

setup_test_data:
	python manage.py setup_test_data

shellplus:
	python manage.py shell_plus --print-sql

shell:
	python manage.py shell

showmigrations:
	python manage.py showmigrations

makemigrations:
	python manage.py makemigrations

makemessages:
	django-admin makemessages --all

compilemessages:
	django-admin compilemessages

migrate:
	python manage.py migrate

migrations-check:
	python manage.py makemigrations --check --dry-run

runserver:
	python manage.py runserver

build: install makemigrations migrate runserver

format:
	ruff check --select I --fix
	ruff format .
	djlint --reformat .

lint:
	ruff check .
	djlint --lint .
	djlint --check .

test: check migrations-check
	coverage run --source='.' manage.py test
	coverage html

security:
	bandit -r .
	safety check

ci: format lint security test

superuser:
	python manage.py createsuperuser

status:
	@echo "Nginx"
	@sudo systemctl status nginx

	@echo "Gunicorn Socket"
	@sudo systemctl status tools.socket

	@echo "Gunicorn Service"
	@sudo systemctl status tools.service


reload:
	@echo "reloading daemon..."
	@sudo systemctl daemon-reload

	@echo "🔌 restarting gunicorn socket..."
	@sudo systemctl restart tools.socket

	@echo "🦄 restarting gunicorn service..."
	@sudo systemctl restart tools.service

	@echo "⚙️ reloading nginx..."
	@sudo nginx -s reload

	@echo "All done! 💅💫💖"

logs:
	@sudo journalctl -fu tools.service
