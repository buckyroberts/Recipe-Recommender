import openai

from config.settings import EMBEDDING_MODEL


def get_vector_for_text(text):
    response = openai.Embedding.create(
        input=text,
        engine=EMBEDDING_MODEL,
    )
    return response['data'][0]['embedding']
