import discord
from discord.ext import commands

__all__ = ['CustomBot']


GUILD_ID = 1141415448425009273

class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = None

    async def on_ready(self):
            print('hqrBot started as ', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            print("Message from self")
            return
        if message.guild is None:
            print("Message from private channel")
            return
        if message.guild.id != GUILD_ID:
            print("Message from unknown guild")
            return


        await self.process_commands(message)
