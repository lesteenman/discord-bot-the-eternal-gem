import discord
import yaml
from loguru import logger as log


class MessageResponder(object):
    def __init__(self, lookup: dict):
        self.lookup = lookup

    async def handle_message(self, channel: discord.TextChannel, message: str, guild_id: int):
        if message.lower() in self.lookup:
            log.info(f"[channel={channel.id}] matched message '{message}', responding in channel")
            messages = self.lookup[message.lower()]
            for message in messages:
                await channel.send(content=message)

    @classmethod
    def from_file(cls, file):
        lookup = {}

        with open(file, 'r') as lookup_file:
            parsed_file = yaml.safe_load(lookup_file)
            for entry in parsed_file['lookup']:
                if 'messages' in entry:
                    messages = [message.lower() for message in entry['messages']]
                else:
                    messages = [entry['message'].lower()]

                if 'responses' in entry:
                    responses = entry['responses']
                else:
                    responses = [entry['response']]

                for message in messages:
                    lookup[message] = responses

        return MessageResponder(lookup=lookup)
