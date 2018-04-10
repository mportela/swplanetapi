build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker stop swplanetapi_web_1 swplanetapi_mongodb_1

test:
	docker-compose run --rm web python test.py

weblogs:
	docker logs -f swplanetapi_web_1

