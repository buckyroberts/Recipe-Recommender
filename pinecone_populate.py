import os
from pathlib import Path

import pinecone
import promptlayer

openai = promptlayer.openai

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_INDEX_NAME = 'recipes'

pinecone.init(api_key=PINECONE_API_KEY, environment='gcp-starter')

# Create the index if it does not already exist
indexes = pinecone.list_indexes()
if PINECONE_INDEX_NAME not in indexes:
    pinecone.create_index(PINECONE_INDEX_NAME, dimension=1024, metric='euclidean')

index = pinecone.Index(PINECONE_INDEX_NAME)
recipe_filepaths = [DATA_DIR / file for file in os.listdir(DATA_DIR) if file.endswith('.txt')]

for filepath in recipe_filepaths:
    # Extract the filename without its extension from a given path
    base_name = os.path.basename(filepath)
    recipe_id, _ = os.path.splitext(base_name)

    # Read the content of a text file, convert it into a vector, insert it into the index
    with open(filepath, 'r') as file:
        recipe_content = file.read()
        response = openai.Embedding.create(
            input=recipe_content,
            engine='text-similarity-ada-001',
        )
        vector = response['data'][0]['embedding']
        index.upsert([(recipe_id, vector)])
