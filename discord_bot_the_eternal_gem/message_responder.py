import discord
import yaml
from loguru import logger as log


class MessageResponder(object):
    def __init__(self, lookup: dict):
        self.lookup = lookup

    async def handle_message(self, channel: discord.TextChannel, message: str, guild_id: int):
        if message.lower() in self.lookup:
            log.info(f"[channel={channel.id}] matched message '{message}', responding in channel")
            await channel.send(content=self.lookup.get(message.lower()))

    @classmethod
    def from_file(cls, file):
        lookup = {}

        with open(file, 'r') as lookup_file:
            parsed_file = yaml.safe_load(lookup_file)
            for entry in parsed_file['lookup']:
                message = entry['message'].lower()
                response = entry['response']
                lookup[message] = response

        return MessageResponder(lookup=lookup)
