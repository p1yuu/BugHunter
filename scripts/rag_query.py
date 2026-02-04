import chromadb
from chromadb.utils import embedding_functions
import requests

# Chroma client
client = chromadb.Client()

# Aynı embedding fonksiyonu
embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Knowledge koleksiyonunu al
collection = client.get_collection(
    name="secai_knowledge",
    embedding_function=embedding
)

def ask_secai(question):
    # En alakalı 4 belgeyi çek
    results = collection.query(
        query_texts=[question],
        n_results=4
    )

    context = "\n\n".join(results["documents"][0])

    prompt = f"""
You are a professional AI Security Research Assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}
"""

    # Ollama API’ye sor
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "secai",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

if __name__ == "__main__":
    while True:
        q = input("Sorunuz: ")
        print(ask_secai(q))
