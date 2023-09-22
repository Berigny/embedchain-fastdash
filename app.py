import streamlit as st
import requests
import os

# Placeholder for GPT-4 API URL
GPT_4_API_URL = "https://gpt-4-api.example.com"

def query_gpt_4(api_key, query):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(GPT_4_API_URL, json={"query": query}, headers=headers)
    response.raise_for_status()
    return response.json()["answer"]

def main():
    st.title("GPT-4 Query Interface")

    api_key = st.text_input("API Key", type="password")
    query = st.text_area("Query")

    if st.button("Submit"):
        if not api_key:
            st.error("Please provide an API Key.")
            return

        if not query:
            st.error("Please provide a query.")
            return

        with st.spinner("Querying GPT-4..."):
            answer = query_gpt_4(api_key, query)

        st.markdown(f"**Answer:** {answer}")

if __name__ == "__main__":
    main()
