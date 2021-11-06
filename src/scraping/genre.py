import requests
from bs4 import BeautifulSoup


class SteamGenreScraping:
    def __init__(self, link):
        self.link = link

    def connect(self):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        response = requests.get(self.link, headers=header)

        with open("src/scraping/steam_store_main.html", "w") as file:
            file.write(response.text)
