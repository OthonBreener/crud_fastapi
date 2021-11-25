# syntax=docker/dockerfile:1

FROM python:3.8-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /api

EXPOSE 8000

COPY . .

CMD ["make", "run"]
