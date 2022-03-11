import asyncio
from time import perf_counter
from inventory import devices
from scrapli.driver.core import AsyncIOSXEDriver
import getpass

async def send_cmd(device): #such a type of function called 'coroutine'
    async with AsyncIOSXEDriver(
        host = device['host'],
        auth_username = 'username',
        auth_password = 'password',
        auth_strict_key = False,
        ssh_config_file = True,
        transport = 'asyncssh',
    ) as conn:
        response = await conn.send_command('show clock')
        return response

async def main():
    coroutines = [send_cmd(device) for device in devices]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())

    hmac-sha2-256,hmac-sha2-512