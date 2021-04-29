import asyncio
import datetime

import discord
from loguru import logger as log

from discord_bot_the_eternal_gem.clock_channel import name_creator


class ClockChannelClient(discord.Client):
    def __init__(self, clock_channel_id: int, **options):
        super().__init__(**options)
        self.clock_channel_id = clock_channel_id
        self.exit_gracefully = False

    async def on_ready(self):
        log.info(f"We have logged in as {self.user}")

        await self.update_loop()
        await self.close()

    async def update_loop(self):
        while not self.exit_gracefully:
            await self.wait_until_next_update_time()
            await self.update_channel_name()

    async def wait_until_next_update_time(self):
        sleep_time = 30
        log.info(f"sleeping for {sleep_time} seconds")
        await asyncio.sleep(sleep_time)

    async def update_channel_name(self):
        channel = await self.fetch_channel(self.clock_channel_id)

        time = datetime.datetime.utcnow()
        name = name_creator.name(time)

        if name == channel.name:
            log.info(f"Name is still '{name}', not updating.")
            return

        log.info(f"updating channel name from {channel.name} to {name}")
        await channel.edit(name=name)
