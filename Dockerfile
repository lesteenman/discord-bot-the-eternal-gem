FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi

COPY discord_bot_the_eternal_gem discord_bot_the_eternal_gem
RUN poetry install --no-interaction --no-ansi

CMD ["python", "discord_bot_the_eternal_gem/app.py"]
