import os

from settings import DATA_DIR


def get_recipe_filepaths():
    """Retrieve a list of recipe filepaths"""
    results = []

    for file in os.listdir(DATA_DIR):
        if file.endswith('.txt'):
            results.append(DATA_DIR / file)

    return results
