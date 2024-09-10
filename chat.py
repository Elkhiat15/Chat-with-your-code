from llama_index.llms.gemini import Gemini
from llama_index.readers.github import GithubRepositoryReader
from llama_index.core import download_loader
from dotenv import load_dotenv
import streamlit as st
import os
import helper, validate

# Load environment variables from .env file
load_dotenv()

#validate.validate()
# Create an empty container
placeholder = st.empty()

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your sectrets")
    st.markdown("[How to get Google API key](https://ai.google.dev/gemini-api/docs/api-key)")
    GOOGLE_API_KEY = st.text_input("Google API Key", type="password")
    st.markdown("[How to get  'classic' personal GitHub Token?](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)")
    GITHUB_TOKEN = st.text_input("GitHub Token", type="password")
    valid_token = False
    if GITHUB_TOKEN:
        try:
            github_client = validate.initialize_github_client(GITHUB_TOKEN)
            valid_token = True
        except :
            st.write("Please, Enter a valid GitHub Token")

    submit = st.form_submit_button("Add")

if submit and GOOGLE_API_KEY and valid_token: 
    placeholder.empty()
    st.success("Added successful")
else:
    pass

GITHUB_TOKEN = "HAMADA"
github_client = validate.initialize_github_client(GITHUB_TOKEN)
            
download_loader("GithubRepositoryReader")

github_url = input("Please enter the GitHub repository URL: ")
owner, repo = validate.parse_github_url(github_url)

while True:
    owner, repo = validate.parse_github_url(github_url)
    if validate.validate_owner_repo(owner, repo):
        try:
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
        except:
            #TODO: ask the user to re enter a token 
            print("TOKEN ERROR\n\n$$$$$$$$$$$$$$$$$$$$\n\n")
            GITHUB_TOKEN = input("Please enter the GitHub TOKEN: ")
            github_client = validate.initialize_github_client(GITHUB_TOKEN)
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
