from llama_index.llms.gemini import Gemini
import helper

def get_query_engine(GOOGLE_API_KEY, docs):
    """
        Creates and returns a query engine instance.

        Parameters:
        - GOOGLE_API_KEY (str): The Google API key to use for creating the embedding model.
        - docs (list): A list of documents to index.

        Returns:
        - query_engine: An instance of the query engine, ready to be used for querying.

        Notes:
        - This function creates an embedding model, a vector store, a storage context, and an index,
        and then uses these components to create a query engine instance.
        - The Gemini LLM is used as the language model for the query engine.
    """
    # Define the variables
    model_name = "models/embedding-001"
    emb_dim=768

    # Create the embedding model
    embed_model = helper.create_embedding_model(model_name, GOOGLE_API_KEY)

    # Create the vector store
    vector_store = helper.create_vector_store(emb_dim=emb_dim)

    # Create the storage context
    storage_context = helper.create_storage_context(vector_store)

    # Create the index
    index = helper.create_index(docs, storage_context, embed_model)

    # Create then return the query engine
    query_engine = helper.create_query_engine(index, llm=Gemini())
    return query_engine
