# A discord username must be at most 32 characters long.
from unittest.mock import patch

import pytest

import discord_bot_the_eternal_gem
from discord_bot_the_eternal_gem.welcomer import Welcomer
from tests.test_client import make_mock_user
from tests.types.fakes import FakeGuild, FakeRole, FakeMessage

pytestmark = pytest.mark.asyncio


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
    guest_role_id = 300
    guest_role = FakeRole(id=guest_role_id)

    fake_guild = FakeGuild(id=-1, roles=[guest_role])

    welcomer = Welcomer()

    mock_user = make_mock_user(discord_name)
    message = FakeMessage(content=osrs_name, author=mock_user,
                          guild=fake_guild)

    # When
    await welcomer.handle_welcome_channel_message(message=message, guest_role_id=guest_role_id)

    # Then
    mock_user.edit.assert_called_with(nick=expected_nick)
    mock_user.add_roles.assert_called_with(guest_role)
    assert message.deleted
