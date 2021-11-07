import math

import requests
import json
from bs4 import BeautifulSoup


class SteamGameScraping:
    def __init__(self, genre, link):
        self.genre = genre
        self.link = link

    def connect(self, page):
        link = f"{self.link}/?query=&start={15 * page}&count=15&cc=KZ&l=russian&v=4&tag={self.genre}"

        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        response = requests.get(link, headers=header, timeout=5)
        with open(f"src/scraping/html/steam_{self.genre}_{page}.json", "w") as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)

    def get_page_count(self):
        self.connect(0)
        with open(f"src/scraping/html/steam_{self.genre}_{0}.json") as file:
            data = json.load(file)
        count = math.ceil(data['total_count'] / 15)
        return count

    def get_data(self, page):
        global game_old_price, game_new_price

        with open(f"src/scraping/html/steam_{self.genre}_{page}.json") as file:
            data = json.load(file)
        html = data['results_html']

        soup = BeautifulSoup(html, "lxml")
        game_cards = soup.find_all("a")
        games_data = []
        for game in game_cards:
            try:
                game_name = game.find('div', class_="tab_item_name").text.strip()
            except Exception as _ex:
                game_name = "No name game"
                print("[Error]", _ex)

            try:
                game_price = game.find('div', class_='discount_prices').text.strip().replace(' ', '')
                if game_price.count("₸") == 2:
                    l_index = game_price.find("₸")
                    r_index = game_price.rfind("₸")
                    game_new_price = game_price[l_index:r_index].replace('₸', '')
                    game_old_price = game_price[:l_index]
                else:
                    game_new_price = 0
                    game_old_price = game_price.replace('₸', '')
            except Exception as _ex:
                game_price = "No game price"
                print("[Error]", _ex)

            games_data.append(
                {
                    'game_name': game_name,
                    'game_old_price': game_old_price,
                    'game_new_price': game_new_price
                }
            )

        with open(f"src/scraping/result/steam_game_{self.genre}_{page}.json", "w") as file:
            json.dump(games_data, file, indent=4, ensure_ascii=False)

        #     print(game_name)
        #     print(game_old_price)
        #     print(game_new_price)
        #     print("#" * 19)
        # print(len(games_data))

    def parse(self):
        page_count = self.get_page_count()

        for i in range(page_count):
            self.connect(i)
            self.get_data(i)
            print(f"[INFO] scraping {i}/{page_count}")
