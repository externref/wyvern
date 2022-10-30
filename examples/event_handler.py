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

# subclassing to create a new EventHandler class.
# events listeners can be added using the @wyvern.listener decorator.
# the client can be accessed using client attribute inside the listener.


class MyHandler(wyvern.EventHandler):
    @wyvern.listener(wyvern.Event.MESSAGE_CREATE)
    async def message_create(self, message: wyvern.Message) -> None:
        print(f"Message sent by {message.author.username}")


# the subclass' type ( !not instance ) is provided for the event_handler kwarg inside
# the client class. which uses this custom EventHandler instead of a default one.

client = wyvern.GatewayClient("TOKEN", event_handler=MyHandler)

# runs the bot.

client.run()
