from src.db.database import DataBaseJob
from src.scraping.genre import SteamGenreScraping
from src.scraping.game import SteamGameScraping
from src.db.config import host, user, password, db_name


def main():
    db = DataBaseJob(host, user, password, db_name)
    genres = db.get_genre()
    for genre in genres:
        if "Free to Play" not in genre and "Early Access" not in genre:
            game = SteamGameScraping(*genre,
                                     "https://store.steampowered.com/contenthub/querypaginated/tags/TopSellers/render")
            game.parse()
            break


if __name__ == '__main__':
    main()
