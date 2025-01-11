import streamlit as st
from pinecone_utils import process_query_and_extract_sources
from constants import GENERAL_RAG_SYSTEM_PROMPT, GENERATION_MODEL, OPENAI_API_KEY,GENERAL_RAG_PROMPT
from openai import OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)

def get_response(query,top_k=10):
    context , sources = process_query_and_extract_sources(query,top_k)
    prompt = GENERAL_RAG_PROMPT.format(
        question=query,context=context
    )
    completion= client.chat.completions.create(
    model=GENERATION_MODEL,
    messages=[
            {
                "role": "system", 
                "content": GENERAL_RAG_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    response = completion.choices[0].message.content
    return response,sources