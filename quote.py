from discord_op import reply
from header import client, logger
import gpt_2_simple as gpt2
import regex
import random

sess = None

def initGPT():
    global sess
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)

async def quotation(message):
    global sess
    logger.debug("quotation")
    prompt = message.content.strip()[6:]   # strip prefix and 'quote'
    if prompt.strip() == "":
        prompt = ""
    chan = message.channel
    logger.debug("genereation of sampleTM")
    sample = gpt2.generate(sess, prefix=prompt, length=100, temperature=1.0, return_as_list=True)
    logger.debug(sample[0])
    match = sample[0].split('\n\n')
    match = [i for i in match if i.strip()] 
    if len(match) > 1:
        msg = match[random.randrange(0, len(match))]
        msg = message.author.mention + "\n" + msg
        msg = msg.format(message)
    else:
        msg = "nothin sorry"
    await reply(message, msg)

async def quotation_batch(message):
    global sess
    logger.debug("quotation")
    prompt = message.content.strip()[11:]   # strip prefix and 'quotematch'
    if prompt.strip() == "":
        prompt = ""
    chan = message.channel
    logger.debug("genereation of sampleTM")
    sample = gpt2.generate(sess, prefix=prompt, length=100, temperature=1.0, return_as_list=True)
    logger.debug(sample[0])
    match = sample[0].split('\n\n')
    match = [i for i in match if i.strip()]
    if len(match) > 1:
        msg = '\n'.join(match)
        msg = message.author.mention + "\n" + msg
        msg = msg.format(message)
    else:
        msg = "nothin sorry"
    await reply(message, msg)
