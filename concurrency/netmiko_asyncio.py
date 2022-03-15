import asyncio
from time import perf_counter
from rich import print as rprint
from inventory import devices
from scrapli.driver.core import AsyncIOSXEDriver
import getpass

async def send_cmd(device): #such a type of function called 'coroutine'
    async with AsyncIOSXEDriver(
        host = device['host'],
        auth_username = 'cisco',
        auth_password = 'cisco',
        auth_strict_key = False,
        transport = 'asyncssh'
    ) as conn:
        response = await conn.send_command('show ip int bri | incl 192')
        return response.result

async def main():
    coroutines = [send_cmd(device) for device in devices]
    results = await asyncio.gather(*coroutines)
    for result in results:
        rprint(f'[green]=== {result} ===[/green]\n\n')

if __name__ == "__main__":
<<<<<<< HEAD
    asyncio.run(main())

    hmac-sha2-256,hmac-sha2-512
=======
    start = perf_counter()
    asyncio.run(main())
    end = perf_counter()
    total_time = end - start
    print(total_time)
>>>>>>> bf223ae... scrapli fix with add asyncio concurrency
