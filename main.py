from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser

from config.settings import DATA_DIR

if __name__ == '__main__':
    # Load in Documents
    reader = SimpleDirectoryReader(input_dir=DATA_DIR)
    documents = reader.load_data()
    print(f'Loaded {len(documents)} documents')

    # Parse the Documents into Nodes
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)

    # Build an index over a set of Node objects directly
    index = VectorStoreIndex(nodes)

    # Query the index
    query_engine = index.as_query_engine()
    response = query_engine.query('I like rice.')

    print(response.source_nodes[0].text)
