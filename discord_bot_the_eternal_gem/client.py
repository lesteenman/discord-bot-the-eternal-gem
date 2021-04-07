import discord
from loguru import logger as log

from discord_bot_the_eternal_gem.message_responder import MessageResponder


class TheEternalGemClient(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.guild_configs = {}

    def configure_guild(self, guild_id: int, welcome_channel: int = None,
                        guest_role: int = None, message_responder: MessageResponder = None):
        if guild_id not in self.guild_configs:
            self.guild_configs[guild_id] = {}

        if welcome_channel is not None:
            self.guild_configs[guild_id]['welcome_channel'] = int(welcome_channel)

        if guest_role is not None:
            self.guild_configs[guild_id]['guest_role'] = int(guest_role)

        if message_responder is not None:
            self.guild_configs[guild_id]['message_responder'] = message_responder

    async def on_ready(self):
        log.info(f"We have logged in as {self.user}")
        log.info("Guild configs:")
        for guild_id, guild_config in self.guild_configs.items():
            log.info(f"{guild_id} => {guild_config}")

    async def on_message(self, message):
        for guild_id, guild_config in self.guild_configs.items():
            if guild_config.get('welcome_channel', -1) == message.channel.id:
                log.info(f"welcome message found for guild {guild_id}.")
                await self.handle_welcome_channel_message(guild_config, message)
            elif guild_config.get('message_responder', None) is not None:
                message_responder = guild_config.get('message_responder', None)
                await message_responder.handle_message(
                    channel=message.channel,
                    message=message.content,
                )

    async def handle_welcome_channel_message(self, guild_config, message):
        log.info(f"\tauthor={message.author.name}")
        log.info(f"\tnick={message.content}")
        discord_name = message.author.name
        osrs_name = message.content
        new_nick = await self.generate_nick(discord_name, osrs_name)
        log.info(f"new nick will be {new_nick}.")
        try:
            log.debug("changing nickname...")
            await message.author.edit(nick=new_nick)
            log.debug("nickname changed.")

            log.debug("deleting message...")
            await message.delete()
            log.debug("message deleted.")

            log.debug("adding guest role...")
            guest_role = next(role for role in message.guild.roles if role.id == guild_config['guest_role'])
            await message.author.add_roles(guest_role)
            log.debug("guest role added.")
        except Exception as e:
            log.error(e)

    async def generate_nick(self, discord_name, osrs_name):
        if len(discord_name) > 25:
            return discord_name

        expected_length = len(discord_name) + len(osrs_name) + 5
        if expected_length > 32:
            return f"{discord_name} [{osrs_name[0:32 - len(discord_name) - 5]}..]"

        return f"{discord_name} [{osrs_name}]"
