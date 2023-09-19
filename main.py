import os

import openai

from config.settings import RECIPES_DIR


def add_recipes_to_prompt(prompt):
    """Combines the given prompt with the list of recipes to form a single string"""
    recipes_list = get_recipes_list()
    recipes_string = '\n\n'.join(recipes_list)
    results = prompt + '\n\n' + recipes_string
    return results


def get_recipes_list():
    """Retrieves the list of recipes from files in the recipes directory"""
    results = []

    for file in os.listdir(RECIPES_DIR):
        if file.endswith('.txt'):
            filepath = RECIPES_DIR / file

            with open(filepath, 'r') as f:
                recipe_content = f.read()
                results.append(recipe_content)

    return results


def suggest_final_recipe(prompt):
    """Given a prompt and a list of recipes, use GPT to suggest one of the recipes"""
    prompt_with_recipes = add_recipes_to_prompt(prompt)
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


if __name__ == '__main__':
    _prompt = 'I like rice.'
    suggest_final_recipe(_prompt)
