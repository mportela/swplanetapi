build:
	docker-compose build

run:
	docker-compose up -d

test:
	docker-compose run --rm web python test.py
