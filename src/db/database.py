import psycopg2


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
        except Exception as _ex:
            print("[Error] Error while working with PostgreSQL", _ex)

        yield connection

        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")