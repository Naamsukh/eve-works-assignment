import asyncio
import logging
import streamlit as st
import os
from dotenv import load_dotenv
from rag import get_response
from db_utils import initialize_db
from sidebar import configure_sidebar

# load the .env file
load_dotenv()
OPENAI_API_TOKEN = os.getenv('OPENAI_API_KEY')


async def main():
    try:
        logging.info("Starting the RAG Chatbot...")
        st.title("Chatbot")

        # Streamlit sidebar for file upload and processing
        await configure_sidebar()
        
        # Initialize the database 
        initialize_db()
        
        # Main area for chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("How can I help you?", key="chat_input")
        
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
           
            response,sources = get_response(prompt)
               
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
                with st.expander("View Chunks"):
                    if sources and len(sources) > 0:
                        tabs = st.tabs([f"Chunk {i+1}" for i in range(len(sources))])
                        for tab, source in zip(tabs, sources):
                            with tab:
                                st.markdown(f"**Filename:** {source['file_name']}")
                                st.markdown(f"**Content:** {source['text']}")
                    else:
                        st.write("No sources available for this response.")
                    
    except Exception as e:
        logging.error("Error occured :",e)
        raise e

if __name__ == "__main__":
    asyncio.run(main())