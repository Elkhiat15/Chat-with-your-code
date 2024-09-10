from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core import download_loader
from dotenv import load_dotenv

import faiss
import re
import os

def parse_github_url(url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    return match.groups() if match else (None, None)

def validate_owner_repo(owner, repo):
    return bool(owner) and bool(repo)

def initialize_github_client():
    github_token = os.getenv("GITHUB_TOKEN")
    return GithubClient(github_token)

def validate():
    # Check for Gemini API key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise EnvironmentError("Google API key not found in environment variables")

    # Check for GitHub Token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")

load_dotenv()
validate()

github_client = initialize_github_client()
download_loader("GithubRepositoryReader")

github_url = input("Please enter the GitHub repository URL: ")
owner, repo = parse_github_url(github_url)

while True:
    owner, repo = parse_github_url(github_url)
    if validate_owner_repo(owner, repo):
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


model_name = "models/embedding-001"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
embed_model = GeminiEmbedding(
    model_name=model_name, api_key=GOOGLE_API_KEY
)

# ====== Create vector store and upload data ======
emb_dim = 768 
faiss_index = faiss.IndexFlatL2(emb_dim)
vector_store = FaissVectorStore(faiss_index=faiss_index )

storage_context = StorageContext.from_defaults(vector_store=vector_store )
index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context,
    embed_model = embed_model)
query_engine = index.as_query_engine(llm= Gemini())

# Include a simple question to test.
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