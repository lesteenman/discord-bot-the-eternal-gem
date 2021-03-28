run:
	poetry run python discord_bot_the_eternal_gem/app.py

test:
	poetry run pytest .

flake:
	flake8 discord-bot-the-eternal-gem/ tests/

image:
	docker build -t ghcr.io/lesteenman/discord-bot-the-eternal-gem:local .
