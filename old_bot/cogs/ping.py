import discord
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count_ping = 0

    @commands.command()
    async def ping(self, ctx):
        print('Ping command received')
        self.count_ping += 1
        await ctx.send(f'Pong! {self.count_ping}')


async def setup(bot):
    await bot.add_cog(PingCog(bot))
