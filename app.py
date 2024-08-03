import streamlit as st
import pandas as pd
import fitz
from chroma_setup import ChromaRAG
from rest_framework.response import Response
from baseapi import BaseApi

if 'collections' not in st.session_state:
    st.session_state.collections = []

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Define a function to handle file upload and processing
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text_content = ''
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text_content += page.get_text()

        rag = ChromaRAG()
        chunks = rag.chunk_text(text_content)
        print(type(chunks))

        rag.create_collection(uploaded_file.name,chunks=chunks)
    
        st.success(f"File '{uploaded_file.name}' uploaded and processed successfully!")

# Define a function to handle the submit action
def handle_submit(selected_option, query):
    st.write(f"Dropdown selected: {selected_option}")
    st.write(f"Query: {query}")
    # Add your query processing logic here

    rag = ChromaRAG()
    collection = rag.get_collection(collection_name=selected_option)
    top_chunks = ChromaRAG().run_query(collection,query=query)

    # print(top_chunks)
    # #Go to GPT
    baseapi = BaseApi()
    baseapi.add_message('system','You are a very good data researcher.You are tasked with answering any question being asked.')
    baseapi.add_message('user',f"Answer the query based on the context provided CONTEXT ::: {top_chunks} QUERY ::: {query}.Provide output in Proper Format and Points such as bullet or numbered or underlining the important words.")

    answer = baseapi.make_openai_call_api()
    st.write(f'Answer: {answer}')


# Streamlit UI
st.title("Streamlit File Upload and Query Interface")

# Layout: Dropdown and File Upload side by side
col1, col2 = st.columns([3, 1])

with col1:
    # Dropdown menu with an option to upload a new file
    collection_manager= ChromaRAG()
    collections = collection_manager.all_collections()
    names = [collection.name for collection in collections]

    options = names + ["Upload a new file"]
    selected_option = st.selectbox("Select an option:", options)

# Check if "Upload a new file" is selected
if selected_option == "Upload a new file":
    uploaded_file = st.file_uploader("Upload a file",type=['pdf'])
else:
    uploaded_file = None

# Query input
query = st.text_input("Enter your query:")

# Submit button
if st.button("Submit"):
    handle_submit(selected_option, query)

# Process the file upload
df = handle_file_upload(uploaded_file)
