import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

bot = commands.Bot(command_prefix='!')
arr = []
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)

@bot.command()
async def play(ctx, url: str):
    vc = discord.utils.get(ctx.guild.voice_channels, name="CF 416")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await vc.connect()

# @bot.command()
# async def join(ctx, url: str):
#     vc = discord.utils.get(ctx.guild.voice_channels, name="CF 416")
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     await vc.connect()

@bot.command(name = 'testing')
async def test(ctx):
    test_quote = [
        'David',
        'Clothesline',
        'David noooo do not pull the trigger'
    ]
    response = random.choice(test_quote)
    await ctx.send(response)

# bot.add_command(test)

@bot.command(name = 'add')
async def test(ctx, arg):
    arr.append(arg)

@bot.command(name = "show")
async def test(ctx):
    await ctx.send(arr)

@bot.command(name = 'delete')
async def test(ctx, arg):
    arr.remove(arg)

bot.run(TOKEN)


