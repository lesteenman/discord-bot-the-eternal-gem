import os

from discord_bot_the_eternal_gem.client import TheEternalGemClient
from discord_bot_the_eternal_gem.config import get_discord_token
from discord_bot_the_eternal_gem.message_responder import MessageResponder
from discord_bot_the_eternal_gem.welcomer import Welcomer

message_responder = None
message_responder_config = os.environ.get('MESSAGE_RESPONDER_CONFIG')
if message_responder_config is not None:
    message_responder = MessageResponder.from_file(message_responder_config)

client = TheEternalGemClient(
    welcomer=Welcomer(),
    message_responder=message_responder,
)

guild_id = int(os.environ.get('DISCORD_GUILD', 800097373681746011))
welcome_channel = int(os.environ.get('DISCORD_WELCOME_CHANNEL', 825656911843295283))

if 'DISCORD_GUEST_ROLE' in os.environ:
    guest_roles = [int(os.environ.get('DISCORD_GUEST_ROLE', 825657018428948520))]
else:
    i = 1
    guest_roles = []
    while f"DISCORD_GUEST_ROLE_{i}" in os.environ:
        guest_roles.append(int(os.environ.get(f"DISCORD_GUEST_ROLE_{i}")))
        i = i + 1
    assert len(guest_roles) > 0

client.configure_guild(
    guild_id=guild_id,
    welcome_channel=welcome_channel,
    guest_roles=guest_roles,
)

client.run(get_discord_token())
