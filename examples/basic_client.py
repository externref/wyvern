# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import wyvern

# creating a GatewayClient instance and storing it into the client variable.
# this acts as the interface between your bot and the code.

client = wyvern.GatewayClient("TOKEN", intents=wyvern.Intents.UNPRIVILEGED | wyvern.Intents.MESSAGE_CONTENT)

# creating an EventListener object and adding it to the client's event handler using the
# @client.listen decorator. You can set the maximum amount of time this listener will get triggered using
# the `max_trigger kwarg in the listener decorator.`


@client.listener(wyvern.Event.MESSAGE_CREATE)
async def message_create(message: wyvern.Message) -> None:
    """This coroutine is triggerd whenever the MESSAGE_CREATE event gets dispatched."""
    if message.content and message.content.lower() == "!ping":
        await message.reply("pong!")


# runs the bot.

client.run()
