import requests
import json
from bs4 import BeautifulSoup


class SteamGenreScraping:
    def __init__(self, link):
        self.link = link

    def connect(self):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        response = requests.get(self.link, headers=header)

        with open("src/scraping/html/steam_store_main.html", "w") as file:
            file.write(response.text)

    @staticmethod
    def get_data():
        with open("src/scraping/html/steam_store_main.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        gutter_block = soup.find("div", class_="home_page_gutter")
        search_by_genre_block = gutter_block.find_all("div", class_="home_page_gutter_block")[1]
        genre_block = search_by_genre_block.find_all("a", class_="gutter_item")

        genre_data = []
        for genre in genre_block:
            link = genre.get("href")
            genre_link = link.replace("/?snr=1_4_4__125", "")
            genre_name = genre.text.strip()

            genre_data.append(
                {
                    "Name": genre_name,
                    "Link": genre_link
                }
            )

        return genre_data

    def create_json(self):
        genre_dict = self.get_data()

        with open("src/scraping/result/genre.json", "w") as file:
            json.dump(genre_dict, file, indent=4, ensure_ascii=False)
