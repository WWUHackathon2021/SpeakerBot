import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
import youtube_dl

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

bot = commands.Bot(command_prefix='!')
arr = []
players = {}
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

@bot.command(aliases=['j'])
async def join(ctx):
    # vc = discord.utils.get(ctx.guild.voice_channels, name=arg)
    try:
        vc = ctx.author.voice.channel
    except:
        print("user isn not in vc, bot can't join")
        await ctx.send("You must be connected to a voice channel for the SpeakerBot to join!")
        return

    try:    
        await vc.connect()
        print("joined vc")
        await ctx.send("SpeakerBot is now connected to a voice channel!")
    except:
        print("already in vc")
        await ctx.send("SpeakerBot is already connected to a voice channel!")

@bot.command(aliases=['l'])
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

# bot.add_command(test)

@bot.command(name = 'add')
async def add(ctx, arg):
    arr.append(arg)

@bot.command(name = "show")
async def show(ctx):
    await ctx.send(arr)

@bot.command(name = 'delete')
async def delete(ctx, arg):
    arr.remove(arg)

    # @bot.command()
    # async def p(self,ctx,*,query):

@bot.command()
async def play(self, ctx, *, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)  
    await ctx.send(f'Now playing: {player.title}')
# https://www.youtube.com/watch?v=m2uTFF_3MaA

bot.run(TOKEN)


