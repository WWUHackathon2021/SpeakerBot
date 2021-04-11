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

@bot.command()
async def join(ctx):
    # vc = discord.utils.get(ctx.guild.voice_channels, name=arg)
    vc = ctx.author.voice.channel

    try:
        await vc.connect()
        print("joined vc")
        await ctx.send("SpeakerBot is now connected to a voice channel!")
    except:
        print("already in vc")
        await ctx.send("SpeakerBot is already connected to a voice channel!")

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:
        if voice.is_connected():
            await voice.disconnect()
            print("bot left vc")
            await ctx.send("SpeakerBot has left the voice channel")
    except:
        print("bot is not connected to vc")
        await ctx.send("Unable to leave voice channel: SpeakerBot is not currently in a voice channel.")
    
#  @bot.command(name = 'testing')
#  async def test(ctx):
#      test_quote = [
#          'David',
#          'Clothesline',
#          'David noooo do not pull the trigger'
#      ]
#      response = random.choice(test_quote)
#      await ctx.send(response)

# # bot.add_command(test)

# @bot.command(name = 'add')
# async def test(ctx, arg):
#     arr.append(arg)

# @bot.command(name = "show")
# async def test(ctx):
#     await ctx.send(arr)

# @bot.command(name = 'delete')
# async def test(ctx, arg):
#     arr.remove(arg)

bot.run(TOKEN)


