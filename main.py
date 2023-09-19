from config.settings import DATA_DIR
from embeddings.llama import build_index_from_documents, load_documents_from_directory, query_index, sort_nodes_by_score
from recipes.suggestion import suggest_final_recipe


def get_top_recipes(prompt):
    """Given a prompt, retrieves and ranks recipes based on their relevance to the prompt"""
    documents = load_documents_from_directory(input_dir=DATA_DIR)
    index = build_index_from_documents(documents)
    response = query_index(index, prompt)
    return sort_nodes_by_score(response.source_nodes)


def main():
    prompt = 'I like fish.'
    recipes_list = get_top_recipes(prompt)
    suggest_final_recipe(prompt, recipes_list)


if __name__ == '__main__':
    main()
