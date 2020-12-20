from header import client, logger, token, prefix
from command_handler import command_handler
import quote


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # prefixed commands
    if message.content.startswith(prefix):
        logger.debug("command handler started")
        await command_handler(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    quote.initGPT()

client.run(token)
