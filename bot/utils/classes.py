import discord
import os
import logging
import requests

from discord.ext import commands

from typing import List

__all__ = [
    'CustomBot',
]

logger = logging.getLogger('hqrBotLogger')

GUILD_ID = 1141415448425009273
ADMIN_IDS = [453871191162224643]

class API():
    def __init__(self):
        self.url = os.getenv('HQR_APP_API_URL')
        self.key = os.getenv('HQR_APP_API_KEY')

    def test(self):
        api_endpoint = 'api/test/'
        url = f'{self.url}{api_endpoint}'
        headers = {'Authorization': f'Api-Key {self.key}'}
        response = requests.post(url, headers=headers)
        return response


class CustomBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cogs_list: List[str] = []
        self.fully_ready = False
        self.synced = False
        self.guild = None
        self.owner_ids = set([int(idx) for idx in ADMIN_IDS])
        self.api = API()
        logger.debug('CustomBot initialized.')

    @staticmethod
    def get_custom_prefix(_bot: 'CustomBot', message: discord.Message):
        logger.debug('Getting prefix for message')
        default_prefixes = ['!', 'hqr.', 'hqr ']

        return commands.when_mentioned_or(*default_prefixes)(_bot, message)

    async def setup_hook(self):
        self.loop.create_task(self.startup())

    async def on_ready(self):
        logger.info('Logged in as %s (ID: %s)', self.user, self.user.id)

        await self.wait_until_ready()
        self.guild = self.get_guild(GUILD_ID)
        logger.debug('Guild: %s', self.guild)

        logger.info('Bot is ready.')
        if not self.synced:
            logger.debug('Syncing slash commands...')
            synced = await self.tree.sync()
            logger.debug(f'Synced {len(synced)} command(s) {synced}')
            self.synced = True

    async def on_message(self, message: discord.Message):
        logger.debug('On message invoked')
        if not self.fully_ready:
            logger.debug('Bot is not fully ready. Waiting for fully_ready event...')
            await self.wait_for('fully_ready')

        if message.author.bot:
            logger.debug('Ignoring bot message.')
            return
        elif message.guild is None:
            logger.debug('Ignoring DM message.')
            return
        elif message.guild.id == GUILD_ID:
            logger.debug('Processing commands...')
            await self.process_commands(message)
        else:
            logger.debug('Ignoring message from other guild. %s(%s)', message.guild, message.guild.id)

    async def startup(self):
        await self.wait_until_ready()

        self.fully_ready = True
        self.dispatch('fully_ready')
        logger.info('Bot is fully ready.')

    async def close(self):
        await super().close()

    async def get_owner(self) -> discord.User:
        if not self.owner_id and not self.owner_ids:
            info = await self.application_info()
            self.owner_id = info.owner.id

        return await self.fetch_user(self.owner_id or list(self.owner_ids)[0])
