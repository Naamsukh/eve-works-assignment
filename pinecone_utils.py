import streamlit as st
from openai import OpenAI
from pinecone import Pinecone
from constants import PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY, TEXT_EMBEDDING_MODEL

def fetch_unique_files(index_name=PINECONE_INDEX_NAME):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    
    files_info = {}
    
    fetch_response = index.query(
        vector=[0.0] * 1536,
        top_k=10000,
        include_metadata=True
    )
    
    for match in fetch_response['matches']:
        metadata = match['metadata']
        if 'file_id' in metadata and 'file_name' in metadata:
            files_info[metadata['file_id']] = metadata['file_name']
    
    return [
        {"file_id": file_id, "file_name": file_name}
        for file_id, file_name in files_info.items()
    ]

def fetch_data_from_pinecone(query,top_k=10):
    """
    Fetch data from Pinecone based on a query using OpenAI embeddings.

    Args:
        query (str): The query string.
        index_name (str): Name of the Pinecone index to query.
        top_k (int): Number of top results to return (default: 5).

    Returns:
        dict: The query results from Pinecone.
    """
    # Initialize Pinecone client and connect to the index
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Generate embedding for the query
    embeddings = client.embeddings.create(input=query, model=TEXT_EMBEDDING_MODEL).data[0].embedding

    query_params = {
        "vector": embeddings,
        "top_k": top_k,
        "include_metadata": True
    }

    # Add file_id filter if files are selected in session state
    if "selected_file_ids" in st.session_state and st.session_state.selected_file_ids:
        query_params["filter"] = {
            "file_id": {"$in": st.session_state.selected_file_ids}
        }
    
    response = index.query(**query_params)
    
    return response

def process_query_and_extract_sources(query,top_k=10):

    response = fetch_data_from_pinecone(query,top_k)

    context = ""
    sources = []
    for match in response['matches']:

        context += match['metadata']['text'] + "\n\n"
        metadata = match['metadata']
        if 'file_id' in metadata and 'file_name' in metadata:
            sources.append(
                {
                    "file_id": metadata['file_id'], 
                    "file_name": metadata['file_name'],
                    "text": metadata['text'],
                 }
            )
    
    return context,sources