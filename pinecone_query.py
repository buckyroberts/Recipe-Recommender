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
food = 'chicken'
index = pinecone.Index(PINECONE_INDEX_NAME)

# Fetch IDs of recipes related to the given text using Pinecone
embedding_response = openai.Embedding.create(
    input=food,
    engine='text-similarity-ada-001',
)
vector = embedding_response['data'][0]['embedding']

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
recipe_template = promptlayer.prompts.get('recipe_template')
recipe_template_template = recipe_template['template']

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
            'content': (
                'You are a helpful assistant. '
                'Given some user input and a list of recipes, suggest one of the recipes. '
                'The final output should be the full recipe.'
            )
        },
        {
            'role': 'user',
            'content': recipe_template_template.format(**variables)
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
