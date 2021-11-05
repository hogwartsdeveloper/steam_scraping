import psycopg2


class DataBaseJob:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

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

    def create_table_genre(self):
        try:
            with self.connect().cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE genres(
                            genre_id SERIAL PRIMARY KEY,
                            name VARCHAR(50) NOT NULL);
                    """
                )
            print("[INFO] Table genres created successful")
        except Exception as _ex:
            print("[ERROR] Table not created", _ex)
