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
discord.opus.load_opus('libopus.so')
