import os

import pinecone

from config.settings import PINECONE_INDEX_NAME
from embeddings.openai_utils import get_vector_for_text
from recipes.io_utils import get_recipe_filepaths
from utils.files import extract_filename_without_extension, read_txt_file

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


def create_index_if_not_exists():
    """Create the given index if it does not already exist"""
    indexes = pinecone.list_indexes()

    if PINECONE_INDEX_NAME not in indexes:
        pinecone.create_index(PINECONE_INDEX_NAME, dimension=1024, metric='euclidean')


def main():
    create_index_if_not_exists()
    index = pinecone.Index(PINECONE_INDEX_NAME)

    for filepath in get_recipe_filepaths():
        recipe_id = extract_filename_without_extension(filepath)
        recipe_content = read_txt_file(filepath)
        vector = get_vector_for_text(recipe_content)
        index.upsert([(recipe_id, vector)])


if __name__ == '__main__':
    pinecone.init(api_key=PINECONE_API_KEY, environment='gcp-starter')
    main()
