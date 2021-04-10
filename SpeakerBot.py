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
# @bot.event
# async def on_ready():
#    print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#     await bot.process_commands(message)

@bot.command(name = 'join')
async def join(ctx,arg):
    # connected = ctx.author.voice.channel
    # await connected.connect()
    vc = discord.utils.get(ctx.guild.voice_channels, name=arg)
    print(vc)
    await vc.connect()

@bot.command(name = 'leave')
async def leave(ctx):
     await ctx.voice_client.disconnect()


# async def join(ctx, url: str):
#     vc = discord.utils.get(ctx.guild.voice_channels, name="CF 416")
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

#     if not voice.is_connected():
#         await vc.connect()
#         print("joined vc")
#     else:
#         print("already in vc")

# @bot.command()
# async def leave(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_connected():
#         await voice.disconnect()
#     else:
#         await ctx.send("bot is not connected to vc")
    # if not vc is None:
    #     await voice.disconnect()
    # else:
    #     await ctx.send("The bot is not connected to a voice channel")
    
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


