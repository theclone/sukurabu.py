from header import client, logger
from eight_ball import eight_ball
from owo import owotoggle
from hello import hello
from music import music
from quote import quotation, quotation_batch

commands = {
    'eight': eight_ball,
    '8'    : eight_ball,
    'hello': hello,
    'music': music,
    'owo' : owotoggle,
    'quote': quotation,
    'quotebatch': quotation_batch
}

async def command_handler(message):
    prefixed_command = message.content.split()[0]
    command = prefixed_command[1:]  # take out prefix

    if command in commands:
        logger.debug("executing command " + command)
        # basically a case statement
        await commands[command](message)
    else:
        logger.debug("unsupported command!")
