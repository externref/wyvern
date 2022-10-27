import asyncio
import logging

import wyvern

l = logging.getLogger(__name__)
l.setLevel(logging.DEBUG)
client = wyvern.GatewayClient("OTY0MTk1NjU4NDY4ODM1MzU4.G8V3T7.puoqO0YxsVjbpthdM_W4LysrQ-4CVRNhlnw4e0", intents=0)


async def main() -> None:
    asyncio.create_task(client.start())
    await asyncio.sleep(10)
    await client.rest.edit_client_user(username="lol")


asyncio.run(main())
