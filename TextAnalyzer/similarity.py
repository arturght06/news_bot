import time

from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
import numpy as np

# Загрузка предварительно обученной модели Word2Vec
model_path = "GoogleNews-vectors-negative300.bin"
model = KeyedVectors.load_word2vec_format(model_path, binary=True)

text = "This is an example sentence."
tokens = word_tokenize(text.lower())
word_embeddings = [model[token] for token in tokens if token in model]

print(tokens)
print(word_embeddings)


def get_text_embedding(text):
    # Токенизация текста
    tokens = word_tokenize(text.lower())

    # Получение векторных представлений для каждого токена
    word_embeddings = [model[token] for token in tokens if token in model]

    # Усреднение векторов
    if word_embeddings:
        text_embedding = np.mean(word_embeddings, axis=0)
        return text_embedding
    else:
        return None

def calculate_similarity(text1, text2):
    # Получение векторных представлений для каждого текста
    embedding1 = get_text_embedding(text1)
    embedding2 = get_text_embedding(text2)

    if embedding1 is not None and embedding2 is not None:
        # Вычисление косинусного сходства между векторами
        similarity_score = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity_score
    else:
        return None

# Пример использования
text1 = "This is an example sentence."
text2 = "It is not possible to compute similarity. Make sure you have a pre-trained model"

start = time.time()
similarity = calculate_similarity(text1, text2)
print("Time for calculating: ", start - time.time())

if similarity is not None:
    print(f"Сходство между текстами: {similarity:.4f}")
else:
    print("Невозможно вычислить сходство. Убедитесь, что у вас есть предварительно обученная модель Word2Vec и тексты содержат поддерживаемые токены.")


# Вычисление косинусного сходства
# similarity = cosine_similarity([vec1], [vec2])[0][0]
