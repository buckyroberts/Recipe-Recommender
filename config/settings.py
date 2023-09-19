from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# Application constants
EMBEDDING_MODEL = 'text-similarity-ada-001'
PINECONE_INDEX_NAME = 'recipes'
