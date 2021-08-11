from unittest.mock import PropertyMock, AsyncMock, patch

import discord
import pytest

from discord_bot_the_eternal_gem.client import TheEternalGemClient
from discord_bot_the_eternal_gem.message_responder import MessageResponder
from discord_bot_the_eternal_gem.welcomer import Welcomer
from tests.types.fakes import FakeChannel, FakeMessage, FakeGuild

pytestmark = pytest.mark.asyncio


@patch.object(TheEternalGemClient, 'user', new_callable=PropertyMock)
@pytest.mark.parametrize("welcome_channel_id,message_channel_id,is_welcome_message", [
    (10, 10, True),
    (10, 11, False),
])
async def test_welcomer(mock_client_user, welcome_channel_id: int, message_channel_id: int, is_welcome_message: bool):
    # Given
    welcomer = AsyncMock(Welcomer)
    client = TheEternalGemClient(
        welcomer=welcomer,
        message_responder=AsyncMock(MessageResponder),
    )

    guest_role_id_1 = 100
    guest_role_id_2 = 101
    guild_id = 10

    client.configure_guild(
        guild_id=guild_id,
        welcome_channel=welcome_channel_id,
        guest_roles=[guest_role_id_1, guest_role_id_2]
    )

    mock_client_user.return_value = make_mock_user(user_id=100)

    # When
    message = FakeMessage(
        content="Hello team!",
        channel=FakeChannel(channel_id=message_channel_id),
        author=make_mock_user("user1", user_id=150),
        guild=FakeGuild(id=guild_id, roles=[])
    )

    await client.on_message(message)

    # Then
    if is_welcome_message:
        welcomer.handle_welcome_channel_message.assert_called()
        args = welcomer.handle_welcome_channel_message.call_args[1]
        assert args['message'].content == message.content
        assert len(args['guest_role_ids']) == 2
        assert guest_role_id_1 in args['guest_role_ids']
        assert guest_role_id_2 in args['guest_role_ids']
    else:
        welcomer.handle_welcome_channel_message.assert_not_called()


@patch.object(TheEternalGemClient, 'user', new_callable=PropertyMock)
@pytest.mark.parametrize("guild_id,message_guild_id,is_guild_message", [
    (50, 50, True),
    (50, 60, False),
])
async def test_message_responder(mock_client_user, guild_id: int, message_guild_id: int, is_guild_message: bool):
    # Given
    message_responder = AsyncMock(MessageResponder)

    client = TheEternalGemClient(
        welcomer=AsyncMock(Welcomer),
        message_responder=message_responder,
    )

    welcome_channel = 20
    other_channel = 21

    client.configure_guild(
        guild_id=guild_id,
        welcome_channel=welcome_channel
    )
    fake_channel = FakeChannel(channel_id=other_channel)

    mock_client_user.return_value = make_mock_user(user_id=100)

    # When
    message = FakeMessage(
        content="Hello team!",
        channel=fake_channel,
        author=make_mock_user("user1", user_id=150),
        guild=FakeGuild(id=message_guild_id, roles=[]))

    await client.on_message(message)

    # Then
    if is_guild_message:
        message_responder.handle_message.assert_called_with(
            guild_id=guild_id,
            message="Hello team!",
            channel=fake_channel
        )
    else:
        message_responder.handle_message.assert_not_called()


@patch.object(TheEternalGemClient, 'user', new_callable=PropertyMock)
async def test_message_responder_of_own_message(mock_client_user):
    # Given
    bot_id = 100
    guild_id = 10

    message_responder = AsyncMock(MessageResponder)

    client = TheEternalGemClient(
        welcomer=AsyncMock(Welcomer),
        message_responder=message_responder,
    )

    welcome_channel = 20
    other_channel = 21

    client.configure_guild(guild_id, welcome_channel=welcome_channel)
    fake_channel = FakeChannel(channel_id=other_channel)

    # And the message is sent by the bot's user
    mock_client_user.return_value = make_mock_user(user_id=bot_id)
    message = FakeMessage(
        content="Hello team!",
        channel=fake_channel,
        author=make_mock_user(user_id=bot_id),
        guild=FakeGuild(id=guild_id, roles=[]))

    # When
    await client.on_message(message)

    # Then
    message_responder.handle_message.assert_not_called()


def make_mock_user(discord_name: str = "discord-name", user_id: int = -1):
    mock_user = AsyncMock(discord.Member, autospec=True)
    type(mock_user).name = PropertyMock(return_value=discord_name)
    type(mock_user).id = PropertyMock(return_value=user_id)
    return mock_user
