Getting started
===============

## First basic bot

### Creating a bot instance

```python
import asyncio
import os

import wyvern

bot = wyvern.GatewayBot(os.environ["TOKEN"], intents=wyvern.Intents.UNPRIVILEGED)
```
### Listening to events
```python
@bot.listener(wyvern.StartingEvent)
async def starting(event: wyvern.StartingEvent) -> None:
    bot.logger.info("Starting bot...")


# or using the implemented decorators


@bot.on_started()
async def started(event: wyvern.StartedEvent) -> None:
    bot.logger.info(f"Logged in as {event.user.tag}")
```

### Running the bot
```python
async def main():
    async with bot:
        await bot.start()


asyncio.run(main())
```