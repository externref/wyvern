# wyvern

<p align="center">
<img src="./docs/assets/wyvern.png" height=150 width=150><br><br>
<img src="https://img.shields.io/github/license/sarthhh/wyvern?style=flat-square">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square">
<img src="https://img.shields.io/badge/%20type_checker-pyright-%231674b1?style=flat-square">
<img src="https://img.shields.io/github/stars/sarthhh/wyvern?style=flat-square">
<img src="https://img.shields.io/github/last-commit/sarthhh/wyvern?style=flat-square">
<img src="https://img.shields.io/pypi/pyversions/wyvern?style=flat-square">
<img src="https://img.shields.io/pypi/v/wyvern?style=flat-square">
<br><br>
A [WIP] flexible and easy to use Discord API wrapper for python 🚀.
</p>

> Warning: This library is very unstable and things might not work as expected. Feel free to create an issue.

## Important Links

Support server: https://discord.gg/FyEE54u9GF

Documentation: https://sarthhh.github.io/wyvern/

PYPI: https://pypi.org/projects/wyvern

## Installation
```sh
$python -m pip install git+https://github.com/sarthhh/wyvern
```

## Example Code:

* CommandsClient with commands support.
```py
import wyvern

# creating a CommandsClient object to interaction with commands.
client = wyvern.CommandsClient("TOKEN")

# creating a slash command using with_slash_command decorator.
@client.with_slash_command(name="hello", description="says a hello")
async def hello(interaction: wyvern.ApplicationCommandInteraction) -> None:
    # creating a response to the interaction.
    await interaction.create_message_response("hi!")


# running the bot.
client.run()

```
* Basic GatewayClient with listener. 
```py
import wyvern

# creating a GatewayClient instance and storing it into the client variable.
# this acts as the interface between your bot and the code.

client = wyvern.GatewayClient("TOKEN", intents=wyvern.Intents.UNPRIVILEGED | wyvern.Intents.MESSAGE_CONTENT)

# creating an EventListener object and adding it to the client's event handler using the
# @client.listen decorator. You can set the maximum amount of time this listener will get triggered using
# the `max_trigger kwarg in the listener decorator.`


@client.as_listener(wyvern.Event.MESSAGE_CREATE)
async def message_create(message: wyvern.Message) -> None:
    """This coroutine is triggerd whenever the MESSAGE_CREATE event gets dispatched."""
    if message.content and message.content.lower() == "!ping":
        await message.respond("pong!")


# runs the bot.

client.run()
```