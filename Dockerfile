FROM python:3.8-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml pyproject.toml
RUN
