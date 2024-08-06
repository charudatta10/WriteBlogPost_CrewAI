import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            print(f"Request to {url} successful. Keeping the connection open for 30 seconds...")
            await asyncio.sleep(30)  # Keep the connection open for 30 seconds
            print(f"Done with {url}.")
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status}")

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        await asyncio.gather(*tasks)

async def main(urls):
    await fetch_all(urls)


site_url = "https://charudatta10.github.io/myblog/about.html" #"https://www.youtube.com/watch?v=Qt1TLzxUvys" #"https://medium.com/@152109007c/explore-a29f7f840f0a"
# List of URLs to fetch
urls = [site_url] * 100

# Run the main function with the list of URLs
asyncio.run(main(urls))
