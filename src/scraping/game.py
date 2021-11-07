import math
import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup


class SteamGameScraping:
    def __init__(self, genre, link):
        self.genre = genre
        self.link = link

    games_data = []

    async def connect(self):
        link = f"{self.link}/?query=&start={0}&count=15&cc=KZ&l=russian&v=4&tag={self.genre}"

        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        async with aiohttp.ClientSession() as session:
            tasks = []
            response = await session.get(url=link, headers=header)
            response_json = await response.json()
            count = math.ceil(response_json['total_count'] / 15)

            for page in range(count):
                task = asyncio.create_task(self.get_data(session, page, count))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def get_page_count(self):
        self.connect()
        with open(f"src/scraping/html/steam_{self.genre}_{0}.json") as file:
            data = json.load(file)
        count = math.ceil(data['total_count'] / 15)
        return count

    async def get_data(self, session, page, page_count):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        link = f"{self.link}/?query=&start={15 * page}&count=15&cc=KZ&l=russian&v=4&tag={self.genre}"
        async with session.get(url=link, headers=header) as response:
            response_json = await response.json()
            html = response_json['results_html']

            soup = BeautifulSoup(html, "lxml")
            game_cards = soup.find_all("a")
            for game in game_cards:
                try:
                    game_name = game.find('div', class_="tab_item_name").text.strip()
                except Exception as _ex:
                    game_name = "No name game"
                    print("[Error]", _ex)

                game_price = game.find('div', class_='discount_prices')

                try:
                    game_new_price = game_price.find('div', "discount_final_price").text.replace('₸', '').replace(' ', '')
                    game_new_price = int(game_new_price)
                except:
                    game_new_price = 0

                try:
                    game_old_price = game_price.find('div', "discount_original_price").text.replace('₸', '').replace(' ', '')
                    game_old_price = int(game_old_price)
                except:
                    game_old_price = 0

                if game_old_price == 0:
                    game_old_price = game_new_price
                    game_new_price = 0

                self.games_data.append(
                    {
                        'game_name': game_name,
                        'game_old_price': game_old_price,
                        'game_new_price': game_new_price
                    }
                )
            print(f"[INFO] scraping {page}/{page_count}")

    def parse(self):
        asyncio.run(self.connect())

        with open(f"src/scraping/result/{self.genre}/steam_game.json", "w") as file:
            json.dump(self.games_data, file, indent=4, ensure_ascii=False)
