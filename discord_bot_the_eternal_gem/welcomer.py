import discord
from loguru import logger as log


class Welcomer:
    async def handle_welcome_channel_message(self, message: discord.Message, guest_role_id: int):
        new_nick = await self.generate_nick(message)
        log.info(f"new nick will be {new_nick}.")

        try:
            await self.change_nickname(message, new_nick)
            await self.delete_message(message)
            await self.add_guest_role(guest_role_id, message)
        except Exception as e:
            log.error(e)

    async def add_guest_role(self, guest_role_id, message):
        log.debug("adding guest role...")
        guest_role = next(role for role in message.guild.roles if role.id == guest_role_id)
        await message.author.add_roles(guest_role)
        log.debug("guest role added.")

    async def delete_message(self, message):
        log.debug("deleting message...")
        await message.delete()
        log.debug("message deleted.")

    async def change_nickname(self, message, new_nick):
        log.debug("changing nickname...")
        await message.author.edit(nick=new_nick)
        log.debug("nickname changed.")

    async def generate_nick(self, message: discord.Message):
        log.info(f"\tauthor={message.author.name}")
        discord_name = message.author.name

        log.info(f"\tnick={message.content}")
        osrs_name = message.content

        if len(discord_name) > 25:
            return discord_name

        expected_length = len(discord_name) + len(osrs_name) + 5
        if expected_length > 32:
            return f"{discord_name} [{osrs_name[0:32 - len(discord_name) - 5]}..]"

        return f"{discord_name} [{osrs_name}]"
