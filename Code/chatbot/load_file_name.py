import pickle

def load_vector_store(filename):
    """
    Load Vector Store from a file

    Parameters
    ----------
    filename: str
        The filename/path from where the vector store will be loaded.

    Returns
    -------
    VectorStore
        The loaded vector store.
    """
    with open(filename, 'rb') as file:
        vectorstore = pickle.load(file)
    return vectorstore