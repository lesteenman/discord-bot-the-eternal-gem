from argparse import ArgumentParser

from loguru import logger as log

from discord_bot_the_eternal_gem.clock_channel.client import ClockChannelClient

MODE_CLOCK_CHANNEL = 'clock-channel'


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('mode', choices=[MODE_CLOCK_CHANNEL])
    arg_parser.add_argument('--discord-token', dest='discord_token', required=True)
    arg_parser.add_argument('--clock-channel', dest='clock_channel_id', required=True)

    arguments = arg_parser.parse_args()

    if arguments.mode == MODE_CLOCK_CHANNEL:
        start_clock_channel(arguments)


def start_clock_channel(arguments):
    log.info("starting clock channel")
    log.info(f"arguments={arguments}")
    client = ClockChannelClient(
        clock_channel_id=arguments.clock_channel_id,
    )

    client.run(arguments.discord_token)


if __name__ == '__main__':
    main()
