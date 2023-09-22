from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'  # directory to store our recipe text files
EMBEDDING_MODEL = 'text-similarity-ada-001'  # OpenAI embedding model
PINECONE_INDEX_NAME = 'recipes'  # name of our Pinecone index
