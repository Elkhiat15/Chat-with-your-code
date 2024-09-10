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