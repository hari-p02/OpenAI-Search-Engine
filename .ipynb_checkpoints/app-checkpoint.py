import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import openai
import os
import pinecone
load_dotenv()
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment='asia-southeast1-gcp-free')
openai.api_key = os.getenv("OPENAI_API_KEY")
index = pinecone.Index("clubs-index")




def search_engine(query):
    response = openai.Embedding.create(
    input="computer science",
    model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']
    query_response = index.query(
        namespace='uconn-clubs',
        top_k=10,
        include_values=True,
        include_metadata=True,
        vector=query_embedding,
    )
    
    ret = []
    for m in query_response["matches"]:
        temp = dict()
        temp["url"] = m["id"]
        temp["name"] = m["metadata"]["Club Name"]
        temp["short_desc"] = m["metadata"]["Club Short Description"]
        temp["long_desc"] = m["metadata"]["Club Long Description"]
        ret.append(temp.copy())
    
    return ret

def display_card(result):
    col1, col2 = st.beta_columns([1, 3])

    with col1:
        st.image("https://via.placeholder.com/100")  # Use an appropriate image or logo

    with col2:
        st.markdown(f"**{result['name']}**")
        st.markdown(result['name'])
        st.markdown(result['short_desc'])
        st.markdown(result['long_desc'])

st.set_page_config(
    page_title="UCONN Clubs Search Engine", page_icon="🐍", layout="wide"
)
st.title("UCONN Clubs Search Engine")

query = st.text_input("Enter your search query:")

if query:
    results = search_engine(query)
    
    if results:
        st.write("Search Results:")
        for r in results:
            st.json(r)
    else:
        st.write("No results found!")
