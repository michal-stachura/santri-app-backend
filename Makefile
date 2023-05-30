migrations:
	sudo docker-compose -p sapp -f local.yml run --rm django python manage.py makemigrations

migrate:
	sudo docker-compose -p sapp -f local.yml run --rm django python manage.py migrate

run:
	sudo docker-compose -p sapp -f local.yml up

build:
	sudo docker-compose -p sapp -f local.yml build

test:
	sudo docker-compose -p sapp -f local.yml run --rm django pytest -x

shell:
	sudo docker-compose -p sapp -f local.yml run --rm django python manage.py shell

cleardocker:
	sudo docker-compose -p sapp -f local.yml down --volumes --remove-orphans --rmi all

pgbash:
	sudo docker exec -it santri_app_local_postgres /bin/bash

bash:
	sudo docker exec -it santri_app_local_django /bin/bash

seed:
	docker-compose -p sapp -f local.yml build; \
	docker-compose -p sapp -f local.yml run --rm django python manage.py migrate; \
	docker-compose -p sapp -f local.yml run --rm django python manage.py shell < santri_app/utils/seed.py
