import json
import logging
import os
from typing import Any

from config import themes_file_path
from language import LanguageManager
from db.UserInterestsUtils import UserInterestsUtils
from db.models import Interests
from sqlalchemy import Column, JSON


class ThemeManager:
    def __init__(self, interests_manager: UserInterestsUtils, lang_manager: LanguageManager):
        self._themes = None
        self._theme_translates = None
        self.lang_manager: LanguageManager = lang_manager
        self._first_interests = None
        self.interests_manager: UserInterestsUtils = interests_manager

    @property
    def themes(self):
        if self._themes is None:
            if os.path.exists(themes_file_path):
                with open(themes_file_path) as file:
                    file_data = file.read()

                    json_data = json.loads(file_data)

                    self._themes = json_data
            else:
                logging.info(f"File {themes_file_path} does not exist")

        return self._themes

    @themes.setter
    def themes(self, value):
        self._themes = value

    @property
    def theme_translates(self):
        if self._theme_translates is None:
            all_phrases = self.lang_manager.phrases

            countries = all_phrases.keys()

            theme_translates = {}

            for country in countries:
                country_themes = all_phrases[country]["themes"]

                theme_translates[country] = country_themes

            logging.info("Theme translates were parsed.")

            self._theme_translates = theme_translates

        return_dict: dict = self._theme_translates
        return dict(return_dict)

    @theme_translates.setter
    def theme_translates(self, value):
        self._theme_translates = value

    async def marked_themes(self, user_id: int) -> Any:
        result: Interests | None = await self.interests_manager.get(user_id)

        if result is None:
            return None

        return dict(result.interests)

    async def subscribed_themes(self, user_id: int):
        result: Interests = await self.interests_manager.get(user_id)

        if result is None:
            return None

        interests: dict = dict(result.interests)
        result_themes = {}

        for country, themes in interests.items():
            country_themes = [theme for theme, value in themes.items() if value]

            if "all" in country_themes:
                result_themes[country] = ["all"]
            elif len(country_themes) > 0:
                result_themes[country] = country_themes

        return result_themes

    async def set_interests(self, interests: dict, user_id: int):
        interests: Interests = Interests(interests=interests, user_id=user_id)
        await self.interests_manager.set(interests)

    @property
    async def first_interests(self):
        if self._first_interests is None:
            logging.info("First interests were parsed")
            user_interests = {}

            for country, themes in self.themes.items():
                null_themes: dict = {}

                for theme in themes:
                    null_themes[str(theme)] = False

                user_interests[str(country)] = null_themes

            self._first_interests = user_interests

        return self._first_interests

    @first_interests.setter
    def first_interests(self, value):
        self._first_interests = value