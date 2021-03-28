import discord
from loguru import logger as log


class TheEternalGemClient(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.guild_configs = {}

    def configure_guild(self, guild_id: int, welcome_channel: int = None, guest_role: int = None):
        if guild_id not in self.guild_configs:
            self.guild_configs[guild_id] = {}

        if welcome_channel is not None:
            self.guild_configs[guild_id]['welcome_channel'] = welcome_channel

        if guest_role is not None:
            self.guild_configs[guild_id]['guest_role'] = guest_role

    async def on_ready(self):
        log.info(f"We have logged in as {self.user}")

    async def on_message(self, message):
        log.debug(f"on_message for {message.content}")

        for guild_id, guild_config in self.guild_configs.items():
            if guild_config['welcome_channel'] == message.channel.id:
                log.info(f"welcome message found for guild {guild_id}.")
                log.info(f"\tauthor={message.author.name}")
                log.info(f"\tnick={message.content}")

                discord_name = message.author.name
                osrs_name = message.content
                new_nick = await self.generate_nick(discord_name, osrs_name)
                await message.author.edit(nick=new_nick)
                await message.delete()

                guest_role = next(role for role in message.guild.roles if role.id == guild_config['guest_role'])
                await message.author.add_roles(guest_role)

    async def generate_nick(self, discord_name, osrs_name):
        if len(discord_name) > 25:
            return discord_name

        expected_length = len(discord_name) + len(osrs_name) + 5
        if expected_length > 32:
            return f"{discord_name} [{osrs_name[0:32 - len(discord_name) - 5]}..]"

        return f"{discord_name} [{osrs_name}]"
