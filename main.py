from header import client, logger, token, prefix
from command_handler import command_handler


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.author.name == '1Joetom[IRH]':
        msg = 'shut up {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(prefix):
        logger.debug("command handler started")
        await command_handler(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
