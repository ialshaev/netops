import asyncio
from time import perf_counter
from rich import print as rprint
from inventory import devices
from scrapli.driver.core import AsyncIOSXEDriver

async def send_cmd(device,cmd): #such a type of function called 'coroutine'
    async with AsyncIOSXEDriver(
        host = device['host'],
        auth_username = 'cisco',
        auth_password = 'cisco',
        auth_strict_key = False,
        transport = 'asyncssh'
    ) as conn:
        await conn.send_config(cmd)

async def main():
    cmd = str(input('\nEnter the command: '))
    coroutines = [send_cmd(device,cmd) for device in devices]
    await asyncio.gather(*coroutines)

if __name__ == "__main__":
    asyncio.run(main())