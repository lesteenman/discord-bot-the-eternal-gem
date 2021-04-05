import discord
import yaml


class MessageResponder(object):
    def __init__(self, lookup: dict):
        self.lookup = lookup

    async def handle_message(self, channel: discord.TextChannel, message: str):
        if message in self.lookup:
            await channel.send(content=self.lookup.get(message))

    @classmethod
    def from_file(cls, file):
        lookup = {}

        with open(file, 'r') as lookup_file:
            parsed_file = yaml.safe_load(lookup_file)
            for entry in parsed_file['lookup']:
                message = entry['message']
                response = entry['response']
                lookup[message] = response

        return MessageResponder(lookup=lookup)
