import discord
from discord.ext import commands
import os

DC_TOKEN = os.environ.get('HQR_DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(DC_TOKEN)
