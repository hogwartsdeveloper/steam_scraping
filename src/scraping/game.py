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

    async def get_data(self, session, page, page_count):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        link = f"{self.link}/?query=&start={15 * page}&count=15&cc=KZ&l=russian&v=4&tag={self.genre}"
        async with session.get(url=link, headers=header) as response:
            if response.status == 200:
                response_json = await response.json(content_type=False)
            else:
                response_json = None
                print(f"[ERROR] Wrong {response.status}")
            html = response_json['results_html']

            soup = BeautifulSoup(html, "lxml")
            game_cards = soup.find_all("a")
            for game in game_cards:
                try:
                    game_name = game.find('div', class_="tab_item_name").text.strip()
                    if "'" in game_name:
                        game_name = game_name.replace("'", "")
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

        with open(f"src/scraping/result/steam_game{self.genre}.json", "w") as file:
            json.dump(self.games_data, file, indent=4, ensure_ascii=False)
