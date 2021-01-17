"""

Utilities to help owoifying text.

"""

from owoify import Owoifator

_should_owo = False
_owoifator = Owoifator()

async def owotoggle(msg):
    global _should_owo

    # Toggle
    _should_owo = not _should_owo

    # Tell user current value.
    if _should_owo:
        await msg.reply('owo is on.')
    else:
        await msg.reply('owo is off.')

def should_owo():
    global _should_owo
    return _should_owo

def owoify(text):
    return _owoifator.owoify(text)
