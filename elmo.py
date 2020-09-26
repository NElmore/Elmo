import discord
import os
import logging
import random
import numpy as np
import asyncio
import requests
import time
from lastfm import *
from youtube_api import YouTubeDataAPI
from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

elmo = discord.Client()
random.seed(time.time())
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
yt_key = os.getenv('YT_KEY')
yt = YouTubeDataAPI(yt_key)
'''
export these to a different file later, it looks nice
'''
def musicSuggestor(message):
    #this will come in useful later
    filen =  "https://thumbs.dreamstime.com/b/arab-musician-violin-guitar-isolated-white-arab-musician-violin-guitar-isolated-white-100298368.jpg"
    inputtag = message.content[8:]
    outputdata = getTopTracksByTag(inputtag, 100)
    outputlen = len(outputdata)
    if(outputlen != 0):
        outputtrack = outputdata[random.randrange(0,outputlen)]
    else:
        embedVar = discord.Embed(title="Elmo couldn't find anything to match that, sorry", color=0x00ff00)
        embedVar.set_image(url = 'https://i2.wp.com/media4.giphy.com/media/jPAdK8Nfzzwt2/giphy.gif')
        return embedVar
    try:
        filen = str(jprint(getinfo(outputtrack[1], outputtrack[0])["track"]["album"]["image"][3]["#text"]))
        filen = filen.strip('"')
    except:
        #placeholder image in case of none attached
        filen =  "https://thumbs.dreamstime.com/b/arab-musician-violin-guitar-isolated-white-arab-musician-violin-guitar-isolated-white-100298368.jpg"
    if (filen == "https://thumbs.dreamstime.com/b/arab-musician-violin-guitar-isolated-white-arab-musician-violin-guitar-isolated-white-100298368.jpg"):
        filen = yt.search(str(outputtrack[1]) + '-' + str(outputtrack[0]))[0]['video_thumbnail']
    embedVar = discord.Embed(title=outputtrack[1] + " - " + outputtrack[0], color=0x00ff00)
    embedVar.add_field(name='https://www.youtube.com/watch?v=' + yt.search(str(outputtrack[1]) + '-' + str(outputtrack[0]))[0]['video_id'], value = yt.search(str(outputtrack[1]) + '-' + str(outputtrack[0]))[0]['video_description'], inline = False)
    embedVar.set_thumbnail(url = filen)
    return embedVar

def urbanD(message):
    query = message.content[5:]
    response = requests.get("https://api.urbandictionary.com/v0/define?term="+query).json()['list'][0]
    output = "\n ```Definition: " + response['definition'] + "\nExample: " + response['example'] + " ```"
    if(len(output)>2048):
        output = output[:2000] + "...[Full Definition at the link below]```"
    embedVar = discord.Embed(title=query, description =  output, color = 0xEEAB1B)
    embedVar.add_field(name = "Link to UrbanDictionary:", value = requests.get("https://api.urbandictionary.com/v0/define?term="+query).json()['list'][0]['permalink'], inline=False)
    return embedVar
    
def elmoifycase1(message):
    x = str(message.author)[:-5]
    query = message.content[9:]
    query = query.replace(" I ", " " + x + " ")
    query = query.replace(" i ", " " + x +" ")
    query = query.replace(" me ", " " + x + " ")
    query = query.replace(" my ", " " + x + "'s ")
    query = query.replace(" I'm", " " + x + " is")
    query = query.replace(" i'm", " " + x + " is")
    query = query.replace(" mine", " " + x + "'s")
    query = query.replace(" myself", " " + x + "'s self")
    return query

def elmoifycase2(message):
    query = message.content[11:]
    x = message.content[11:message.content.find(" ")]
    query = message.content[message.content.find(" "):]
    query = query.replace(" I ", " " + x + " ")
    query = query.replace(" i ", " " + x +" ")
    query = query.replace(" me ", " " + x + " ")
    query = query.replace(" my ", " " + x + "'s ")
    query = query.replace(" I'm", " " + x + " is")
    query = query.replace(" i'm", " " + x + " is")
    query = query.replace(" mine", " " + x + "'s")
    query = query.replace(" myself", " " + x + "'s self")
    return query

'''
The ranch dimension ends
'''


@elmo.event
async def on_ready():
    print('We have logged in as {0.user}'.format(elmo))
    await elmo.change_presence(activity=discord.Game(name="n.help"))
    '''user.setPresence({
        status: "online",  //You can show online, idle....
        game: {
            name: "Using n.help",  //The message shown
            type: "PLAYING" //PLAYING: WATCHING: LISTENING: STREAMING:
        }
        '''

@elmo.event
async def on_message(message): #ignores if message is from elmo
    if message.author == elmo.user:
        return

    if "n.help" == message.content.lower():
        embedVar = discord.Embed(title="__Command List__", color=0x00ff00)#todo, add command list here
        embedVar.add_field(name = 'n.help: Well... you\'re here\nn.elmo: Summon a random elmo\nn.music <tag>: Elmo gives you a random music suggestion related to provided tag\nn.ud <word>: Learning words on Urban Dictionary with Elmo\nn.elmoify <phrase or paragraph>: Elmo will do the rest', value = "n.elmoify has a second option to run with a name you input, running the command n.elmoify-><Name>",inline = False)
        await message.channel.send(embed=embedVar)
    elif "n.elmo" == message.content.lower(): #add a self search function sometime?
        filen = 'ElmoPics/' + str(random.randrange(1, 30)) + '.png'
        embedVar = discord.Embed(title="Hello friend!", color=0x00ff00)
        file = discord.File(filen, filename = "image.png")
        embedVar.set_image(url = "attachment://image.png")
        await message.channel.send(file=file, embed=embedVar)
    elif message.content.startswith('n.music '):        
        await message.channel.send(embed=musicSuggestor(message))
    elif message.content.startswith('n.ud '):
        await message.channel.send(embed=urbanD(message))
    elif message.content.startswith('n.elmoify '):
        await message.channel.send("```" + elmoifycase1(message) + "\n```")
    elif message.content.startswith('n.elmoify->'):
        await message.channel.send("```" + elmoifycase2(message) + "\n```")
        

elmo.run(token)#perm number 3533888 