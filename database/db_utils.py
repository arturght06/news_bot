from database.connect import PostgresConnector
import logging
from psycopg2 import IntegrityError


class DBUtils:
    def __init__(self):
        logging.info("> Start initializing DBUtils object")

        db_connector = PostgresConnector()
        self.connector, self.cursor = db_connector()
        self.tables = None

        self.start()

    def start(self):
        self.create_tables()
        self.refresh_list_tables()

    # create tables before starting program
    def create_tables(self):
        # Creation table command
        create_commands = {
            "channels": """CREATE TABLE IF NOT EXISTS channels(
                id SERIAL BIGINT UNIQUE PRIMARY KEY,
                access_hash BIGINT NOT NULL UNIQUE,
                username VARCHAR (100),
                title VARCHAR (200),
                subscribers_count INTEGER,
                creation_date TIMESTAMP,
                has_link BOOL,
                join_request BOOL,
                last_post_id INTEGER,
                last_post_time TIMESTAMP,
                last_post_text VARCHAR (16000)
                ) """,
            "users": """CREATE TABLE IF NOT EXISTS users(
                id BIGINT UNIQUE PRIMARY KEY,
                username VARCHAR (255),
                first_name VARCHAR (255),
                last_name VARCHAR (255),
                language_code VARCHAR (16)
                ) """,
            "user_languages": """CREATE TABLE IF NOT EXISTS user_languages(
                id BIGINT UNIQUE PRIMARY KEY,
                language_code VARCHAR (16),
                translate_posts BOOL,
                language_interface VARCHAR (16),
                language_translate VARCHAR (16)
                )""",
            # "user_translates": """CREATE TABLE IF NOT EXISTS post_translates(
            #     id SERIAL UNIQUE PRIMARY KEY,
            #     language_code VARCHAR (16),
            #     translate_posts BOOL,
            #     language_interface VARCHAR (16),
            #     language_translate VARCHAR (16)
            #     )""",
            "posts": """CREATE TABLE IF NOT EXISTS posts(
                id SERIAL BIGINT UNIQUE PRIMARY KEY,
                channel_id BIGINT NOT NULL,
                post_id INT,
                text VARCHAR (10000),
                status BOOL,
                advertisement BOOL,
                lang VARCHAR (16),
                theme_id INT,
                creation_time BIGINT
                )"""
        }

        for table_name, table_creation_command in create_commands.items():
            self.start_table(table_name, table_creation_command)

    # create table if it does not exist
    def start_table(self, table_name: str, creation_command: str):
        # make request for checking if table exists
        self.cursor.execute("select exists(select * from information_schema.tables where table_name=%s)",
                            (table_name.lower(),))
        # receive answer
        is_table_exists = self.cursor.fetchone()[0]

        # check if table does not exist
        if not is_table_exists:
            logging.info('Table {} - does not exist'.format(table_name.upper()))

            # make request for creating table
            self.cursor.execute(creation_command)
            logging.info('Table {} - created'.format(table_name.upper()))

            # transaction commit
            self.connector.commit()
        else:
            logging.info("Table {} - already exists".format(table_name.upper()))

    # remove table from db
    def drop_table(self, table_name):
        try:
            # check if table exists
            if table_name.lower() not in self.tables:
                logging.info("Table {} does not exists (it can`t be deleted)".format(table_name.upper()))
                return 0

            # drop table from db
            command = "DROP TABLE {};".format(table_name)
            self.cursor.execute(command)
            self.connector.commit()

            logging.warning("[!!!] Table {} was dropped".format(table_name.upper()))

        except Exception as error:
            logging.error(error)

            return error

    # refresh attribute with list of existing tables at db
    def refresh_list_tables(self):
        # command to receive all tables from db
        command = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"

        self.cursor.execute(command)
        tables = self.cursor.fetchall()

        logging.info("Received list of tables")

        # convert received list to readable
        self.tables = [item[0] for item in tables]

    def list_all_users(self):
        command = "SELECT * FROM users;"

        self.cursor.execute(command)

        all_users_list = self.cursor.fetchall()
        return all_users_list

    # "user_languages": """CREATE TABLE IF NOT EXISTS user_languages(
    #     id SERIAL UNIQUE PRIMARY KEY,
    #     language_code VARCHAR (16),
    #     translate_posts BOOL,
    #     language_interface VARCHAR (16),
    #     language_translate VARCHAR (16)

    def set_user_languages(self, data):
        insert_data = {
            "table_name": "user_languages",
            "id": int(data[0]),
            "language_code": data[1],
            "translate_posts": data[2],
            "language_interface": data[3],
            "language_translate": data[4]
        }

        self.add_line_to_table(insert_data)

    # add or update info about user at table users
    # receive tuple data with this structure: (id, username, first name, last name, lang code)
    def add_user(self, data):
        insert_data = {
            "table_name": "users",
            "id": int(data[0]),
            "username": data[1],
            "first_name": data[2],
            "last_name": data[3],
            "language_code": data[4]
        }

        self.add_line_to_table(insert_data)

    # add line of insert data to table
    def add_line_to_table(self, insert_data: dict):
        unique_id = insert_data["id"]
        table_name = insert_data["table_name"]

        insert_data.pop("table_name")

        try:
            # check if line already exists
            line_exists = self.get_line_from_table(table_name, unique_id)

            if line_exists is None:
                # log
                logging.info("ADD new line with id: {} to {}".format(unique_id, table_name))
                # tuples of insert data dict
                keys = tuple(insert_data.keys())
                values = tuple(insert_data.values())
                # make strings for making sql request
                request_values = "%s,"*(len(insert_data) - 1) + "%s"
                request_keys = str(', '.join(keys))

                command = ("INSERT INTO {table_name}({keys}) "
                           "VALUES ({values});".format(table_name=table_name, keys=request_keys, values=request_values))

                self.cursor.execute(command, values)

            else:
                insert_data.pop("id")
                # get list of keys of insert data
                keys = list(insert_data.keys())
                values = tuple(insert_data.values())
                # start making command
                command = f"UPDATE {table_name} SET {'=%s, '.join(keys)}=%s WHERE id={unique_id};"

                self.cursor.execute(command, values)
                logging.info("UPDATE line with id: {} at {}".format(unique_id, table_name))

            self.connector.commit()

        except IntegrityError as error:
            logging.info("line with id: {}, at {} already exists".format(unique_id, table_name))

        except Exception as error:
            logging.error(error)
            return 0

    def get_line_from_table(self, table_name, unique_id):
        try:
            command = "SELECT * FROM {} WHERE id=%s".format(table_name)

            self.cursor.execute("ROLLBACK")
            self.connector.commit()

            self.cursor.execute(command, (unique_id,))
            answer_data = self.cursor.fetchone()

            if answer_data is not None:
                logging.info("received data from table:{} with id: {}".format(table_name.upper(), unique_id))

                return answer_data
            else:
                logging.info("line with id: {} does not exists at {}".format(unique_id, table_name.upper()))

                return None

        except Exception as error:
            logging.error(error)
            return error

    def user_exists(self, user_id):
        result = self.get_line_from_table("users", user_id)

        if result is not None:
            return True
        else:
            return False


if __name__ == '__main__':
    db_utils = DBUtils()

# cur.execute()
#
# values = (40779159, 12828, 'titeafsk', 4, 1293930, True, True, 4)
#
# cur.execute("""INSERT INTO channels(id, access_hash, username, title, logo_id, verified, has_link, count_subs)
# VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""", values)
