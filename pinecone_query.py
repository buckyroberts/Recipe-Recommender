import os

import pinecone

from config.settings import DATA_DIR, PINECONE_INDEX_NAME
from embeddings.openai_utils import get_vector_for_text
from recipes.suggestion import suggest_final_recipe
from utils.files import read_txt_file

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


def get_recipes_from_ids(recipe_ids):
    """Retrieve recipe contents for a given list of recipe IDs"""
    results = []
    filepaths = {DATA_DIR / f'{recipe_id}.txt' for recipe_id in recipe_ids}

    for filepath in filepaths:
        content = read_txt_file(filepath)
        results.append(content)

    return results


def get_related_recipe_ids_for_text(text):
    """Fetch IDs of recipes related to the given text using Pinecone"""
    index = pinecone.Index(PINECONE_INDEX_NAME)
    vector = get_vector_for_text(text)
    query_results = index.query(
        vector=vector,
        top_k=2,
        include_values=True
    )
    return {i['id'] for i in query_results['matches']}


def main():
    prompt = 'I like chicken.'
    recipe_ids = get_related_recipe_ids_for_text(prompt)
    recipes_list = get_recipes_from_ids(recipe_ids)
    suggest_final_recipe(prompt, recipes_list)


if __name__ == '__main__':
    pinecone.init(api_key=PINECONE_API_KEY, environment='gcp-starter')
    main()
