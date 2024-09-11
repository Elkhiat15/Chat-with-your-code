from llama_index.llms.gemini import Gemini
from llama_index.readers.github import GithubRepositoryReader
from llama_index.core import download_loader
import streamlit as st
import  validate, engine
from css_styles import css, bot_template, user_template

if "load" not in st.session_state:
    st.session_state.load = False

if "started" not in st.session_state:
    st.session_state.started = False

if "GITHUB_TOKEN" not in st.session_state:
    st.session_state.GITHUB_TOKEN = ""

if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = ""

if "docs" not in st.session_state:
    st.session_state.docs = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown(css, unsafe_allow_html=True)


# ========= Show the form to take API and Token ==========
if not st.session_state.load:
    placeholder = st.empty()

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your sectrets")
        st.markdown("[How to get Google API key](https://ai.google.dev/gemini-api/docs/api-key)")
        st.session_state.GOOGLE_API_KEY = st.text_input("Google API Key", type="password")
        st.markdown("[How to get  'classic' personal GitHub Token?](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)")
        st.session_state.GITHUB_TOKEN = st.text_input("GitHub Token", type="password")
        submit = st.form_submit_button("Add")

    if submit and st.session_state.GOOGLE_API_KEY and st.session_state.GITHUB_TOKEN: 
        placeholder.empty()
        st.success("Added successful")
        with st.spinner("Loading Github Repository Reader"):
            download_loader("GithubRepositoryReader")
        st.session_state.load = True
    else:
        pass    

   
         
if st.session_state.load and not st.session_state.started:
    github_url = st.text_input("Enter repo URL") 
    if github_url:
        github_client = validate.initialize_github_client(st.session_state.GITHUB_TOKEN)
        owner, repo = validate.parse_github_url(github_url)
        if validate.validate_owner_repo(owner, repo):
            try:
                with st.spinner("Loading your Repo"):
                    st.session_state.docs = validate.load_repo(github_client, owner, repo)
            except:
                st.error("Please, refresh the page and enter a valid GitHub Token")
        else:
            st.error("Invalid GitHub URL. Please try again.")
            #github_url = input("Please enter the GitHub repository URL: ")

      # Create the query engine
        if st.session_state.docs:
            try:
                with st.spinner("Preparing your engine"):
                    if "query_engine" not in st.session_state:
                        st.session_state.query_engine =engine.get_query_engine(st.session_state.GOOGLE_API_KEY, st.session_state.docs)
                    st.session_state.started = True
            except:
                st.error("Please, Refresh the page and enter a valid Google API key")
            
if st.session_state.started:
    _,c,_ = st.columns(spec=[1,5,1])
    c.subheader(":blue[Enter your question]")
    user_question = c.text_input("Enter your question:", label_visibility="collapsed")
    if user_question!="":
        # Get the answer to the user's question
        answer = st.session_state.query_engine.query(user_question)
        # Update the chat history
        st.session_state.chat_history.append(("User", user_question))
        st.session_state.chat_history.append(("Bot", answer))

        with st.container(border=True, height=700):    
            for speaker, message in st.session_state.chat_history:
                if speaker == "User":
                    st.write(user_template.replace("{{MSG}}", message),
                        unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", f"\n\n{message}\n\n"),
                            unsafe_allow_html=True)
    else:
        st.session_state.chat_history = []