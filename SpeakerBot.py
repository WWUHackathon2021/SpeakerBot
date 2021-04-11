import discord
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands
import random
from youtube_dl import YoutubeDL
from collections import deque

load_dotenv()
TOKEN = os.getenv("TOKEN")
queue = deque()

bot = commands.Bot(command_prefix='!')

#Once the bot is online, it will display a ready message in the terminal and in the bot-terminal channel.
@bot.event
async def on_ready():
   print('We have logged in as {0.user}'.format(bot))
   await bot.get_channel(828834006829105162).send("SpeakerBot is ready to go! Make sure to use !help if you want the command list.")

#Class of any general commands that don't fit any category.
class General(commands.Cog):

    #Brings in the bot to the current voice channel. '!join' or '!j'
    @commands.command(aliases=['j'], description="The bot will join whichever call you\'re currently in")
    async def join(self, ctx):
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

    #The bot is forced to leave the current channel. '!leave' or '!l'
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

#A class that features all simple music player commands. Playlist commands are seperate.
class Music(commands.Cog):

    #The bot plays the youtube video link after the command. '!play [video url]' or '!pl [video url]'
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

    #Pauses the current youtube video. '!pause' or '!p'
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

    #Resumes the current youtube video. '!resume' or '!r'
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

    #Stops the current song from playing and removes from the queue. '!stop' or '!s'
    @commands.command(aliases=['s'], description="The bot will stop the currently playing video")
    async def stop(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("Music has stopped! :(")

    #Adds the indicated video to the current queue (if there is one). '!queue [video url] or !q [video url]'
    @commands.command(aliases=['q'], description="Queues up the next video specified")
    async def queue(self, ctx, url):

        global queue
        queue.append(url)
        await ctx.send(f'`{url}` was added to the queue!')

    #Removes a song in the queue that the user can specify. '!skip [song number]'
    @commands.command(description="The bot removes the specified song in the queue")
    async def skip(self, ctx, num = None):
        global queue

        try:
            if (num is None):
                queue.popleft()
            else:
                del queue[int(num)]

            await ctx.send(f'Current queue: `{queue}`')

        except:
            await ctx.send("Queue is empty or that index is out of bounds!")

    #Displays a list of all the videos in the current queue. '!view or !v'
    @commands.command(description="The bot shows all of the videos in the queue")
    async def view(self, ctx):
        await ctx.send(f'Current queue: `{queue}!`')

#A class the specializes in playlist commands. 
class Playlist(commands.Cog):

    #Lists all currently stored playlists in the directory. '!list' or '!l'
    @commands.command(description="The bot displays all stored playlists")
    async def pList(self, ctx):
        for f_name in os.listdir('Playlists/.'):
            if f_name.endswith('.txt'):
                await ctx.send(f_name)

    #Add a new playlist if it isn't in the playlist folder already. '!addPl [listname]' or '!ap [listname]'
    @commands.command(aliases=['ap'], description="The bot adds a new playlist if the name is valid")
    async def addPl(self, ctx, arg):
        newFile = ""
        newFile = "Playlists/"
        newFile += arg + ".txt"
        # print(newFile)
        if os.path.exists(newFile):
            await ctx.send(arg+" Already Exists")
        else:
            file = open(newFile,'w+')

    #Adds a new song to the playlist if it's not already in there. '!add [songname] [playlist]'
    @commands.command(description="The bot adds a new song to the playlist")
    async def add(self, ctx, song, playlist):

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

    #Display the indicated playlist. '!showPL [playlist]' or '!sPL [playlist'
    @commands.command(aliases=['sPL'], description="The bot displays the current edition of the named playlist")
    async def showPl(self, ctx, playlist):
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

    #Delete indicated song from the indicated playlist. Can't be undone!. '!delSong [song name] [playlist]' or '!delS [song name] [playlist]'
    @commands.command(aliases=['delS'], description="The bot deletes a selected song from the selected playlist.")
    async def delSong(self, ctx, song,playlist):
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
        # @commands.command()
        # async def p(self,ctx,*,query):

    #Delete a specified playlist. Can't be undone! '!delPl' or '!dP'
    @commands.command(aliases=['dP'], description="The bot deletes an entire playlist")
    async def delPl(self, ctx,playlist):
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
bot.add_cog(Playlist())
bot.run(TOKEN)