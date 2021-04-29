from datetime import datetime
from math import floor


def name(time: datetime):
    hour = time.hour
    minutes = int(floor(time.minute / 10) * 10)

    if minutes == 0:
        minutes = "00"

    emoji = emoji_lookup[hour % 12]

    return f"{emoji}  {hour}:{minutes} UTC"


emoji_lookup = {
    0: '🕛',
    1: '🕐',
    2: '🕑',
    3: '🕒',
    4: '🕓',
    5: '🕔',
    6: '🕕',
    7: '🕖',
    8: '🕗',
    9: '🕘',
    10: '🕙',
    11: '🕚',
}
