import datetime

import pytest

from discord_bot_the_eternal_gem.clock_channel import name_creator


@pytest.mark.parametrize("utc_time,expected_name", [
    ("0:50:55 UTC", "🕛  0:50 UTC"),
    ("00:50:55 UTC", "🕛  0:50 UTC"),
    ("1:10:20 UTC", "🕐  1:10 UTC"),
    ("2:10:20 UTC", "🕑  2:10 UTC"),
    ("3:10:20 UTC", "🕒  3:10 UTC"),
    ("4:10:20 UTC", "🕓  4:10 UTC"),
    ("5:8:20 UTC", "🕔  5:00 UTC"),
    ("6:10:20 UTC", "🕕  6:10 UTC"),
    ("7:10:20 UTC", "🕖  7:10 UTC"),
    ("8:4:20 UTC", "🕗  8:00 UTC"),
    ("9:34:20 UTC", "🕘  9:30 UTC"),
    ("10:45:00 UTC", "🕙  10:40 UTC"),
    ("11:10:20 UTC", "🕚  11:10 UTC"),
    ("12:10:20 UTC", "🕛  12:10 UTC"),
    ("13:10:20 UTC", "🕐  13:10 UTC"),
    ("14:10:20 UTC", "🕑  14:10 UTC"),
    ("15:10:20 UTC", "🕒  15:10 UTC"),
    ("16:10:20 UTC", "🕓  16:10 UTC"),
    ("17:10:20 UTC", "🕔  17:10 UTC"),
    ("18:10:20 UTC", "🕕  18:10 UTC"),
    ("19:10:20 UTC", "🕖  19:10 UTC"),
    ("20:10:20 UTC", "🕗  20:10 UTC"),
    ("21:49:59 UTC", "🕘  21:40 UTC"),
    ("22:50:55 UTC", "🕙  22:50 UTC"),
    ("23:50:55 UTC", "🕚  23:50 UTC"),
])
def test_channel_name_generation(utc_time, expected_name):
    # Given
    current_datetime = datetime.datetime.strptime(utc_time, '%H:%M:%S %Z')

    # When
    name = name_creator.name(current_datetime)

    # Then
    assert name == expected_name
