import json
import logging
import time

from sqlalchemy import Column, String, BigInteger, Boolean, JSON, ARRAY, Double
from sqlalchemy.orm import declarative_base
from typing import TypedDict
from db.connect import engine
from typing import Type

Base: Type = declarative_base()


# class UserInfo(TypedDict, total=False):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     language_code: str


class User(Base):
    __tablename__ = 'User'

    id: Column[int] = Column(BigInteger, primary_key=True, index=True)
    username: Column[str] = Column(String(length=100), index=True)
    first_name: Column[str] = Column(String(length=100), index=True)
    last_name: Column[str] = Column(String(length=100), index=True)
    language_code: Column[str] = Column(String(length=16), index=True)


class UserLanguage(Base):
    __tablename__ = 'User_languages'

    id: Column[int] = Column(BigInteger, primary_key=True)
    language_code: Column[str] = Column(String(length=16), default="en")
    translate_posts: Column[bool] = Column(Boolean(), default=False)
    language_interface: Column[str] = Column(String(length=16), default="en")
    language_translate: Column[str] = Column(String(length=16), default="en")


class Post(Base):
    __tablename__ = 'Post'

    id: Column[str] = Column(String, primary_key=True)
    channel_id: Column[int] = Column(BigInteger)
    post_id: Column[int] = Column(BigInteger)
    text: Column[str] = Column(String)
    processed: Column[bool] = Column(Boolean)
    creation_time: Column[int] = Column(BigInteger)
    # advertisement: Column[bool] = Column(Boolean)
    # lang: Column[str] = Column(String(length=16))
    # theme: Column[str] = Column(String)


class Interests(Base):
    __tablename__ = 'Interests'

    user_id: Column[int] = Column(BigInteger, primary_key=True)
    interests: Column[json] = Column(JSON)


class TgChannel(Base):
    __tablename__ = 'Tg_Channel'

    id: Column[int] = Column(BigInteger, primary_key=True, index=True)
    access_hash: Column[int] = Column(BigInteger, index=True)
    title: Column[str] = Column(String, index=True)
    last_post_id: Column[int] = Column(BigInteger, index=True)
    username: Column[str] = Column(String, index=True)
    participants_count: Column[int] = Column(BigInteger, index=True)
    accepted: Column[bool] = Column(Boolean, default=False, index=True)


class PostTranslates(Base):
    __tablename__ = 'Post_Translates'

    id: Column[str] = Column(String, primary_key=True)
    text: Column[str] = Column(String)
    translates: Column[JSON] = Column(JSON)


class PostRegion(Base):
    __tablename__ = 'Post_Region'

    id: Column[str] = Column(String, primary_key=True)
    region: Column[str] = Column(String)


class PostTheme(Base):
    __tablename__ = 'Post_Theme'

    id: Column[str] = Column(String, primary_key=True)
    theme: Column[str] = Column(String)


class AnalyzeProcess(Base):
    __tablename__ = 'Analyze_Process'

    id: Column[str] = Column(String, primary_key=True)
    translate: Column[bool] = Column(Boolean, default=False)
    embedding: Column[bool] = Column(Boolean, default=False)
    theme_id: Column[bool] = Column(Boolean, default=False)
    region: Column[bool] = Column(Boolean, default=False)
    theme: Column[bool] = Column(Boolean, default=False)


class TextEmbedding(Base):
    __tablename__ = 'Text_Embedding'

    id: Column[str] = Column(String, primary_key=True)
    embedding: Column[list] = Column(ARRAY(Double), default=None)


class UniqueThemeId(Base):
    __tablename__ = 'Unique_Theme_Id'

    id: Column[str] = Column(String, primary_key=True)
    creation_time: Column[int] = Column(BigInteger, default=int(time.time()))
    post_ids: Column[list] = Column(ARRAY(BigInteger), default=None)


class OpenAiKey(Base):
    __tablename__ = 'Open_Ai_Key'

    key: Column[str] = Column(String, primary_key=True)
    taking_time: Column[int] = Column(BigInteger, default=int(time.time()))
    unusable: Column[bool] = Column(Boolean, default=False)


async def create_tables():
    async with engine.begin() as conn:
        logging.info("Tables were created")
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# def create_tables(engine):
#     Base.metadata.create_all(engine)
