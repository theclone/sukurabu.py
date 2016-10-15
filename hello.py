import logging
import sys

async def hello(message, client, logger):
    logger.debug("saying hello")
    msg = 'hey der big guy {0.author.mention}'.format(message)
    await client.send_message(message.channel, msg)
