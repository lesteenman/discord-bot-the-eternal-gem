import argparse
import os

import discord

from loguru import logger as log

discord_token = os.environ.get('DISCORD_TOKEN')
if discord_token is None:
    with open('.discord-token', 'r') as discord_token_file:
        discord_token = discord_token_file.read()

client = discord.Client()


parser = argparse.ArgumentParser()
parser.add_argument('--guild', dest='guild')
parser.add_argument('--channel', dest='channel')
parser.add_argument('--title', dest='title')
parser.add_argument('message')

args = parser.parse_args()
guild_id = args.guild
channel_id = args.channel
title = args.title
message = args.message

log.info(f"Will send the following message to channel {channel_id} of guild {guild_id}:")
log.info(message)


@client.event
async def on_ready():
    try:
        # guild = await client.fetch_guild(guild_id)
        channel = await client.fetch_channel(channel_id)

        embed = discord.Embed(
            title=title,
            description=message,
            colour=discord.Colour.from_rgb(62, 158, 179),
        )
        await channel.send(embed=embed)

        log.info("Message sent.")
    except Exception as e:
        log.error(e)

    await client.close()


client.run(discord_token)
