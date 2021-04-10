import discord
import discord.ext
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

client = commands.Bot(command_prefix='!')

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@client.command()
async def play(ctx, url: str):
    vc = discord.utils.get(ctx.guild.voice_channels, name="CF 416")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await vc.connect()

# @client.command()
# async def join(ctx, url: str):
#     vc = discord.utils.get(ctx.guild.voice_channels, name="CF 416")
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     await vc.connect()

client.run(TOKEN)
