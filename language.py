import json
import logging
import os

from sqlalchemy import Column

from db.UserLanguageUtils import UserLanguageUtils
from db.models import UserLanguage

folder_path = "lang_phrases"
country_to_emoji_file = "country_to_emoji.txt"
country_to_long_file = "country_to_name.json"


class LanguageManager:
    """language manager for user interface"""
    def __init__(self, user_lang_manager: UserLanguageUtils):
        self.user_lang_manager: UserLanguageUtils = user_lang_manager
        logging.info("> Start initializing LanguageManager object")
        self._langs = None
        self._lang_files = None
        self._phrases = None
        self._country_to_emoji = None
        self._country_to_name = None

    @property
    def country_to_name(self):
        if self._country_to_name is None:
            if os.path.exists(country_to_long_file):
                with open(country_to_long_file, encoding="utf8") as file:
                    file_data = file.read()

                    json_data = json.loads(file_data)

                    self._country_to_name = json_data
            else:
                logging.info(f"File {country_to_long_file} does not exist")

        return self._country_to_name

    @country_to_name.setter
    def country_to_name(self, value):
        self._country_to_name = value

    @property
    def country_to_emoji(self):
        if self._country_to_emoji is None:
            file_path = folder_path + "\\" + country_to_emoji_file
            # check if folder exists
            if os.path.exists(file_path):
                with open(file_path, encoding="utf8") as file:
                    file_data = file.read()

                    country_to_emoji = {}
                    file_data = file_data.split("\n")

                    for line in file_data:
                        name, flag = line.split("=")

                        country_to_emoji[name] = flag

                    self._country_to_emoji = country_to_emoji
                    logging.info(f"File {file_path} was parsed.")
            else:
                logging.info(f"[!!!] File {file_path} does not exist.")

        return self._country_to_emoji

    @country_to_emoji.setter
    def country_to_emoji(self, value):
        self._country_to_emoji = value

    @property
    def phrases(self):
        """Get all phrases from language json files to variable phrases"""
        if self._phrases is None:
            # check if folder exists
            if os.path.exists(folder_path):
                # contain all local phrases
                phrases = {}
                # read all files to get phrases from lang config files
                for lang_file in self.lang_files:
                    file_lang_path = f"{folder_path}/{lang_file}"
                    lang = lang_file.split(".")[0]
                    # read file and parse phrases
                    with open(file_lang_path, encoding="utf8") as file:
                        file_data = file.read()
                        json_data = json.loads(file_data)

                        phrases[lang] = json_data

                self._phrases = phrases
                logging.info("Phrases in different languages were parsed.")
            else:
                logging.info("File does not exist.")

        return self._phrases

    @phrases.setter
    def phrases(self, value):
        self._phrases = value

    @property
    def langs(self):
        if self._langs is None:
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)

                self._langs = [lang.split(".")[0] for lang in files if lang.endswith(".json")]
            else:
                logging.info(f"Folder {folder_path} does not exist.")

        return self._langs

    @langs.setter
    def langs(self, value):
        self._langs = value

    @property
    def lang_files(self):
        if self._lang_files is None:
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)

                self._lang_files = [lang for lang in files if lang.endswith(".json")]
                self.langs = [lang.split(".")[0] for lang in self._lang_files]

                logging.info("Were found these language config files: {}".format(self.langs))

            else:
                logging.info(f"Folder {folder_path} does not exist.")

        return self._lang_files

    @lang_files.setter
    def lang_files(self, value):
        self._lang_files = value

    async def set_user_interface_language(self, user_id: int, new_lang: str) -> None:
        if new_lang in self.langs:
            insert_data: UserLanguage = UserLanguage(id=user_id, language_interface=new_lang)
        else:
            insert_data: UserLanguage = UserLanguage(id=user_id, language_interface="en")

        await self.user_lang_manager.set(insert_data)

    async def get_user_interface_language(self, user_id: int) -> str | bool:
        current_languages: UserLanguage = await self.user_lang_manager.get(user_id)

        if current_languages is None:
            return False
        else:
            return str(current_languages.language_interface)
