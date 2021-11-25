# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /crud_fastapi

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python3", "-m", "--host=0.0.0.0", "uvicorn", "--reload", "app.main:app"]
