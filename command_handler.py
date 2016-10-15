from eight_ball import eight_ball
from hello import hello

commands = {
    'eight': eight_ball,
    'hello': hello
}

async def command_handler(message, client, logger):
    print("in command handler")
    prefixed_command = message.content.split()[0]
    command = prefixed_command[1:]  # take out prefix

    if command in commands:
        logger.debug("doing command " + command)
        await commands[command](message, client, logger)  # basically a case statement
    else:
        logger.debug("unsupported command!")
