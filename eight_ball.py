import random

from header import logger
from owo import should_owo, owoify

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
    "THERE IS AS YET INSUFFICIENT DATA FOR A MEANINGFUL ANSWER.",
    "maybe you should ask again",
    "all i know is that my heart says maybe",
    "for sure",
    "42",
    "i'd do it",
    "do it, you won't",
    "why not",
    "only one way to find out",
    "don't ask a bot for this"
]

async def eight_ball(message):
    logger.debug("eight")
    # Strip prefix + command
    questionarr = message.content.split()
    if len(questionarr) == 1:
        await message.reply('Hey! Give me something to predict.')
        return
    question = ' '.join(questionarr[1:])

    if question.strip() == "":
        return
    resp = responses[random.randint(0, len(responses) - 1)]
    if should_owo():
        resp = owoify(resp)
    msg = message.author.mention + ' `asks` ' \
        + '__**' + question + '**__' \
        + '\n:8ball: `responds` ' + '__**' \
        + resp + '**__'
    msg = msg.format(message)
    await message.reply(msg)
