# RAG chatbot 

## Installation

 ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

## Add following Environments in .env file

```bash
    OPENAI_API_KEY=your_openai_api_key
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_INDEX_NAME=your_pinecone_index_name
```

## Running the chatbot Application

```bash
    streamlit run app.py
```


