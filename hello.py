from header import client, logger

async def hello(message):
    logger.debug("saying hello")
    msg = 'hey der big guy {0.author.mention}'.format(message)
    await client.send_message(message.channel, msg)
