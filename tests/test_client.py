from abc import ABC
from unittest.mock import PropertyMock, patch, AsyncMock

import discord
import pytest

import discord_bot_the_eternal_gem
from discord_bot_the_eternal_gem.client import TheEternalGemClient
from discord_bot_the_eternal_gem.message_responder import MessageResponder

pytestmark = pytest.mark.asyncio


class FakeRole:
    def __init__(self, id):
        self.id = id


class FakeGuild:
    def __init__(self, roles):
        self.roles = roles


class FakeMessage(discord.Message):
    def __init__(self, channel, content, author, guild): # noqa
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


# A discord username must be at most 32 characters long.
@pytest.mark.parametrize('discord_name,osrs_name,expected_nick', [
    # If we stay within 32 characters, the whole nickname and whole osrs username will be added.
    ('Awesome Dude', 'EG AwesomeDude', 'Awesome Dude [EG AwesomeDude]'),
    # We only add the osrs name if there will be at least enough for 2 characters plus 2 ellipses.
    ('This username is already 32 long', 'EG AwesomeDude', 'This username is already 32 long'),
    ('26 chrs is too much to add', 'EG AwesomeDude', '26 chrs is too much to add'),
    ('But 25 chars is just fine', 'EG AwesomeDude', 'But 25 chars is just fine [EG..]'),
])
@patch.object(discord_bot_the_eternal_gem.client, 'discord')
async def test_message_in_welcome_channel_changes_nick(mock_discord, discord_name, osrs_name, expected_nick):
    # Given
    guild_id = 10
    welcome_channel_id = 100

    guest_role_id = 300
    guest_role = FakeRole(id=guest_role_id)

    fake_guild = FakeGuild(roles=[guest_role])

    client = TheEternalGemClient()
    client.configure_guild(guild_id, welcome_channel=welcome_channel_id, guest_role=guest_role_id)

    mock_user = make_mock_user(discord_name)
    message = FakeMessage(channel=FakeChannel(welcome_channel_id), content=osrs_name, author=mock_user,
                          guild=fake_guild)

    # When
    await client.on_message(message)

    # Then
    mock_user.edit.assert_called_with(nick=expected_nick)
    mock_user.add_roles.assert_called_with(guest_role)
    assert message.deleted


async def test_message_responder():
    # Given
    client = TheEternalGemClient()
    guild_id = 10

    message_responder = AsyncMock(MessageResponder)

    client.configure_guild(guild_id, message_responder=message_responder)
    fake_channel = FakeChannel(channel_id=10)

    # When
    message = FakeMessage(
        content="Hello team!",
        channel=fake_channel,
        author=make_mock_user("user1"),
        guild=FakeGuild(roles=[]))
    await client.on_message(message)

    # Then
    message_responder.handle_message.assert_called_with(message="Hello team!", channel=fake_channel)


def make_mock_user(discord_name: str = "discord-name"):
    mock_user = AsyncMock(discord.Member, autospec=True)
    type(mock_user).name = PropertyMock(return_value=discord_name)
    return mock_user
