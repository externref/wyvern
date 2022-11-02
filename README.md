# wyvern
![](https://img.shields.io/github/license/sarthhh/asuka?style=flat-square)
![](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)
![](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat-square)
![](https://img.shields.io/github/stars/sarthhh/asuka?style=flat-square)
![](https://img.shields.io/github/last-commit/sarthhh/asuka?style=flat-square)

A flexible and easy to use Discord API wrapper for python 🚀.

## Why use wyvern? 
* Feature rich API.
* Full control over the library's functionality.
* Built-in extensions for prefix commands.
* Interaction commands handling.

## Installation
```sh
# from pypi 
$python -m pip install wyvern
# from source stable branch
$python -m pip install git+https://github.com/sarthhh/wyvern@main
# from source development branch 
$pythonn -m pip install git+https://github.com/sarthhh/wyvern
```

## Example Code:
* Basic GatewayClient with listener. 
```py
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
        await message.respond("pong!")


# runs the bot.

client.run()
```
* GatewayClient with custom event handler.
```py
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
```