import os

from discord_bot_the_eternal_gem.client import TheEternalGemClient

discord_token = os.environ.get('DISCORD_TOKEN')
if discord_token is None:
    with open('.discord-token', 'r') as discord_token_file:
        discord_token = discord_token_file.read()

client = TheEternalGemClient()
client.configure_guild(guild_id=800097373681746011,
                       welcome_channel=825656911843295283,
                       guest_role=825657018428948520)

client.run(discord_token)
