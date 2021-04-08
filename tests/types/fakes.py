from abc import ABC

import discord


class FakeRole:
    def __init__(self, id):
        self.id = id


class FakeGuild:
    def __init__(self, id: int, roles):
        self.id = id
        self.roles = roles


class FakeMessage(discord.Message):
    def __init__(self, channel=None, content=None, author=None, guild=None): # noqa
        self.channel = channel
        self.content = content
        self.author = author
        self.deleted = False
        self.guild = guild

    async def delete(self): # noqa
        self.deleted = True


class FakeChannel(discord.abc.GuildChannel, ABC):
    def __init__(self, channel_id: int):
        self.id = channel_id
