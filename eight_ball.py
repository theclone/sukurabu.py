import random
import logging

responses = [
    "most definitely",
    "i'm kinda tired, ask again later pls",
    "not in the foreseeable future",
    "NO - it may cause disease contraction",
    "there is a chance",
    "don't even think about it",
    "sure, why not",
    "if you believe hard enough",
    "not even in your lewdest fantasies",
    "have you thought about not asking that question",
    "yes",
    "probably not",
    "no",
    "iunno",
    "who knows",
    "mayhaps",
    "the heart of cards say yes",
    "how bout no",
    "ERROR: TOO INSIGNIFICANT TO ANSWER",
    "maybe you should ask again",
    "all i knw is that my heart says maybe",
    "for sure"
]

async def eight_ball(message, client, logger):
    logger.debug("eight")
    question = message.content[7:]   # strip prefix and 'eight', including whitespace
    if question.strip() == "":
        return
    msg = message.author.mention + ' `asks` ' \
        + '__**' + question + '**__' \
        + '\n:8ball: `responds` ' + '__**' \
        + responses[random.randint(0, len(responses) - 1)] + '**__'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)
