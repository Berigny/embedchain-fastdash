
import streamlit as st
import os
from string import Template
from embedchain import App
from embedchain.config import QueryConfig

# Define app configurations
PROMPT = Template(
    '''Use the given context to answer the question at the end.
If you don't know the answer, say so, but don't try to make one up.
At the end of the answer, also give the sources as a bulleted list.
Display the answer as markdown text.

Context: $context

Query: $query

Answer:'''
)
query_config = QueryConfig(
    template=PROMPT, number_documents=5, max_tokens=2000, model="gpt-4"
)

def explore_your_knowledge_base(
    openai_api_key, web_page_urls, youtube_urls, pdf_urls, text, query
):
    answer_suffix = ""

    if not openai_api_key:
        return "Did you forget adding your OpenAI API key? If you don't have one, you can get it [here](https://platform.openai.com/account/api-keys)."

    if not query:
        return "Did you forget writing your query in the query box?"

    os.environ["OPENAI_API_KEY"] = openai_api_key
    app = App()

    try:
        if web_page_urls:
            [app.add("web_page", url) for url in web_page_urls]

        if youtube_urls:
            [app.add("youtube_video", url) for url in youtube_urls]

        if pdf_urls:
            [app.add("pdf_file", url) for url in pdf_urls]

        if text:
            app.add_local("text", text)

    except Exception as e:
        print(str(e))
        answer_suffix = "I couldn't analyze some sources. If you think this is an error, please try again later or make a suggestion [here](https://github.com/dkedar7/embedchain-fastdash/issues)."

    answer = app.query(query, query_config)
    answer = f'''{answer}

    {answer_suffix}
    '''

    return answer

# Streamlit layout and interactivity
st.title("Explore Your Knowledge Base")

openai_api_key = st.text_input("API Key", help="Get yours at https://platform.openai.com/account/api-keys")
web_page_urls = st.text_area("Include all the reference web URLs", help="Enter URLs separated by commas")
youtube_urls = st.text_area("Include all the reference YouTube URLs", help="Enter URLs separated by commas")
pdf_urls = st.text_area("Include all the reference PDF URLs", help="Enter URLs separated by commas")
text = st.text_area("Any additional information that could be useful")
query = st.text_area("Write your query here", help="Write your query here")

if st.button("Submit"):
    answer = explore_your_knowledge_base(
        openai_api_key, web_page_urls.split(","), youtube_urls.split(","), pdf_urls.split(","), text, query
    )
    st.markdown(answer)
