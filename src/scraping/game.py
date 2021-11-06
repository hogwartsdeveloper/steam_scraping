import requests
from bs4 import BeautifulSoup


class SteamGameScraping:
    def __init__(self, genre, link):
        self.genre = genre
        self.link = link

    def connect(self):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        response = requests.get(self.link + "#p=0&tab=TopSellers", headers=header)

        with open(f"src/scraping/html/steam_{self.genre}.html", "w") as file:
            file.write(response.text)
