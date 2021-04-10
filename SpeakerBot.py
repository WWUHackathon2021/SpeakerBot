import discord
import discord.ext
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

<<<<<<< HEAD
client.run(TOKEN)
=======
<<<<<<< HEAD
<<<<<<< HEAD
client.run(os.getenv('TOKEN'))
=======
client.run(os.getenv("TOKEN"))
>>>>>>> 95119ec22b7ee4f07cd7c4dcc3da0049072c65da
=======
client.run(TOKEN)
>>>>>>> 4825926db6162252fa527c07d69b4ab107bde71a
>>>>>>> main
