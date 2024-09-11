from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.storage.storage_context import StorageContext
from dotenv import load_dotenv

import faiss

# Load environment variables from .env file
load_dotenv()


def create_embedding_model(model_name: str, api_key: str):
    """
    Create a Gemini embedding model instance.

    Args:
        model_name (str): The name of the embedding model.
        api_key (str): The Google API key.

    Returns:
        object: A Gemini embedding model instance.
    """
    return GeminiEmbedding(model_name=model_name, api_key=api_key)

def create_vector_store(emb_dim: int):
    """
    Create a Faiss vector store instance.

    Args:
        emb_dim (int): The embedding dimension.

    Returns:
        object: A Faiss vector store instance.
    """
    faiss_index = faiss.IndexFlatL2(emb_dim)
    return FaissVectorStore(faiss_index=faiss_index)

def create_storage_context(vector_store: object):
    """
    Create a storage context instance.

    Args:
        vector_store (object): The Faiss vector store instance.

    Returns:
        object: A storage context instance.
    """
    return StorageContext.from_defaults(vector_store=vector_store)

def create_index(docs: list, storage_context: object, embed_model: object):
    """
    Create a vector store index instance.

    Args:
        docs (list): The list of documents.
        storage_context (object): The storage context instance.
        embed_model (object): The Gemini embedding model instance.

    Returns:
        object: A vector store index instance.
    """
    return VectorStoreIndex.from_documents(
        docs,
        storage_context=storage_context,
        embed_model=embed_model
    )

def create_query_engine(index: object, llm: object):
    """
    Create a query engine instance.

    Args:
        index (object): The vector store index instance.
        llm (object): The language model instance.

    Returns:
        object: A query engine instance.
    """
    return index.as_query_engine(llm=llm)
