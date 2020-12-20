from header import client, logger

async def hello(message):
    logger.debug("saying hello")
    await message.reply('hey der big guy')
