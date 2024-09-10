
from llama_index.readers.github import GithubClient

import os 
import re

def parse_github_url(url: str):
    """
    Parse a GitHub URL and extract the owner and repository names.

    Args:
        url (str): The GitHub URL to parse.

    Returns:
        tuple: A tuple containing the owner and repository names, or (None, None) if the URL is invalid.
    """
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    return match.groups() if match else (None, None)

def validate_owner_repo(owner: str, repo: str):
    """
    Validate the owner and repository names.

    Args:
        owner (str): The owner name.
        repo (str): The repository name.

    Returns:
        bool: True if both owner and repository names are valid, False otherwise.
    """
    return bool(owner) and bool(repo)

def initialize_github_client():
    """
    Initialize a GitHub client using the GITHUB_TOKEN environment variable.

    Returns:
        object: A GitHub client object.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")
    return GithubClient(github_token)

def validate():
    """
    Validate the environment variables for Gemini API key and GitHub token.
    """
    # Check for Gemini API key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise EnvironmentError("Google API key not found in environment variables")

    # Check for GitHub Token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")
