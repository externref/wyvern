```py title="wyvern/examples/basic_client.py"
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