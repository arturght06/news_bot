import psycopg2
from database.dbconfig import load_config
import logging


class PostgresConnector:
    # initialise object with required for connecting variables
    def __init__(self):
        self.connector = None
        self.cursor = None
        self.config = load_config()

        self.connect_db()

    def __call__(self):
        return self.connector, self.cursor

    # Connect to the PostgresSQL database server
    def connect_db(self):
        try:
            # connecting to the PostgresSQL server
            with psycopg2.connect(**self.config) as connector:
                logging.info('Connected to the PostgresSQL server.')

                self.connector = connector
                self.cursor = self.connector.cursor()

        except (psycopg2.DatabaseError, Exception) as error:
            logging.error(error)
