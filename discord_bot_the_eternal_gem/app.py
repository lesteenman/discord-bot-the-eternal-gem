import os

from discord_bot_the_eternal_gem.client import TheEternalGemClient
from discord_bot_the_eternal_gem.message_responder import MessageResponder

discord_token = os.environ.get('DISCORD_TOKEN')
if discord_token is None:
    with open('.discord-token', 'r') as discord_token_file:
        discord_token = discord_token_file.read()

message_responder = None
message_responder_config = os.environ.get('MESSAGE_RESPONDER_CONFIG')
if message_responder_config is not None:
    message_responder = MessageResponder.from_file(message_responder_config)

client = TheEternalGemClient()
client.configure_guild(guild_id=os.environ.get('DISCORD_GUILD', 800097373681746011),
                       welcome_channel=os.environ.get('DISCORD_WELCOME_CHANNEL', 825656911843295283),
                       guest_role=os.environ.get('DISCORD_GUEST_ROLE', 825657018428948520),
                       message_responder=message_responder)

client.run(discord_token)
