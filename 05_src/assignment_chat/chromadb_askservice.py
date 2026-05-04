
import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv('../.secrets')

# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_client.list_collections()
collection=chroma_client.get_collection(name="origin")

client = OpenAI(base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
                 api_key='any value',
                 default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')})

@tool
def search_pdf(query: str):
    """ This service retrieves the relavant chunks for the book for context"""
    query_embedding = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    print("search context:",results["documents"][0])

    return results["documents"][0]

def generate_response(query:str):
    context = search_pdf(query)
    print("Generated context:\n", context)
    prompt = f"""
    Answer the question using ONLY the context below.
    If the answer is not in the context, say "I don't know".
    Context:
    {context}

    Question:
    {query}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides information based on book context."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content