setup:
	make build
	make mm
	make m
	make fixture
	make down
	make up

build:
	sudo docker-compose -f docker-compose.yml up -d --build

up:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

down_v:
	docker-compose -f docker-compose.yml down -v

mm:
	docker exec -it student_management_system python manage.py makemigrations

m:
	docker exec -it student_management_system python manage.py migrate

dd:
	docker exec -t student_management_system_db  pg_dump -c -U student_management_system -d student_management_system > student_management_system_dump_data_2024_12_12.sql

dr:
	cat student_management_system_dump_data_2024_12_12.sql | sudo docker exec -i precious_db psql -U student_management_system

rweb:
	docker restart student_management_system

ir:
	docker exec -it student_management_system pip install -r requirements.txt

csu:
	docker exec -it student_management_system python manage.py createsuperuser

lw:
	docker logs student_management_system -f

ln:
	docker logs student_management_system_nginx -f

cs:
	docker exec -it student_management_system python manage.py collectstatic --noinput

shell:
	docker exec -it student_management_system python manage.py shell

pylint:
	DJANGO_SETTINGS_MODULE=core.settings pylint --load-plugins=pylint_django .

docker_loc:
	docker exec -it student_management_system python manage.py makemessages -l ne

docker_loc_c:
	docker exec -it student_management_system python manage.py compilemessages -l ne

loc:
	python3 manage.py makemessages -l ne

loc_c:
	python3 manage.py compilemessages -l ne

fixture:
	docker exec -it student_management_system python manage.py loaddata groups