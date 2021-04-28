import os


def get_discord_token():
    discord_token = os.environ.get('DISCORD_TOKEN')
    if discord_token is None:
        with open('.discord-token', 'r') as discord_token_file:
            return discord_token_file.read()

    return discord_token
