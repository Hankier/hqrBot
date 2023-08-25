import discord
import asyncio
import aiohttp
import utils
import logging
import logging.config
import os
import yaml

with open('logging_config.yaml', 'r') as f:
    log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)


logger = logging.getLogger('hqrBotLogger')

cogs = [
    'cogs.ping',
]
headers = {
    'User-Agent': 'hqrBot - simple discord bot for hqr',
}


DC_TOKEN = os.environ['HQR_DISCORD_TOKEN']

intents = discord.Intents(
    message_content=True,
    reactions=True,
    messages=True,
    members=True,
    guilds=True,
    emojis=True,
    bans=True
)


async def startup():
    logger.info('Starting bot...')
    bot = utils.CustomBot(
        activity=discord.Activity(type=discord.ActivityType.watching, name="hqrBot"),
        allowed_mentions=discord.AllowedMentions(replied_user=False),
        command_prefix=utils.CustomBot.get_custom_prefix,
        strip_after_prefix=True,
        case_insensitive=True,
        max_messages=20000,
        intents=intents

    )

    bot.cogs_list = cogs
    for cog in cogs:
        await bot.load_extension(cog)

    async with aiohttp.ClientSession(headers=headers) as session:
        bot.session = session
        await bot.start(DC_TOKEN)

if __name__ == '__main__':
    asyncio.run(startup())
