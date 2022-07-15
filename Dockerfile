FROM python:3.8-slim

RUN mkdir -p /app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /app/
RUN pip install -r req.txt
