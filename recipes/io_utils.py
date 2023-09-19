import os

from config.settings import DATA_DIR


def get_recipes_list():
    """Retrieves the list of recipes from files in the data directory"""
    results = []

    for file in os.listdir(DATA_DIR):
        if file.endswith('.txt'):
            filepath = DATA_DIR / file

            with open(filepath, 'r') as f:
                recipe_content = f.read()
                results.append(recipe_content)

    return results
