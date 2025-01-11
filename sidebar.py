import streamlit as st
# from pinecone_utils import fetch_unique_files
from db_utils import get_stored_files
from processing import process_documents



async def configure_sidebar():
    docs = []
    with st.sidebar:
        st.header("Upload PDF Files")
        uploaded_files = st.file_uploader(
            "Choose PDF files", 
            type=['pdf'], 
            accept_multiple_files=True, 
            key="file_uploader"
        )
        if uploaded_files:
            if st.button("Process documents"):
                proceesed_docs,unprocessed_docs = process_documents(uploaded_files)
                
                if proceesed_docs:
                    st.success(f"Processed documents: {proceesed_docs}")
                
                if unprocessed_docs:
                    st.error(f"Unprocessed documents: {unprocessed_docs}")
    
        st.divider()

        st.header("Knowledge Base Files")
        stored_files = get_stored_files()

        if stored_files:
            # Create a mapping of file names to their IDs
            file_options = {file["file_name"]: file["file_id"] for file in stored_files}


            # Display the multiselect widget with file IDs as options
            st.multiselect(
                "Select files to query",
                options=list(file_options.values()), 
                format_func=lambda file_id: next(name for name, id_ in file_options.items() if id_ == file_id),
                key="selected_file_ids",  # Bind the widget to session state
            )

