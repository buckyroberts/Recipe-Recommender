import os

from config.settings import DATA_DIR
from utils.files import read_txt_file


def get_recipe_filepaths():
    """Retrieve a list of recipe filepaths"""
    results = []

    for file in os.listdir(DATA_DIR):
        if file.endswith('.txt'):
            results.append(DATA_DIR / file)

    return results


def get_recipes_list():
    """Retrieves the list of recipes from files in the data directory"""
    results = []

    for filepath in get_recipe_filepaths():
        recipe_content = read_txt_file(filepath)
        results.append(recipe_content)

    return results
