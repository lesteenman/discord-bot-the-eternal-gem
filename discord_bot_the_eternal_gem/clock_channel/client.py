import discord
from loguru import logger as log


class ClockChannelClient(discord.Client):
    async def on_ready(self):
        log.info(f"We have logged in as {self.user}")
