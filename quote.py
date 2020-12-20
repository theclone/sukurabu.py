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
    prompt = message.content.strip()[6:]   # strip prefix and 'eight'
    if prompt.strip() == "":
        prompt = ""
    chan = message.channel
    logger.debug("genereation of sampleTM")
    sample = gpt2.generate(sess, prefix=prompt, length=100, temperature=1.0, return_as_list=True)
    logger.debug(sample[0])
    # match = regex.match(r'\n?.*\n+', sample[0])
    match = sample[0].split('\n\n')
    if len(match) > 1:
        msg = match[random.randrange(0, len(match))]
        msg = message.author.mention + msg
        msg = msg.format(message)
    else:
        msg = "nothin sorry"
    await chan.send(msg)