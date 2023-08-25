import asyncio
import utils
import discord
import os

#import token
DC_TOKEN = os.environ.get('HQR_DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

cogs = ['cogs.ping']

async def setup():
    bot = utils.CustomBot(command_prefix='!', intents=intents)

    for cog in cogs:
        await bot.load_extension(cog)

    await bot.start(DC_TOKEN)

if __name__ == '__main__':
    asyncio.run(setup())


