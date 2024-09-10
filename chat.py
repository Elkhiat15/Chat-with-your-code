from llama_index.llms.gemini import Gemini
from llama_index.readers.github import GithubRepositoryReader
from llama_index.core import download_loader
from dotenv import load_dotenv

import os
import helper, validate

# Load environment variables from .env file
load_dotenv()

validate.validate()

github_client = validate.initialize_github_client()
download_loader("GithubRepositoryReader")

github_url = input("Please enter the GitHub repository URL: ")
owner, repo = validate.parse_github_url(github_url)

while True:
    owner, repo = validate.parse_github_url(github_url)
    if validate.validate_owner_repo(owner, repo):
        loader = GithubRepositoryReader(
            github_client,
            owner=owner,
            repo=repo,
            filter_file_extensions=(
                [".py", ".java",".js", ".cpp" ".md"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            verbose=False,
            concurrent_requests=5,
        )
        print(f"Loading {repo} repository by {owner}")
        docs = loader.load_data(branch="main")
        print("Documents uploaded:")
        for doc in docs:
            print(doc.metadata)
        break  # Exit the loop once the valid URL is processed
    else:
        print("Invalid GitHub URL. Please try again.")
        github_url = input("Please enter the GitHub repository URL: ")

print("Uploading to vector store...")

# Define the variables
model_name = "models/embedding-001"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
emb_dim=768

# Create the embedding model
embed_model = helper.create_embedding_model(model_name, GOOGLE_API_KEY)

# Create the vector store
vector_store = helper.create_vector_store(emb_dim=emb_dim)

# Create the storage context
storage_context = helper.create_storage_context(vector_store)

# Create the index
index = helper.create_index(docs, storage_context, embed_model)

# Create the query engine
query_engine = helper.create_query_engine(index, llm=Gemini())

# Test the query engine
intro_question = "What is the repository about?"
print(f"Test question: {intro_question}")
print("=" * 50)

while True:
    user_question = input("Please enter your question (or type 'exit' to quit): ")
    if user_question.lower() == "exit":
        print("Exiting, thanks for chatting!")
        break

    print(f"Your question: {user_question}")
    print("=" * 50)

    answer = query_engine.query(user_question)
    print(f"Answer: {str(answer)} \n")
