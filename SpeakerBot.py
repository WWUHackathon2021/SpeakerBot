import discord
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
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
    vc = ctx.author.voice.channel

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

@bot.command(aliases=['pl'])
async def play(ctx, url : str):
    song_here = os.path.isfile("song.mp3")
    try:
        if song_here:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Music is currently playing! Use !stop or !s to stop the song!")
        return

    vc = discord.utils.get(ctx.guild.voice_channels, name='CF 420')
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    #FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command(aliases=['p'])
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
            print("bot is paused")
            await ctx.send("SpeakerBot is currently paused!")
    except:
        print("You messed up")
        await ctx.send("Nothing is playing at the moment!")

@bot.command(aliases=['r'])
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
            print("bot is now resuming")
            await ctx.send("SpeakerBot is cranking out the tunes again!")
    except:
        print("You messed up")
        await ctx.send("It's not paused silly!")

@bot.command(aliases=['s'])
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Music has stopped! :(")
    
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

bot.run(TOKEN)


