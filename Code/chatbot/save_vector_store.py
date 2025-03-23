import pickle

def save_vector_store(vectorstore, filename):
    """
    Save Vector Store to a file

    Parameters
    ----------
    vectorstore: VectorStore
        The vector store to be saved.
    filename: str
        The filename/path where the vector store will be saved.
    """
    with open(filename, 'wb') as file:
        pickle.dump(vectorstore, file)

