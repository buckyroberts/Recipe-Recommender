from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser


def build_index_from_documents(documents):
    """Creates a VectorStoreIndex from a list of documents using a default node parser"""
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index


def load_documents_from_directory(input_dir):
    """Loads all documents from a specified directory using the SimpleDirectoryReader"""
    reader = SimpleDirectoryReader(input_dir=input_dir)
    documents = reader.load_data()
    return documents


def query_index(index, query_text):
    """Queries a given VectorStoreIndex with specified text and returns the response"""
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return response


def sort_nodes_by_score(nodes):
    """Sorts a list of nodes in descending order based on their scores and returns the sorted node texts"""
    sorted_nodes = sorted(nodes, key=lambda x: x.score, reverse=True)
    return [node.text for node in sorted_nodes]
