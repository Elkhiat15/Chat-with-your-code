import streamlit as st 

# Create an empty container
placeholder = st.empty()

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your sectrets")
    st.markdown("[How to get Google API key](https://ai.google.dev/gemini-api/docs/api-key)")
    GOOGLE_API_KEY = st.text_input("Google API Key", type="password")
    st.markdown("[How to get  'classic' personal GitHub Token?](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)")
    GITHUB_TOKEN = st.text_input("GitHub Token", type="password")
    submit = st.form_submit_button("Add")

if submit and GOOGLE_API_KEY and GITHUB_TOKEN: 
    placeholder.empty()
    st.success("Added successful")
else:
    pass
