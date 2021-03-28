run:
	poetry run python discord_bot_the_eternal_gem/app.py

test:
	poetry run pytest .

lint:
	poetry run flake8 discord_bot_the_eternal_gem/ tests/

image:
	docker build -t ghcr.io/lesteenman/discord-bot-the-eternal-gem:local .
