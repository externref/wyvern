# wyvern

<p align="center">
<img src="https://raw.githubusercontent.com/sarthhh/wyvern/master/docs/assets/wyvern.png" height=150 width=150><br><br>
</p>

----

<img src="https://img.shields.io/github/license/sarthhh/wyvern?style=flat-square"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"><img src="https://img.shields.io/badge/%20type_checker-pyright-%231674b1?style=flat-square"><img src="https://img.shields.io/github/stars/sarthhh/wyvern?style=flat-square"><img src="https://img.shields.io/github/last-commit/sarthhh/wyvern?style=flat-square"><img src="https://img.shields.io/pypi/pyversions/wyvern?style=flat-square"><img src="https://img.shields.io/pypi/v/wyvern?style=flat-square">

A [WIP] flexible and easy to use Discord API wrapper for python 🚀.
> Warning: This library is very unstable and things might not work as expected. Feel free to create an issue.

## Important Links

Support server: https://discord.gg/FyEE54u9GF

Documentation: https://wyvern.readthedocs.io

PYPI: https://pypi.org/project/wyvern

## Installation
```sh
$python -m pip install git+https://github.com/sarthhh/wyvern
```
## Example
```python
import asyncio
import os

import wyvern

bot = wyvern.GatewayBot(os.environ["TOKEN"], intents=wyvern.Intents.UNPRIVILEGED)


@bot.listener(wyvern.StartingEvent)
async def starting(event: wyvern.StartingEvent) -> None:
    bot.logger.info("Starting bot...")


# or using the implemented decorators


@bot.on_started()
async def started(event: wyvern.StartedEvent) -> None:
    bot.logger.info(f"Logged in as {event.user.tag}")


async def main():
    async with bot:
        await bot.start()


asyncio.run(main())
```
