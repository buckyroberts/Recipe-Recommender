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
        recipe_embedding_response = openai.Embedding.create(
            input=recipe_content,
            engine='text-similarity-ada-001',
        )
        vector = recipe_embedding_response['data'][0]['embedding']
        index.upsert([(recipe_id, vector)])

food = 'chicken'

# Fetch IDs of recipes related to the given text using Pinecone
food_embedding_response = openai.Embedding.create(
    input=food,
    engine='text-similarity-ada-001',
)
vector = food_embedding_response['data'][0]['embedding']

query_results = index.query(
    vector=vector,
    top_k=2,
    include_values=True
)
recipe_ids = {i['id'] for i in query_results['matches']}

# Retrieve recipe contents for a given list of recipe IDs
recipes_list = [open(DATA_DIR / f'{recipe_id}.txt', 'r').read() for recipe_id in recipe_ids]

"""
Given a prompt and a list of recipes, use GPT to suggest one of the recipes
"""

# Fetch our template from PromptLayer
recipe_template = promptlayer.prompts.get("recipe_template")
system_content = recipe_template['messages'][0]['prompt']['template']
user_content_template = recipe_template['messages'][1]['prompt']['template']

# Set our template variables
variables = {
    'food': food,
    'recipes_string': '\n\n'.join(recipes_list)
}

response, pl_request_id = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {
            'role': 'system',
            'content': system_content
        },
        {
            'role': 'user',
            'content': user_content_template.format(**variables)
        },
    ],
    temperature=0.5,
    max_tokens=1024,
    return_pl_id=True
)
print(response.choices[0].message.content)

# Associate request with a prompt template
promptlayer.track.prompt(
    request_id=pl_request_id,
    prompt_name='recipe_template',
    prompt_input_variables=variables
)
