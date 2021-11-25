make run:
	uvicorn app.main:app --reload --port=8005 --host=0.0.0.0

make docker:
	docker-compose up -d --build

make down:
	docker-compose down

make logs:
	docker-compose logs
