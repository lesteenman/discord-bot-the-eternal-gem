import os
import pathlib
from unittest.mock import AsyncMock, call

import discord
import pytest

from discord_bot_the_eternal_gem.message_responder import MessageResponder

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("message", ['Eternal Gem', 'eternal gem', 'eternal Gem'])
async def test_handle_matching_message(message: str):
    # Given
    lookup = {
        'eternal gem': ['The most awesome bot ever!'],
    }
    message_responder = MessageResponder(lookup)

    channel = AsyncMock(discord.TextChannel, autospec=True)

    # When
    await message_responder.handle_message(guild_id=-1,
                                           channel=channel,
                                           message=message)

    # Then
    channel.send.assert_called_with(content='The most awesome bot ever!')


async def test_handle_nonmatching_message():
    # Given
    lookup = {
        'eternal gem': ['The most awesome bot ever!'],
    }
    message_responder = MessageResponder(lookup)

    channel = AsyncMock(discord.TextChannel, autospec=True)

    # When
    await message_responder.handle_message(guild_id=-1,
                                           channel=channel,
                                           message='Something else')

    # Then
    channel.send.assert_not_called()


async def test_handle_multiple_responses():
    # Given
    lookup = {
        'eternal gem': [
            'The most awesome bot ever!',
            'There is none like it!'
        ],
    }
    message_responder = MessageResponder(lookup)

    channel = AsyncMock(discord.TextChannel, autospec=True)

    # When
    await message_responder.handle_message(guild_id=-1,
                                           channel=channel,
                                           message='eternal gem')

    # Then
    channel.send.assert_has_calls([
        call(content='The most awesome bot ever!'),
        call(content='There is none like it!'),
    ])


def test_initialize_from_file():
    # Given
    file = os.path.join(pathlib.Path(__file__).parent.absolute(),
                        'data',
                        'message_lookup.yml')

    # When
    message_responder = MessageResponder.from_file(file)

    # Then
    assert message_responder.lookup == {
        'the eternal gem': ['The most awesome bot ever!'],
        'good bot': ['Thank you!'],
        'great bot': ['Thank you!'],
        'bad bot': ["You know what?", "I don't like you either."],
    }
