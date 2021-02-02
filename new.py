import discord
import os
TOKEN= 'ODA2MjE1NDY3MTgxNTM5MzQ4.YBmMqg.yIyYwXme5QtKBaz_bNonuqsdg4E'
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

client.run(TOKEN)
