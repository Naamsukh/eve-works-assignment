import time
import os
from regex import T
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone
from pdfminer.high_level import extract_text
from chonkie import SemanticChunker
from db_utils import store_file_info
from langchain_core.documents.base import Document
from tqdm.auto import tqdm
from constants import PINECONE_API_KEY, PINECONE_INDEX_NAME, TEXT_EMBEDDING_MODEL

def create_documents_from_chunks(file_name,chunks):

    file_id = str(int(time.time()))
    documents = []
    for idx,chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk.text,
            metadata={
                "id": f"{file_id}-{idx}",
                "file_id":  file_id,
                "file_name": file_name,
                "text": chunk.text,
                "token_count": chunk.token_count,
                "start": chunk.start_index,
                "end": chunk.end_index,
                }
        )
        documents.append(doc)
    
    return documents ,file_id
        
def semantic_chunking(text):
    chunker = SemanticChunker(
        embedding_model=TEXT_EMBEDDING_MODEL,  
        threshold=0.55,
        chunk_size=600,
        min_sentences=2,
    )
    return chunker.chunk(text)


def check_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    indexes = pc.Index(PINECONE_INDEX_NAME)
    if indexes:
        return True
    else:
        return False

def upsert_documents_in_pinecone(documents):
    print(f"\nStarting to upsert {len(documents)} documents to Pinecone")
    start_time = time.time()
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    
    batch_size = 32
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    try:
        for i in tqdm(range(0, len(documents), batch_size), desc="Upserting batches"):
            batch_start_time = time.time()
            
            # Get batch of documents
            batch = documents[i:i + batch_size]
            current_batch_size = len(batch)
            print(f"Processing batch {i//batch_size + 1}/{total_batches} with {current_batch_size} documents")
            
            # Extract text content for embedding
            texts = [doc.page_content for doc in batch]
            
            # Create embeddings using OpenAI
            try:
                client = OpenAI()
                res = client.embeddings.create(input=texts, model=TEXT_EMBEDDING_MODEL)
                embeddings = [record.embedding for record in res.data]
            except Exception as e:
                print(f"Error creating embeddings: {str(e)}")
                raise
            
            # Prepare vectors for upserting
            vectors_to_upsert = []
            for doc, embedding in zip(batch, embeddings):
                vector = {
                    'id': doc.metadata['id'],
                    'values': embedding,
                    'metadata': doc.metadata
                }
                vectors_to_upsert.append(vector)
            
            # Upsert batch to Pinecone
            try:
                print(f"Upserting batch to Pinecone")
                index.upsert(vectors=vectors_to_upsert)
                batch_end_time = time.time()
                print(f"Batch upsert completed in {batch_end_time - batch_start_time:.2f} seconds")
            except Exception as e:
                print(f"Error upserting to Pinecone: {str(e)}")
                raise
                
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Completed upserting all documents in {total_time:.2f} seconds")
        
    except Exception as e:
        print(f"Error in upsert process: {str(e)}")
        raise

def process_documents(uploaded_files):
    total_files = len(uploaded_files)
    processed_documents = []
    unprocessed_documents = []
    print(f"\nStarting to process {total_files} files")
    
    for idx, uploaded_file in enumerate(uploaded_files, 1):
        try:
            print(f"\nProcessing file {idx}/{total_files}: {uploaded_file.name}")
            
            text = extract_text(uploaded_file)
            print(f"Successfully extracted text from {uploaded_file.name}")
            
            chunks = semantic_chunking(text)
            print(f"Created {len(chunks)} chunks from {uploaded_file.name}")
            
            documents ,file_id = create_documents_from_chunks(uploaded_file.name, chunks)
            print(f"Created {len(documents)} documents from chunks")
            
            upsert_documents_in_pinecone(documents)
            print(f"Successfully processed {uploaded_file.name}")
            
            store_file_info(file_id,uploaded_file.name)
            print(f"Stored file info in database")

            processed_documents.append(uploaded_file.name)

        except Exception as e:
            print(f"Error processing file {uploaded_file.name}: {str(e)}")            
            unprocessed_documents.append(uploaded_file.name)
            continue
    
    return processed_documents, unprocessed_documents