import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from termcolor import colored

print(colored("Instagram @3g86", "blue"))


link_file = sys.argv[1]


with open(link_file, 'r') as file:
    links = [line.strip() for line in file.readlines()]

working_links = []
not_working_links = []

async def check_link(link):
    global working_count, not_working_count
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(link) as response:
                if response.status == 200:
                    print(colored(f"{link} shell is work", "green"))
                    working_links.append(link)
                    working_count += 1
                elif response.status in [301, 302]:
                    # print(colored(f"{link} redirects to another page", "red"))
                    pass
                else:
                    print(colored(f"{link} shell not work", "red"))
                    not_working_links.append(link)
                    not_working_count += 1
        except Exception as e:
            # print(colored(f"{link} {e}", "yellow"))
            not_working_links.append(link)
            not_working_count += 1
        await asyncio.sleep(0.1)

async def check_links(chunk):
    tasks = []
    for link in chunk:
        tasks.append(asyncio.ensure_future(check_link(link)))
    await asyncio.gather(*tasks)

async def main():
    CHUNK_SIZE = 50
    chunks = [links[i:i+CHUNK_SIZE] for i in range(0, len(links), CHUNK_SIZE)]
    tasks = []
    for chunk in chunks:
        tasks.append(asyncio.ensure_future(check_links(chunk)))
    await asyncio.gather(*tasks)

with ThreadPoolExecutor(max_workers=10) as executor:
    loop = asyncio.get_event_loop()
    working_count = 0
    not_working_count = 0
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print(colored("stop nigaa."))

print(colored(f"\n------------------------------------------------------------------------", "green"))
print(colored(f"Number shell working: {working_count}", "green"))
print(colored(f"Number shell not working: {not_working_count}", "red"))
print(colored("Instagram @3g86", "blue"))
print(colored(f"------------------------------------------------------------------------", "green"))
with open("working.txt", "w") as f:
    f.write("\n".join(working_links))

with open("not_working.txt", "w") as f:
    f.write("\n".join(not_working_links))

