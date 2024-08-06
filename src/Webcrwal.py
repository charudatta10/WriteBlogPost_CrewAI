import requests
from bs4 import BeautifulSoup
from itertools import cycle
import itertools
import time

visited_urls = set()
max_depth = 10
max_sites = 10000


# Lists of IP addresses, MAC addresses, and user agents
ip_addresses = [
    "192.168.1.1",
    "203.0.113.5",
    "172.16.254.1",
    "198.51.100.10",
    "192.0.2.25",
    "203.0.113.15",
    "172.16.254.2",
    "198.51.100.20",
    "192.0.2.30",
    "203.0.113.35",
]

mac_addresses = [
    "00:1A:2B:3C:4D:5E",
    "00:1B:2C:3D:4E:5F",
    "00:1C:2D:3E:4F:5A",
    "00:1D:2E:3F:4A:5B",
    "00:1E:2F:3A:4B:5C",
    "00:1F:2A:3B:4C:5D",
    "00:2A:3B:4C:5D:6E",
    "00:2B:3C:4D:5E:6F",
    "00:2C:3D:4E:5F:6A",
    "00:2D:3E:4F:5A:6B",
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
]

# Generate all combinations
combinations = list(itertools.product(ip_addresses, mac_addresses, user_agents))


proxy_pool = cycle(combinations)


def get_proxy():
    return next(proxy_pool)


def scrape_links(url, depth):
    if depth > max_depth or len(visited_urls) >= max_sites:
        return

    try:
        # Generate a random user agent
        proxy = get_proxy()
        headers = {
            "User-Agent": proxy[2],
            "X-Forwarded-For": proxy[0],  # Dummy IP address
            "X-Client-MAC": proxy[1],  # Dummy MAC address
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href and href.startswith("http") and href not in visited_urls:
                visited_urls.add(href)
                print(href)
                scrape_links(href, depth + 1)
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")


# Starting URL
start_url = (
    "https://www.levelwinner.com/art-of-war-legions-guide-tips-tricks-strategies/"
)
# scrape_links(start_url, 0)


def visit_site(url, visits):

    try:
        # Generate a random user agent
        for _ in range(0, visits):
            proxy = get_proxy()
            headers = {
                "User-Agent": proxy[2],
                "X-Forwarded-For": proxy[0],  # Dummy IP address
                "X-Client-MAC": proxy[1],  # Dummy MAC address
            }
            response = requests.get(url, headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                time.sleep(60)  # Keep the connection open for 30 seconds

    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")


site_url = "https://www.youtube.com/watch?v=Qt1TLzxUvys" #"https://medium.com/@152109007c/explore-a29f7f840f0a"
visit_site(site_url, 10)
