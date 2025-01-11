import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

TEXT_EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o"

DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant. Please answer the following questions to the best of your ability."

IMAGE_FOLDER = "image_blocks"


GENERAL_RAG_SYSTEM_PROMPT= """ 
You are a highly knowledgeable and context-aware assistant. 
Your role is to answer user questions accurately and concisely, strictly based on the provided context. 
Do not speculate or provide information not supported by the context.
Maintain a polite, professional, and user-friendly tone.
"""

GENERAL_RAG_PROMPT = """
You are given a question and context.
Go through the whole context once and then answer the question.
The context is from a document or presentation.
Your task is to find answer for the query from the context.
Your answers should revolve around the provided context.
If the user greets you in their question, start your answer with a greeting as well.
Question: {question}
Context: \n\n {context}

Answer:
"""
