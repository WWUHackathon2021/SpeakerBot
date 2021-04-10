import discord
import discord.ext
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv("TOKEN")
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

# bot.run(TOKEN)

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


