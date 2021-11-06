import psycopg2
import json


class DataBaseJob:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("[INFO] PostgreSQL connection successful")
            return connection
        except Exception as _ex:
            print("[Error] Error while working with PostgreSQL", _ex)

    def create_table_genres(self):
        connection = None
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE genres(
                            id serial PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            steam_link VARCHAR(255) NOT NULL
                        );
                    """
                )
                connection.commit()
            print("[INFO] Table genres created successful")
        except Exception as _ex:
            print("[ERROR] Table not created", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def create_table_games(self):
        connection = None
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE games(
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE
                        );
                    """
                )
                connection.commit()
            print("[INFO] Table games created successful")
        except Exception as _ex:
            print("[ERROR] Table not created", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def create_table_price(self):
        connection = None
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE price(
                            id SERIAL PRIMARY KEY,
                            game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
                            price_kzt MONEY,
                            date TIMESTAMP
                        );
                    """
                )
                connection.commit()
            print("[INFO] Table games created successful")
        except Exception as _ex:
            print("[ERROR] Table not created", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def parse_genre_json(self):
        connection = None
        with open("src/scraping/result/genre.json") as file:
            data = json.load(file)
        try:
            connection = self.connect()

            for genre_data in data:
                name = genre_data.get('Name')
                link = genre_data.get('Link')

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                            INSERT INTO genres (name, steam_link) VALUES
                                ('{name}', '{link}');
                        """
                    )
                    connection.commit()
                    print("[INFO] Table inserted successful")
        except Exception as _ex:
            print("[ERROR] Table not insert into", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")