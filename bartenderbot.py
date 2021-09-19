# bot.py
import os

import discord
import urllib.request
import urllib.parse 
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')
PORT = os.getenv('PORT')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is ready to serve drinks!')

@client.event
async def on_guild_join(message):
    await message.channel.send(f'{client.user} is ready to serve drinks! Use >bar_help to learn more.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>bar_help'):
        embedVar = discord.Embed(title="Help", description="Commands and what they do", color=0x9e7606)
        embedVar.add_field(name='>make_me_a_drink', value='Gets a random mixed drink recipe', inline=False)
        await message.channel.send(embed = embedVar)

    if message.content.startswith('>make_me_a_drink'):
        url = URL + ':' + PORT + '/make_drink'
        drink = urllib.request.urlopen(url).read()
        drink_dict = json.loads(drink)

        result = ''

        for ingredient in drink_dict['ingredients']:
            ingredient_str = ingredient['measure'] + ' ' + ingredient['ingredient']
            result += ingredient_str + '\n'

        embedVar = discord.Embed(title="Here's your drink:", description=result, color=0x9e7606)

        await message.channel.send(embed = embedVar)
    

client.run(TOKEN)