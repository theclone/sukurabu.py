from header import logger
from discord_op import reply

async def hello(message):
    logger.debug("saying hello")
    await reply(message, 'hey der big guy')
