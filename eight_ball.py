import random
import logging

responses = [
    "most definitely"
    "i'm kinda tired, ask again later pls"
    "not in the foreseeable future"
    "NO - it may cause disease contraction"
    "there is a chance"
    "don't even think about it"
    "sure, why not"
    "if you believe hard enough"
    "yes"
    "no"
    "iunno"
    "who knows"
    "for sure"
]

async def eight_ball(message, client, logger):
    logger.debug("eight")
    question = message.content[7:]   # strip prefix and 'eight', including whitespace
    msg = message.author.mention + ' `asks` ' + '__**' + question + '**__'
    + '\n:8ball: `responds` ' + '__**' + responses[random.randint(0, len(responses))] + '**__'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)
