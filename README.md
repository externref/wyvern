# Asuka 

![](https://img.shields.io/github/license/sarthhh/asuka?style=flat-square)
![](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)
![](http://www.mypy-lang.org/static/mypy_badge.svg)
![](https://img.shields.io/github/stars/sarthhh/asuka?style=flat-square)
![](https://img.shields.io/github/last-commit/sarthhh/asuka?style=flat-square)

An easy to use, statically typed Discord API wrapper using python.

EXAMPLE
-------

```python
import asuka

bot = asuka.Bot("TOKEN")


@asuka.listener_config(guild_only=True, humans_only=True)
@bot.listener(asuka.MessageCreate)
async def hello(event: asuka.MessageCreate) -> None:
    """
    -> This coro gets triggered every time a message is sent.
    -> The conditions for when to invoke the coro can be controlled
       using listener configs
    """
    print(f"Message sent by {event.user.username}")


@bot.listen_once(asuka.MessageCreate)
async def first_message(event: asuka.MessageCreate) -> None:
    """Gets triggred once in a runtime."""
    print(f"First message in this session was sent by: {event.user}")


bot.run()
```
