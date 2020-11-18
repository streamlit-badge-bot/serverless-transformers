import functools
import streamlit as st
#st.set_page_config(page_title="Transformer on Cloud Run",
#                   initial_sidebar_state="expanded")
import requests
from newspaper import Article

DEFAULT_QUESTION = "When was Nvidia founded?"
DEFAULT_URL = "https://en.wikipedia.org/wiki/Nvidia"
DEFAULT_ENDPOINT = "https://cloudrun-transformer-test-34x4ouuclq-de.a.run.app/predict"

st.sidebar.markdown("# Transformer on Cloud Run")
st.sidebar.markdown("**Model**")
st.sidebar.markdown("`allenai/unifiedqa-t5-base` (220M)")
st.sidebar.markdown("**Options**")

max_words = st.sidebar.slider("Max Doc Word Count", min_value=128, max_value=1024, value=512, step=32)

@st.cache
def download_article(article_url):
    article = Article(article_url, fetch_images=False)
    article.download()
    article.parse()
    article_text = article.text
    return article_text.strip()

@st.cache
def make_api_query(context, question, endpoint):
    query_json = {
        "context": str(context).strip(),
        "question": str(question).strip(),
    }
    response = requests.post(endpoint, json=query_json).json()
    return response

def main():
    st.markdown("## Question Answering Demo")
    article_url = st.text_input("Document URL", DEFAULT_URL)
    article_text = download_article(article_url)
    article_text = " ".join(article_text.split(" ")[:max_words])
    context = article_text
    sentences = context.lower().split(".")
    with st.beta_expander(label="Show Text Document", expanded=False):
        st.markdown(article_text)
    question = st.text_input("Question", DEFAULT_QUESTION)
    if question[-1] != "?":
        question = question.strip() + "?"
    response = make_api_query(context, question, DEFAULT_ENDPOINT)
    try:
        answer = response["answer"][0]
        st.markdown("### "+answer)
        st.markdown("Evidence:")
        answer = answer.lower()
        for s in sentences:
            if answer in s:
                st.markdown("* "+s.replace("\n", "").strip())
    except:
        st.markdown(response)

main()