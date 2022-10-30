```py title="wyvern/examples/event_handler.py"
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