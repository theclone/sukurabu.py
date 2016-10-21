import discord
import configparser
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('config.ini')
token = config['init']['token']
prefix = config['init']['prefix']
youtube_key = config['init']['youtube_api']

client = discord.Client()
logger = logging.getLogger('Discord')
if not discord.opus.is_loaded():
    if platform == 'linux':
        discord.opus.load_opus('libopus.so.1')
    elif platform == 'win32':
        discord.opus.load_opus('opus')
    else:
        logger.error("unsupported platform")
