import discord
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands
import random
# import youtube_dl
from youtube_dl import YoutubeDL


load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

bot = commands.Bot(command_prefix='!')
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

class General(commands.Cog):
    @commands.command(aliases=['j'], description="The bot will join whichever call you\'re currently in")
    async def join(self, ctx):
        # vc = discord.utils.get(ctx.guild.voice_channels, name=arg)
        try:
            vc = ctx.author.voice.channel
        except:
            print("user isn not in vc, bot can't join")
            await ctx.send("You must be connected to a voice channel for the SpeakerBot to join!")
            return

        try:    
            await vc.connect()
            await ctx.send("SpeakerBot is now connected to a voice channel!")
        except:
            print("already in vc")
            await ctx.send("SpeakerBot is already connected to a voice channel!")

    @commands.command(aliases=['l'], description="The bot will leave the call.")
    async def leave(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        try:
            if voice.is_connected():
                await voice.disconnect()
                await ctx.send("SpeakerBot has left the voice channel")
        except:
            print("bot is not connected to vc")
            await ctx.send("Unable to leave voice channel: SpeakerBot is not currently in a voice channel.")


class Music(commands.Cog):
    @commands.command(aliases=['pl'], description="The bot will play the youtube link stated after \'!pl\'")
    async def play(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = get(bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
        else:
            await ctx.send("Already playing song")
            return

    # async def play(ctx, url : str):
    #     song_here = os.path.isfile("song.mp3")
    #     try:
    #         if song_here:
    #             os.remove("song.mp3")
    #     except PermissionError:
    #         await ctx.send("Music is currently playing! Use !stop or !s to stop the song!")
    #         return

    #     vc = discord.utils.get(ctx.guild.voice_channels, name='CF 420')
    #     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)

    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #     }

    #     #FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([url])
    #     for file in os.listdir("./"):
    #         if file.endswith(".mp3"):
    #             os.rename(file, "song.mp3")
        
    #     voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command(aliases=['p'], description="The bot will pause the currently playing video.")
    async def pause(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
                print("bot is paused")
                await ctx.send("SpeakerBot is currently paused!")
        except:
            print("You messed up")
            await ctx.send("Nothing is playing at the moment!")

    @commands.command(aliases=['r'], description="The bot will resume the currently paused video.")
    async def resume(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
                print("bot is now resuming")
                await ctx.send("SpeakerBot is cranking out the tunes again!")
        except:
            print("You messed up")
            await ctx.send("It's not paused, silly!")

    @commands.command(aliases=['s'], description="The bot will stop the currently playing video")
    async def stop(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("Music has stopped! :(")

@bot.command(name = "list")
async def list(ctx):
    for f_name in os.listdir('Playlists/.'):
        if f_name.endswith('.txt'):
            await ctx.send(f_name)

@bot.command(name = 'addPl')
async def addPl(ctx, arg):
    newFile = ""
    newFile = "Playlists/"
    newFile += arg + ".txt"
    # print(newFile)
    if os.path.exists(newFile):
        await ctx.send(arg+" Already Exists")
    else:
        file = open(newFile,'w+')

@bot.command(name = 'add')
async def add(ctx, song, playlist):

    newPlaylist=""
    newPlaylist +="Playlists/" + playlist
    isSeen = 0
    with open(newPlaylist) as f:
        for line in f:
            if line.strip() == song:
                isSeen = 1
                await ctx.send(song + " already exists")
                return
    if isSeen == 0:
        with open(newPlaylist,'a') as file:
            newSong = ""
            newSong = song + '\n'
            file.write(newSong)
        msg = "Added "+  song +  " to " + playlist
        await ctx.send(msg)


    # with open(newPlaylist) as f:
    #     seen = set()
    #     dSong = ""
    #     dSong = song
    #     seen.add(dSong)
    #     for line in f:
    #         line_lower = line.lower()
    #         if line_lower in seen:
    #             await ctx.send(song + " already exists")
    #             isSeen = 1
    #             return
    #         else:
    #             seen.add(line_lower)
    # if isSeen == 0:         
    #     with open(newPlaylist,'a') as file:
    #         newSong = ""
    #         newSong = song + '\n'
    #         file.write(newSong)
    #     msg = "Added "+  song +  " to " + playlist
    #     await ctx.send(msg)

@bot.command(name = "showPl")
async def showPl(ctx,playlist):
    iter = 1
    songs = " "
    songs += "**------------------------------------------------------------------------------------------**\n"
    newPlaylist=""
    newPlaylist +="Playlists/" + playlist
    sep = '.'
    owner = playlist.split(sep,1)[0]
    songs += "**"+owner+'\'s Playlist**\n'
    songs += "**------------------------------------------------------------------------------------------**\n"
    with open(newPlaylist) as file:
        for line in file:
            line_lower = line.lower()
            songs+= "**"+str(iter)+"**" + ") " + line_lower
            iter+=1
    songs+="**------------------------------------------------------------------------------------------**\n"
    await ctx.send(songs)


@bot.command(name = 'delSong')
async def delSong(ctx, song,playlist):
    # with open(playlist,"r") as f:
    #     lines = f.readlines()
    # for line in lines:
    #     print(line.strip("\n") != song)
    #     print(line)
    newPlaylist=""
    newPlaylist +="Playlists/" + playlist
    with open(newPlaylist,"r") as f:
        lines = f.readlines()
    with open(newPlaylist,"w") as f:
        for line in lines:
            if line.strip("\n") != song:
                f.write(line)
    # @bot.command()
    # async def p(self,ctx,*,query):

@bot.command(name = 'delPl')
async def delPl(ctx,playlist):
    # for f_name in os.listdir('.'):
    #     if f_name.endswith('.txt'):
    #         await ctx.send(f_name)
    for f_name in os.listdir('Playlists/.'):
        if f_name == playlist:
            rm = ""
            rm += "Playlists/"+f_name
            os.remove(rm)
            return
    await ctx.send(playlist+" Does Not Exist")

bot.add_cog(General())
bot.help_command.cog = bot.cogs["General"]
bot.add_cog(Music())
bot.run(TOKEN)


