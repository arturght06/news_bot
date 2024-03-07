import asyncio
import logging
from pprint import pprint

import numpy as np
import openai


async def embedding(key: str, input_text: list | str) -> list | None | bool:
    model_engine = "text-embedding-3-large"
    openai.api_key = key
    if len(input_text) == 0 or any(not isinstance(element, str) for element in input_text):
        return None

    try:
        embeddings = await openai.Embedding.acreate(
            input=input_text,
            engine=model_engine
        )
        logging.info("Got embedding using OpenAi key: {}...".format(key[:10]))
        return embeddings.data[0].embedding
    except Exception as error:
        code: str = dict(error.__dict__)['json_body']['error']['code']
        if code == 'rate_limit_exceeded':
            return None
        elif code == 'insufficient_quota':
            return False

        # raise error


async def compare_embeddings(a: list, b: list) -> float:
    similarity: float = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return similarity

