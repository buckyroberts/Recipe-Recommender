import os

import promptlayer

openai = promptlayer.openai
openai.api_key = os.getenv('OPENAI_API_KEY')


def add_recipes_to_prompt(prompt, recipes_list):
    """Combines the given prompt with the list of recipes to form a single string"""
    recipes_string = '\n\n'.join(recipes_list)
    results = prompt + '\n\n' + recipes_string
    return results


def suggest_final_recipe(prompt, recipes_list):
    """Given a prompt and a list of recipes, use GPT to suggest one of the recipes"""
    prompt_with_recipes = add_recipes_to_prompt(prompt, recipes_list)
    response = openai.ChatCompletion.create(
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
            {'role': 'user', 'content': prompt_with_recipes},
        ],
        temperature=0.5,
        max_tokens=1024
    )
    print(response.choices[0].message.content)
