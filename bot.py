import os
import random
import discord
import re
import io
from PIL import Image, ImageDraw
import requests

client = discord.Client()

hotwords = [
    re.compile('\\btit\\b'),
    re.compile('\\btits\\b'),
    re.compile('\\btitty\\b'),
    re.compile('\\btitties\\b')
]

bustinthru = [
    'hannibal bustin\' through',
    'hannibal bustin through',
    'hannibal bustin thru',
    'hannibal bustin\' thru'
]


def discrete_phrase(phrase):
    return re.compile('\\b' + phrase + '\\b')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    if any(re.search(regex, msg.content.lower()) for regex in hotwords):
        await client.send_file(msg.channel, 'thetits.png')

    if 'what if it was purple' in msg.content.lower():
        attachment = None

        try:
            attachment = msg.attachments[0]['url']
        except IndexError:
            try:
                last_msg = await get_logs_from_channel(msg.channel)
                attachment = last_msg.attachments[0]['url']
            except IndexError:
                await client.send_message(msg.channel, 'Nothing to make purple!')

        if attachment is not None:
            try:
                img = Image.open(io.BytesIO(requests.get(attachment).content)).convert('RGBA')
                tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(tmp)
                draw.rectangle((0, 0) + img.size, fill=(85, 26, 139, 175))

                img = Image.alpha_composite(img, tmp)
                imgbytearr = io.BytesIO()
                img.save(imgbytearr, format='PNG')
                imgbytearr = imgbytearr.getvalue()
                await client.send_file(msg.channel, io.BytesIO(imgbytearr), filename='its-purple.png')
            except OSError:
                await client.send_message(msg.channel, 'Looks like the last sent file isn\'t an image!')

    if re.search(discrete_phrase('sucks'), msg.content.lower()):
        await client.send_file(msg.channel, 'thissucksman.png')

    if re.search(discrete_phrase('wack'), msg.content.lower()):
        await client.send_file(msg.channel, 'wack.png')

    if re.search(discrete_phrase('boo'), msg.content.lower()):
        await client.send_file(msg.channel, 'imright.png')

    if re.search(discrete_phrase('bird up'), msg.content.lower()):
        await client.send_file(msg.channel, 'birdup.jpg')

    if re.search(discrete_phrase('rice'), msg.content.lower()):
        await client.send_file(msg.channel, 'rice.png')

    if re.search('\\bhannibal (bustin\'?|busting) (thru|through)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'hbt.jpg')

    if re.search(discrete_phrase('call me'), msg.content.lower()):
        await client.send_file(msg.channel, 'callme.jpg')

    if re.search('(brb|be right back)', msg.content.lower()):
        await client.send_file(msg.channel, './brb/' + random.choice(os.listdir('./brb')))

    if re.search(discrete_phrase('who killed hannibal?'), msg.content.lower()):
        await client.send_file(msg.channel, 'death.png')

    if re.search('\\bburgers?\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'burgers.gif')

    if re.search(discrete_phrase('get yourself together'), msg.content.lower()):
        await client.send_file(msg.channel, 'philly.jpg')


async def get_logs_from_channel(channel):
    async for m in client.logs_from(channel):
        if m.attachments:
            try:
                i = Image.open(io.BytesIO(requests.get(m.attachments[0]['url']).content)).convert('RGBA')
                return m
            except OSError:
                # Not an image attachment
                continue

    return None


async def get_last_message_from(channel, message):
    async for m in client.logs_from(channel, limit=1, before=message):
        return m

client.run(os.environ["bot_token"])
