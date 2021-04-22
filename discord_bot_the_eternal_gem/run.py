from argparse import ArgumentParser

from discord_bot_the_eternal_gem.clock_channel.client import ClockChannelClient
from discord_bot_the_eternal_gem.config import get_discord_token

from loguru import logger as log

MODE_CLOCK_CHANNEL = 'clock-channel'


def start_clock_channel(arguments):
    log.info("starting clock channel")
    log.info(f"arguments={arguments}")
    client = ClockChannelClient()

    client.run(get_discord_token())


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('mode', choices=[MODE_CLOCK_CHANNEL])

    arguments = arg_parser.parse_args()

    if arguments.mode == MODE_CLOCK_CHANNEL:
        start_clock_channel(arguments)
