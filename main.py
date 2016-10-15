import discord
import logging
import sys
import configparser
from command_handler import command_handler

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('config.ini')
token = config['init']['token']
prefix = config['init']['prefix']

client = discord.Client()
logger = logging.getLogger('Discord')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(prefix):
        logger.debug("command handler started")
        await command_handler(message, client, logger)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
