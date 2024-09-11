from llama_index.llms.gemini import Gemini
import helper

def get_query_engine(GOOGLE_API_KEY, docs):
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
