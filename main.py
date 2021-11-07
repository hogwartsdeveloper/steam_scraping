from src.db.database import DataBaseJob
from src.scraping.genre import SteamGenreScraping
from src.scraping.game import SteamGameScraping
from src.db.config import host, user, password, db_name


def main():
    db = DataBaseJob(host, user, password, db_name)
    db.create_table_genres()
    db.create_table_games()
    db.create_table_price()

    genre = SteamGenreScraping("https://store.steampowered.com/")
    genre.connect()
    genre.get_data()
    genre.create_json()
    db.parse_genre_json()

    genres = db.get_genre()
    for genre in genres:
        if "Free to Play" not in genre and "Early Access" not in genre:
            game = SteamGameScraping(*genre,
                                     "https://store.steampowered.com/contenthub/querypaginated/tags/TopSellers/render")
            game.parse()
            db.parse_game_json(*genre)
            db.parse_price_json(*genre)


if __name__ == '__main__':
    main()
