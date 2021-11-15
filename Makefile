make run:
	uvicorn app.main:app --reload

make docker:
	docker start 59b882a8b571
