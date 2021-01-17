"""

Common way to send text to discord (e.g. replies).
Contains a handler to transform all incoming text (from the application) into
owospeak which then is outputted to discord.

"""

from owo import owoify, should_owo

async def reply(msg, text):
    if should_owo():
        text = owoify(text)

    await msg.reply(text)
