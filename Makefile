TEST_DISCORD_TOKEN=`cat .discord-token`
TEST_CLOCK_CHANNEL=`cat .clock-channel-id`

run:
	poetry run python discord_bot_the_eternal_gem/run.py

run-clock:
	poetry run python discord_bot_the_eternal_gem/run.py clock-channel --discord-token $(TEST_DISCORD_TOKEN) \
		--clock-channel $(TEST_CLOCK_CHANNEL)

test:
	poetry run pytest .

lint:
	poetry run flake8 discord_bot_the_eternal_gem/ tests/

image:
	docker build -t ghcr.io/lesteenman/discord-bot-the-eternal-gem .

push: image
	docker push ghcr.io/lesteenman/discord-bot-the-eternal-gem:latest
