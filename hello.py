from header import client, logger

async def hello(message):
    logger.debug("saying hello")
    chan = message.channel
    msg = 'hey der big guy {0.author.mention}'.format(message)
    await chan.send(msg)
